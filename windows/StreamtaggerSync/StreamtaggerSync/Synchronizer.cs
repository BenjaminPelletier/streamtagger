using Json.Serialization;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Security.Cryptography;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Web;
using System.Windows.Forms;

namespace StreamtaggerSync
{
    class Synchronizer
    {
        /// <summary>
        /// Salt to use when constructing the password hash
        /// </summary>
        /// <remarks>
        /// If changing here, also change in 
        /// </remarks>
        const string SALT = "K80Tgi^w1&jc";

        public class LogMessageEventArgs : EventArgs
        {
            public readonly string Message;

            public LogMessageEventArgs(string message)
            {
                Message = message;
            }
        }

        public class PlaylistToDelete
        {
            public readonly FileInfo Path;
            public bool Delete;

            public PlaylistToDelete(FileInfo path)
            {
                Path = path;
                Delete = false;
            }
        }

        public class RequestDeleteOldPlaylistsEventArgs : EventArgs
        {
            public readonly PlaylistToDelete[] Playlists;

            public RequestDeleteOldPlaylistsEventArgs(IEnumerable<FileInfo> playlists)
            {
                Playlists = playlists.Select(fi => new PlaylistToDelete(fi)).ToArray();
            }
        }

        public class SongToDelete
        {
            public readonly FileInfo Path;
            public bool Delete;

            public SongToDelete(FileInfo path)
            {
                Path = path;
                Delete = false;
            }
        }

        public class RequestDeleteUnreferencedSongsEventArgs : EventArgs
        {
            public readonly SongToDelete[] Songs;

            public RequestDeleteUnreferencedSongsEventArgs(IEnumerable<FileInfo> songs)
            {
                Songs = songs.Select(s => new SongToDelete(s)).ToArray();
            }
        }

        private PlaylistSet _Playlists;
        private Preferences _Preferences;
        private string _Password;

        public event EventHandler<LogMessageEventArgs> LogMessage;
        public event EventHandler<RequestDeleteOldPlaylistsEventArgs> RequestDeleteOldPlaylists;
        public event EventHandler<RequestDeleteUnreferencedSongsEventArgs> RequestDeleteUnreferencedSongs;

        public Synchronizer(PlaylistSet playlists, Preferences preferences, string password)
        {
            _Playlists = playlists;
            _Preferences = preferences;
            _Password = password;
        }

        private void Log(string message)
        {
            LogMessage?.Invoke(this, new LogMessageEventArgs(message));
        }

