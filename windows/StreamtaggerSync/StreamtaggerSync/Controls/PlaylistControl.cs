using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace StreamtaggerSync
{
    public partial class PlaylistControl : UserControl
    {
        public class InformationRequestedEventArgs : EventArgs
        {
            public Uri StreamtaggerUri;
        }

        private Playlist _Playlist;

        public event EventHandler DeleteRequested;
        public event EventHandler PlaylistChanged;
        public event EventHandler<InformationRequestedEventArgs> InformationRequested;

        public Playlist Playlist
        {
            get
            {
                _Playlist.Name = txtName.Text;
                _Playlist.Query = txtQuery.Text;
                _Playlist.Enabled = chkEnable.Checked;
                return _Playlist;
            }
            set
            {
                _Playlist = value;
                txtName.Text = value.Name;
                txtQuery.Text = value.Query;
                chkEnable.Checked = value.Enabled;
            }
        }

        public PlaylistControl()
        {
            InitializeComponent();
            _Playlist = new Playlist(txtName.Text, txtQuery.Text, true);
        }

        private void cmdDelete_Click(object sender, EventArgs e)
        {
            DeleteRequested?.Invoke(this, EventArgs.Empty);
        }

        private void chkEnable_CheckedChanged(object sender, EventArgs e)
        {
            if (chkEnable.Checked != _Playlist.Enabled)
            {
                _Playlist.Enabled = chkEnable.Checked;
                PlaylistChanged?.Invoke(this, EventArgs.Empty);
            }
        }

        private void txtName_Leave(object sender, EventArgs e)
        {
            if (txtName.Text != _Playlist.Name)
            {
                _Playlist.Name = txtName.Text;
                PlaylistChanged?.Invoke(this, EventArgs.Empty);
            }
        }

        private void txtQuery_Leave(object sender, EventArgs e)
        {
            if (txtQuery.Text != _Playlist.Query)
            {
                _Playlist.Query = txtQuery.Text;
                PlaylistChanged?.Invoke(this, EventArgs.Empty);
            }
        }

        private void llQuery_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            var infoArgs = new InformationRequestedEventArgs();
            InformationRequested?.Invoke(this, infoArgs);
            if (infoArgs.StreamtaggerUri != null)
            {
                Uri uri = Synchronizer.AddQuery(infoArgs.StreamtaggerUri, txtQuery.Text);
                System.Diagnostics.Process.Start(uri.AbsoluteUri);
            }
        }
    }
}
