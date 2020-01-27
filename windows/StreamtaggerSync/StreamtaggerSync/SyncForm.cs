using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace StreamtaggerSync
{
    public partial class SyncForm : Form
    {
        private FileInfo _PreferencesPath = new FileInfo("Preferences.json");
        private Preferences _Preferences;

        private FileInfo _PlaylistsPath = new FileInfo("Playlists.json");

        private string _Password = null;

        public SyncForm()
        {
            InitializeComponent();
            if (_PreferencesPath.Exists)
            {
                _Preferences = Preferences.FromFile(_PreferencesPath.FullName);
            }
            else
            {
                _Preferences = new Preferences();
            }
            if (_PlaylistsPath.Exists)
            {
                playlistListBox1.Playlists = PlaylistSet.FromFile(_PlaylistsPath.FullName);
            }
        }

        private void exitToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }

        private void preferencesToolStripMenuItem_Click(object sender, EventArgs e)
        {
            UpdatePreferences();
        }

        private DialogResult UpdatePreferences(string instructions = null)
        {
            var prefs = new PreferencesDialog();
            prefs.Preferences = _Preferences;
            if (instructions != null)
            {
                prefs.Instructions = instructions;
            }
            DialogResult result = prefs.ShowDialog(this);
            if (result == DialogResult.OK)
            {
                _Preferences.WriteToFile(_PreferencesPath.FullName);
            }
            return result;
        }

        private void playlistListBox1_PlaylistsChanged(object sender, EventArgs e)
        {
            playlistListBox1.Playlists.WriteToFile(_PlaylistsPath.FullName);
        }

        private async void cmdSync_Click(object sender, EventArgs e)
        {
            if (cmdSync.Text == "Sync!")
            {
                cmdSync.Text = "Cancel";
                var cts = new CancellationTokenSource();
                cmdSync.Tag = cts;
                await Synchronize(cts.Token);
                cmdSync.Text = "Sync!";
                cmdSync.Enabled = true;
            }
            else if (cmdSync.Text == "Cancel")
            {
                (cmdSync.Tag as CancellationTokenSource).Cancel();
                cmdSync.Text = "Cancelling...";
                cmdSync.Enabled = false;
            }
        }

        private async Task Synchronize(CancellationToken token)
        {
            if (_Preferences.Username == "")
            {
                if (UpdatePreferences("Please specify a valid username") != DialogResult.OK)
                {
                    return;
                }
            }

            var passwordDialog = new PasswordDialog();
            passwordDialog.Password = _Password;
            DialogResult result = passwordDialog.ShowDialog(this);
            if (result != DialogResult.OK)
            {
                return;
            }
            _Password = passwordDialog.Password;

            var synchronizer = new Synchronizer(playlistListBox1.Playlists, _Preferences, _Password);
            synchronizer.LogMessage += synchronizer_LogMessage;

            await synchronizer.Synchronize(token);
        }

        private void synchronizer_LogMessage(object sender, Synchronizer.LogMessageEventArgs e)
        {
            if (txtSyncLog.InvokeRequired)
            {
                txtSyncLog.Invoke(new Action<object, Synchronizer.LogMessageEventArgs>(synchronizer_LogMessage));
                return;
            }

            txtSyncLog.Text += "==> " + e.Message + "\r\n";
            txtSyncLog.SelectionStart = txtSyncLog.Text.Length - 1;
            txtSyncLog.ScrollToCaret();
        }

        private void playlistListBox1_InformationRequested(object sender, PlaylistControl.InformationRequestedEventArgs e)
        {
            e.StreamtaggerUri = _Preferences.StreamtaggerUrl;
        }
    }
}