        public async Task Synchronize(CancellationToken token)
        {
            try
            {
                Log("***STARTING SYNCHRONIZATION***");
                CookieContainer cookies = new CookieContainer();
                using (var handler = new HttpClientHandler() { CookieContainer = cookies })
                using (var client = new HttpClient(handler))
                {
                    // Log in to get session cookie
                    Uri loginUri = new Uri(_Preferences.StreamtaggerUrl, "login");
                    Log("Logging " + _Preferences.Username + " into Streamtagger at " + loginUri.AbsoluteUri + "...");
                    string passwordHash = Hash(SALT + _Preferences.Username + _Password + SALT + _Preferences.Username);
                    var loginData = new Dictionary<string, string>() { { "username", _Preferences.Username }, { "password_hash", passwordHash } };
                    var content = new FormUrlEncodedContent(loginData);
                    using (var response = await client.PostAsync(loginUri, content, token))
                    {
                        if (!response.IsSuccessStatusCode)
                        {
                            Log("Error logging into Streamtagger: " + response.StatusCode + " " + response.ReasonPhrase + ":\r\n" + await response.Content.ReadAsStringAsync());
                            return;
                        }
                    }

                    // Retrieve song lists for all playlists
                    var playlistPathLists = new Dictionary<string, List<string>>();
                    var syncSongs = new Dictionary<string, SyncSong>();
                    Uri songListUri = new Uri(_Preferences.StreamtaggerUrl, "song_list");
                    foreach (Playlist playlistDef in _Playlists.Playlists.Where(p => p.Enabled))
                    {
                        Uri playlistUri = AddQuery(songListUri, playlistDef.Query);
                        Log("Reading song list " + (playlistDef.Name == "" ? "" : ("for " + playlistDef.Name)) + " at " + playlistUri.AbsoluteUri);
                        using (var response = await client.GetAsync(playlistUri, token))
                        {
                            if (!response.IsSuccessStatusCode)
                            {
                                Log("Error reading song list: " + response.StatusCode + " " + response.ReasonPhrase + ":\r\n" + await response.Content.ReadAsStringAsync());
                                return;
                            }
                            string songListJson = await response.Content.ReadAsStringAsync();
                            StreamtaggerSongsResponse parsedResponse = JsonTranslator.Singleton.MakeObject<StreamtaggerSongsResponse>(JsonObject.Parse(songListJson.Trim()));
                            if (parsedResponse.status != "success")
                            {
                                Log("Song list query did not indicate success:\r\n" + songListJson);
                                return;
                            }

                            if (playlistDef.Name != "")
                            {
                                playlistPathLists[playlistDef.Name] = parsedResponse.songs.Select(s => s.path).ToList();
                            }

                            int prevSongPathCount = syncSongs.Count;
                            foreach (var song in parsedResponse.songs)
                            {
                                if (!syncSongs.ContainsKey(song.path))
                                {
                                    syncSongs[song.path] = new SyncSong(song.path, _Preferences.StreamtaggerUrl, _Preferences.MusicPath);
                                }
                            }
                            Log("Added " + (syncSongs.Count - prevSongPathCount) + " new songs to sync list");
                        }
                    }

                    // Download songs
                    string tempFileName = Path.Combine(_Preferences.MusicPath.FullName, "song.partialdownload");
                    int nDownloaded = 0;
                    foreach (SyncSong syncSong in syncSongs.Values)
                    {
                        if (!syncSong.LocalFile.Directory.Exists)
                        {
                            Log("Creating " + syncSong.LocalFile.DirectoryName + " locally");
                            syncSong.LocalFile.Directory.Create();
                        }

                        if (syncSong.LocalFile.Exists)
                        {
                            continue;
                        }

                        Log("Downloading " + syncSong.RemotePath);
                        using (var response = await client.GetAsync(syncSong.RemotePath, token))
                        {
                            if (!response.IsSuccessStatusCode)
                            {
                                Log("Error downloading: " + response.StatusCode + " " + response.ReasonPhrase);
                                continue;
                            }

                            using (var w = new FileStream(tempFileName, FileMode.Create))
                            {
                                await response.Content.CopyToAsync(w);
                            }
                            File.Move(tempFileName, syncSong.LocalFile.FullName);
                            nDownloaded++;
                        }
                    }

                    // Write M3U playlists
                    int nPlaylists = 0;
                    foreach (string playlistName in playlistPathLists.Keys)
                    {
                        string playlistFilename = Path.Combine(_Preferences.PlaylistsPath.FullName, playlistName + ".m3u");
                        using (var w = new StreamWriter(playlistFilename))
                        {
                            w.WriteLine("#EXTM3U");
                            foreach (string songPath in playlistPathLists[playlistName])
                            {
                                w.WriteLine(syncSongs[songPath].LocalFile.FullName);
                            }
                            nPlaylists++;
                        }
                    }

                    // Remove old playlists
                    var newPlaylists = new HashSet<string>(playlistPathLists.Select(kvp => kvp.Key.ToLower()));
                    var oldPlaylists = new List<FileInfo>();
                    foreach (FileInfo fi in _Preferences.PlaylistsPath.GetFiles("*.m3u"))
                    {
                        string playlistName = fi.Name.Substring(0, fi.Name.Length - ".m3u".Length).ToLower();
                        if (!newPlaylists.Contains(playlistName))
                        {
                            oldPlaylists.Add(fi);
                        }
                    }
                    if (oldPlaylists.Any())
                    {
                        var eOldPlaylists = new RequestDeleteOldPlaylistsEventArgs(oldPlaylists);
                        RequestDeleteOldPlaylists?.Invoke(this, eOldPlaylists);
                        var playlistsToDelete = eOldPlaylists.Playlists.Where(p => p.Delete);
                        foreach (PlaylistToDelete playlist in playlistsToDelete)
                        {
                            playlist.Path.Delete();
                        }
                        Log("Deleted " + playlistsToDelete.Count() + " playlists:\r\n" + playlistsToDelete.Select(p => p.Path.FullName).Aggregate((a, b) => a + "\r\n" + b));
                    }

                    // Remove unreferenced songs
                    var newSongs = new HashSet<string>(syncSongs.Select(s => s.Value.LocalFile.FullName.ToLower()));
                    var oldSongs = new List<FileInfo>();
                    foreach (FileInfo fi in FindSongs(_Preferences.MusicPath))
                    {
                        if (!newSongs.Contains(fi.FullName.ToLower()))
                        {
                            oldSongs.Add(fi);
                        }
                    }
                    if (oldSongs.Any())
                    {
                        var eOldSongs = new RequestDeleteUnreferencedSongsEventArgs(oldSongs);
                        RequestDeleteUnreferencedSongs?.Invoke(this, eOldSongs);
                        var songsToDelete = eOldSongs.Songs.Where(s => s.Delete);
                        foreach (SongToDelete song in songsToDelete)
                        {
                            song.Path.Delete();
                        }
                        Log("Deleted " + songsToDelete.Count() + " songs:\r\n" + songsToDelete.Select(s => s.Path.FullName).Aggregate((a, b) => a + "\r\n" + b));
                    }

                    Log("Synchronization successful; downloaded " + nDownloaded + " songs and updated " + nPlaylists + " playlists.");
                }
            }
            catch (WebException ex)
            {
                if (ex.Status == WebExceptionStatus.RequestCanceled)
                {
                    Log("Synchronization was cancelled");
                }
            }
            catch (Exception ex)
            {
                if (ex is AggregateException)
                {
                    ex = ex.InnerException;
                }
                Log("Fatal unexpected error " + ex.GetType().FullName + ":\r\n" + ex.ToString());
            }
        }

