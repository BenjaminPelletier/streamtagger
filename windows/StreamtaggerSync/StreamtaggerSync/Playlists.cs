using Json.Serialization;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace StreamtaggerSync
{
    public class Playlist
    {
        public string Name;
        public string Query;

        public Playlist(string name, string query)
        {
            Name = name;
            Query = query;
        }
    }

    public class PlaylistSet
    {
        private static JsonTranslator _Translator = new JsonTranslator();

        public List<Playlist> Playlists;

        public PlaylistSet(List<Playlist> playlists)
        {
            Playlists = playlists;
        }

        public static PlaylistSet FromFile(string jsonFilename)
        {
            return _Translator.MakeObject<PlaylistSet>(JsonObject.Parse(File.ReadAllText(jsonFilename).Trim()));
        }

        public void WriteToFile(string jsonFilename)
        {
            using (var f = new StreamWriter(jsonFilename))
            {
                f.WriteLine(_Translator.MakeJson(this).ToMultilineString());
            }
        }
    }
}
