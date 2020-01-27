using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace StreamtaggerSync
{
    public partial class PreferencesDialog : Form
    {
        private Preferences _Preferences;

        public Preferences Preferences
        {
            set
            {
                _Preferences = value;
                if (_Preferences.StreamtaggerUrl != null)
                {
                    txtStreamtaggerUrl.Text = _Preferences.StreamtaggerUrl.AbsoluteUri;
                }
                txtUsername.Text = _Preferences.Username;
                if (_Preferences.MusicPath != null)
                {
                    fbdMusicPath.SelectedPath = _Preferences.MusicPath.FullName;
                    lblMusicPath.Text = fbdMusicPath.SelectedPath;
                }
                if (_Preferences.PlaylistsPath != null)
                {
                    fbdPlaylistsPath.SelectedPath = _Preferences.PlaylistsPath.FullName;
                    lblPlaylistsPath.Text = fbdPlaylistsPath.SelectedPath;
                }
            }
        }

        public string Instructions
        {
            set
            {
                lblInstructions.Text = value;
            }
        }

        public PreferencesDialog()
        {
            InitializeComponent();
            DialogResult = DialogResult.Cancel;
        }

        private void cmdOk_Click(object sender, EventArgs e)
        {
            try
            {
                _Preferences.StreamtaggerUrl = new Uri(txtStreamtaggerUrl.Text);
            }
            catch (UriFormatException ex)
            {
                lblInstructions.Text = ex.Message;
                return;
            }
            _Preferences.Username = txtUsername.Text;
            _Preferences.MusicPath = new DirectoryInfo(fbdMusicPath.SelectedPath);
            _Preferences.PlaylistsPath = new DirectoryInfo(fbdPlaylistsPath.SelectedPath);
            DialogResult = DialogResult.OK;
            Close();
        }

        private void cmdMusicPath_Click(object sender, EventArgs e)
        {
            string oldPath = fbdMusicPath.SelectedPath;
            if (fbdMusicPath.ShowDialog(this) == DialogResult.OK)
            {
                lblMusicPath.Text = fbdMusicPath.SelectedPath;
            }
            else
            {
                fbdMusicPath.SelectedPath = oldPath;
            }
        }

        private void cmdPlaylistsPath_Click(object sender, EventArgs e)
        {
            string oldPath = fbdPlaylistsPath.SelectedPath;
            if (fbdPlaylistsPath.ShowDialog(this) == DialogResult.OK)
            {
                lblPlaylistsPath.Text = fbdPlaylistsPath.SelectedPath;
            }
            else
            {
                fbdPlaylistsPath.SelectedPath = oldPath;
            }
        }

        private void txt_KeyPress(object sender, KeyPressEventArgs e)
        {
            if (e.KeyChar == Convert.ToChar(Keys.Return))
            {
                cmdOk.PerformClick();
                e.Handled = true;
            }
        }
    }
}