        static string Hash(string input)
        {
            using (SHA1Managed sha1 = new SHA1Managed())
            {
                var hash = sha1.ComputeHash(Encoding.UTF8.GetBytes(input));
                return string.Concat(hash.Select(b => b.ToString("x2")));
            }
        }

        public static Uri AddQuery(Uri uri, string queryString)
        {
            var uriBuilder = new UriBuilder(uri);
            var query = HttpUtility.ParseQueryString(queryString);
            uriBuilder.Query = query.ToString();
            return uriBuilder.Uri;
        }

        private static List<FileInfo> FindSongs(DirectoryInfo path)
        {
            var result = new List<FileInfo>(path.GetFiles("*.mp3"));
            foreach (DirectoryInfo di in path.GetDirectories())
            {
                result.AddRange(FindSongs(di));
            }
            return result;
        }

        private class SyncSong
        {
            public readonly Uri RemotePath;
            public readonly FileInfo LocalFile;

            public SyncSong(string relativeSongPath, Uri baseUri, DirectoryInfo mediaPath)
            {
                if (!relativeSongPath.Contains("media/"))
                {
                    throw new FormatException("Relative song path provided by server does not contain 'media/': " + relativeSongPath);
                }
                if (baseUri.AbsolutePath.EndsWith("/") && relativeSongPath.StartsWith("/"))
                {
                    relativeSongPath = relativeSongPath.Substring(1);
                }
                RemotePath = new Uri(baseUri.AbsoluteUri + relativeSongPath);
                string[] relativeSongPathComponents = relativeSongPath.Substring(relativeSongPath.IndexOf("media/") + "media/".Length).Split('/');
                LocalFile = new FileInfo(Path.Combine(mediaPath.FullName, relativeSongPathComponents.Aggregate(Path.Combine)));
            }
        }

        #pragma warning disable 0649

        private class StreamtaggerSongsResponse
        {
            public string status;
            public List<StreamtaggerSong> songs;

            public class StreamtaggerSong
            {
                public string title;
                public string path;
            }
        }

        #pragma warning restore 0649

    }
}
