using Json.Serialization;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace StreamtaggerSync
{
    public class Preferences
    {
        static JsonTranslator _Translator = new JsonTranslator();

        public Uri StreamtaggerUrl = new Uri("https://bjp.streamtagger.com");
        public string Username;
        public DirectoryInfo MusicPath = new DirectoryInfo(Path.Combine(Syroot.Windows.IO.KnownFolders.Music.Path, "Streamtagger"));
        public DirectoryInfo PlaylistsPath = new DirectoryInfo(Path.Combine(Syroot.Windows.IO.KnownFolders.Music.Path, "Streamtagger"));

        public static Preferences FromFile(string jsonFilename)
        {
            return _Translator.MakeObject<Preferences>(JsonObject.Parse(File.ReadAllText(jsonFilename).TrimEnd()));
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
