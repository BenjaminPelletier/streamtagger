namespace StreamtaggerSync
{
    partial class PlaylistListBox
    {
        /// <summary> 
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary> 
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Component Designer generated code

        /// <summary> 
        /// Required method for Designer support - do not modify 
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(PlaylistListBox));
            this.cmdAdd = new System.Windows.Forms.Button();
            this.cmdSave = new System.Windows.Forms.Button();
            this.cmdLoad = new System.Windows.Forms.Button();
            this.ofdPlaylists = new System.Windows.Forms.OpenFileDialog();
            this.sfdPlaylists = new System.Windows.Forms.SaveFileDialog();
            this.SuspendLayout();
            // 
            // cmdAdd
            // 
            this.cmdAdd.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(192)))), ((int)(((byte)(225)))), ((int)(((byte)(192)))));
            this.cmdAdd.Location = new System.Drawing.Point(3, 3);
            this.cmdAdd.Name = "cmdAdd";
            this.cmdAdd.Size = new System.Drawing.Size(23, 23);
            this.cmdAdd.TabIndex = 0;
            this.cmdAdd.Text = "+";
            this.cmdAdd.UseVisualStyleBackColor = false;
            this.cmdAdd.Click += new System.EventHandler(this.cmdAdd_Click);
            // 
            // cmdSave
            // 
            this.cmdSave.BackgroundImage = ((System.Drawing.Image)(resources.GetObject("cmdSave.BackgroundImage")));
            this.cmdSave.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch;
            this.cmdSave.Location = new System.Drawing.Point(61, 3);
            this.cmdSave.Name = "cmdSave";
            this.cmdSave.Size = new System.Drawing.Size(23, 23);
            this.cmdSave.TabIndex = 4;
            this.cmdSave.UseVisualStyleBackColor = true;
            this.cmdSave.Click += new System.EventHandler(this.cmdSave_Click);
            // 
            // cmdLoad
            // 
            this.cmdLoad.BackgroundImage = global::StreamtaggerSync.Properties.Resources.folder_xxl;
            this.cmdLoad.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch;
            this.cmdLoad.Location = new System.Drawing.Point(32, 3);
            this.cmdLoad.Name = "cmdLoad";
            this.cmdLoad.Size = new System.Drawing.Size(23, 23);
            this.cmdLoad.TabIndex = 3;
            this.cmdLoad.UseVisualStyleBackColor = true;
            this.cmdLoad.Click += new System.EventHandler(this.cmdLoad_Click);
            // 
            // ofdPlaylists
            // 
            this.ofdPlaylists.FileName = "Playlists.json";
            this.ofdPlaylists.Filter = "JSON|*.json";
            this.ofdPlaylists.RestoreDirectory = true;
            // 
            // sfdPlaylists
            // 
            this.sfdPlaylists.DefaultExt = "JSON|*.json";
            this.sfdPlaylists.FileName = "Playlists.json";
            this.sfdPlaylists.RestoreDirectory = true;
            // 
            // PlaylistListBox
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.AutoScroll = true;
            this.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D;
            this.Controls.Add(this.cmdSave);
            this.Controls.Add(this.cmdLoad);
            this.Controls.Add(this.cmdAdd);
            this.Name = "PlaylistListBox";
            this.Size = new System.Drawing.Size(227, 108);
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Button cmdAdd;
        private System.Windows.Forms.Button cmdLoad;
        private System.Windows.Forms.Button cmdSave;
        private System.Windows.Forms.OpenFileDialog ofdPlaylists;
        private System.Windows.Forms.SaveFileDialog sfdPlaylists;
    }
}
