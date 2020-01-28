using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Json.Serialization;
using System.IO;

namespace StreamtaggerSync
{
    public partial class PlaylistListBox : UserControl
    {
        private List<PlaylistControl> PlaylistControls = new List<PlaylistControl>();

        public event EventHandler PlaylistsChanged;
        public event EventHandler<PlaylistControl.InformationRequestedEventArgs> InformationRequested;

        public PlaylistListBox()
        {
            InitializeComponent();
        }

        public PlaylistSet Playlists
        {
            get
            {
                return new PlaylistSet(PlaylistControls.Select(ctrl => ctrl.Playlist).ToList());
            }
            set
            {
                this.SuspendLayout();
                foreach (PlaylistControl playlistControl in PlaylistControls)
                {
                    RemoveControl(playlistControl);
                }
                PlaylistControls.Clear();
                foreach (Playlist playlist in value.Playlists)
                {
                    AddControl(playlist);
                }
                this.ResumeLayout();
            }
        }

        private PlaylistControl AddControl(Playlist playlist = null)
        {
            var playlistControl = new PlaylistControl();
            playlistControl.Left = this.ClientRectangle.Left;
            if (PlaylistControls.Count == 0)
            {
                playlistControl.Top = this.ClientRectangle.Top;
            }
            else
            {
                playlistControl.Top = PlaylistControls.Last().Bottom + 3;
            }
            playlistControl.Width = this.ClientRectangle.Width;
            playlistControl.Anchor = AnchorStyles.Top | AnchorStyles.Left | AnchorStyles.Right;
            if (playlist != null)
            {
                playlistControl.Playlist = playlist;
            }
            playlistControl.DeleteRequested += playlist_DeleteRequested;
            playlistControl.PlaylistChanged += playlist_PlaylistChanged;
            playlistControl.InformationRequested += playlist_InformationRequested;
            PlaylistControls.Add(playlistControl);

            cmdAdd.Top = playlistControl.Bottom + 3;
            cmdLoad.Top = cmdAdd.Top;
            cmdSave.Top = cmdAdd.Top;

            this.Controls.Add(playlistControl);

            return playlistControl;
        }

        private void RemoveControl(PlaylistControl playlistControl)
        {
            this.Controls.Remove(playlistControl);
            playlistControl.DeleteRequested -= playlist_DeleteRequested;
            playlistControl.PlaylistChanged -= playlist_PlaylistChanged;
            playlistControl.InformationRequested -= playlist_InformationRequested;
        }

        private void cmdAdd_Click(object sender, EventArgs e)
        {
            AddControl();
        }

        private void playlist_DeleteRequested(object sender, EventArgs e)
        {
            this.SuspendLayout();
            PlaylistControl playlistControl = sender as PlaylistControl;
            RemoveControl(playlistControl);
            int i = PlaylistControls.IndexOf(playlistControl);
            PlaylistControls.RemoveAt(i);
            for (int j = i; j < PlaylistControls.Count; j++)
            {
                if (j == 0)
                {
                    PlaylistControls[j].Top = this.ClientRectangle.Top;
                }
                else
                {
                    PlaylistControls[j].Top = PlaylistControls[j - 1].Bottom + 3;
                }
            }
            if (PlaylistControls.Count == 0)
            {
                cmdAdd.Top = this.ClientRectangle.Top;
            }
            else
            {
                cmdAdd.Top = PlaylistControls.Last().Bottom + 3;
            }
            cmdLoad.Top = cmdAdd.Top;
            cmdSave.Top = cmdAdd.Top;
            PlaylistsChanged?.Invoke(this, EventArgs.Empty);
            this.ResumeLayout();
        }

        private void playlist_PlaylistChanged(object sender, EventArgs e)
        {
            PlaylistsChanged?.Invoke(this, EventArgs.Empty);
        }

        private void playlist_InformationRequested(object sender, PlaylistControl.InformationRequestedEventArgs e)
        {
            InformationRequested?.Invoke(this, e);
        }

        private void cmdLoad_Click(object sender, EventArgs e)
        {
            if (ofdPlaylists.ShowDialog(this) == DialogResult.OK)
            {
                PlaylistSet newPlaylists;
                try
                {
                    newPlaylists = JsonTranslator.Singleton.MakeObject<PlaylistSet>(JsonObject.Parse(File.ReadAllText(ofdPlaylists.FileName).Trim()));
                } catch (Exception ex)
                {
                    MessageBox.Show(this, "Error loading playlists:\r\n" + ex.GetType().FullName + ": " + ex.ToString(), "Error loading playlists", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }
                foreach (Playlist playlist in newPlaylists.Playlists)
                {
                    AddControl(playlist);
                }
                sfdPlaylists.InitialDirectory = ofdPlaylists.InitialDirectory;
                sfdPlaylists.FileName = ofdPlaylists.FileName;
                PlaylistsChanged?.Invoke(this, EventArgs.Empty);
            }
        }

        private void cmdSave_Click(object sender, EventArgs e)
        {
            if (sfdPlaylists.ShowDialog(this) == DialogResult.OK)
            {
                File.WriteAllText(sfdPlaylists.FileName, JsonTranslator.Singleton.MakeJson(Playlists).ToMultilineString());
                ofdPlaylists.InitialDirectory = sfdPlaylists.InitialDirectory;
                ofdPlaylists.FileName = sfdPlaylists.FileName;
            }
        }
    }
}
