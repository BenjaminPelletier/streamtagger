namespace StreamtaggerSync
{
    partial class SyncForm
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

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(SyncForm));
            this.menuStrip1 = new System.Windows.Forms.MenuStrip();
            this.fileToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.preferencesToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.toolStripMenuItem1 = new System.Windows.Forms.ToolStripSeparator();
            this.exitToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.splitContainer1 = new System.Windows.Forms.SplitContainer();
            this.gbPlaylists = new System.Windows.Forms.GroupBox();
            this.gbSync = new System.Windows.Forms.GroupBox();
            this.txtSyncLog = new System.Windows.Forms.TextBox();
            this.cmdSync = new System.Windows.Forms.Button();
            this.cmdCopyLog = new System.Windows.Forms.Button();
            this.playlistListBox1 = new StreamtaggerSync.PlaylistListBox();
            this.menuStrip1.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.splitContainer1)).BeginInit();
            this.splitContainer1.Panel1.SuspendLayout();
            this.splitContainer1.Panel2.SuspendLayout();
            this.splitContainer1.SuspendLayout();
            this.gbPlaylists.SuspendLayout();
            this.gbSync.SuspendLayout();
            this.SuspendLayout();
            // 
            // menuStrip1
            // 
            this.menuStrip1.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.fileToolStripMenuItem});
            this.menuStrip1.Location = new System.Drawing.Point(0, 0);
            this.menuStrip1.Name = "menuStrip1";
            this.menuStrip1.Size = new System.Drawing.Size(1046, 24);
            this.menuStrip1.TabIndex = 0;
            this.menuStrip1.Text = "menuStrip1";
            // 
            // fileToolStripMenuItem
            // 
            this.fileToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.preferencesToolStripMenuItem,
            this.toolStripMenuItem1,
            this.exitToolStripMenuItem});
            this.fileToolStripMenuItem.Name = "fileToolStripMenuItem";
            this.fileToolStripMenuItem.Size = new System.Drawing.Size(37, 20);
            this.fileToolStripMenuItem.Text = "&File";
            // 
            // preferencesToolStripMenuItem
            // 
            this.preferencesToolStripMenuItem.Name = "preferencesToolStripMenuItem";
            this.preferencesToolStripMenuItem.Size = new System.Drawing.Size(135, 22);
            this.preferencesToolStripMenuItem.Text = "&Preferences";
            this.preferencesToolStripMenuItem.Click += new System.EventHandler(this.preferencesToolStripMenuItem_Click);
            // 
            // toolStripMenuItem1
            // 
            this.toolStripMenuItem1.Name = "toolStripMenuItem1";
            this.toolStripMenuItem1.Size = new System.Drawing.Size(132, 6);
            // 
            // exitToolStripMenuItem
            // 
            this.exitToolStripMenuItem.Name = "exitToolStripMenuItem";
            this.exitToolStripMenuItem.Size = new System.Drawing.Size(135, 22);
            this.exitToolStripMenuItem.Text = "E&xit";
            this.exitToolStripMenuItem.Click += new System.EventHandler(this.exitToolStripMenuItem_Click);
            // 
            // splitContainer1
            // 
            this.splitContainer1.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.splitContainer1.Location = new System.Drawing.Point(12, 27);
            this.splitContainer1.Name = "splitContainer1";
            // 
            // splitContainer1.Panel1
            // 
            this.splitContainer1.Panel1.Controls.Add(this.gbPlaylists);
            // 
            // splitContainer1.Panel2
            // 
            this.splitContainer1.Panel2.Controls.Add(this.gbSync);
            this.splitContainer1.Size = new System.Drawing.Size(1022, 532);
            this.splitContainer1.SplitterDistance = 487;
            this.splitContainer1.TabIndex = 2;
            // 
            // gbPlaylists
            // 
            this.gbPlaylists.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.gbPlaylists.Controls.Add(this.playlistListBox1);
            this.gbPlaylists.Location = new System.Drawing.Point(3, 3);
            this.gbPlaylists.Name = "gbPlaylists";
            this.gbPlaylists.Size = new System.Drawing.Size(481, 526);
            this.gbPlaylists.TabIndex = 2;
            this.gbPlaylists.TabStop = false;
            this.gbPlaylists.Text = "Playlists";
            // 
            // gbSync
            // 
            this.gbSync.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.gbSync.Controls.Add(this.cmdCopyLog);
            this.gbSync.Controls.Add(this.cmdSync);
            this.gbSync.Controls.Add(this.txtSyncLog);
            this.gbSync.Location = new System.Drawing.Point(3, 3);
            this.gbSync.Name = "gbSync";
            this.gbSync.Size = new System.Drawing.Size(525, 526);
            this.gbSync.TabIndex = 0;
            this.gbSync.TabStop = false;
            this.gbSync.Text = "Sync";
            // 
            // txtSyncLog
            // 
            this.txtSyncLog.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.txtSyncLog.Location = new System.Drawing.Point(6, 19);
            this.txtSyncLog.Multiline = true;
            this.txtSyncLog.Name = "txtSyncLog";
            this.txtSyncLog.ReadOnly = true;
            this.txtSyncLog.ScrollBars = System.Windows.Forms.ScrollBars.Vertical;
            this.txtSyncLog.Size = new System.Drawing.Size(513, 472);
            this.txtSyncLog.TabIndex = 0;
            // 
            // cmdSync
            // 
            this.cmdSync.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)));
            this.cmdSync.Location = new System.Drawing.Point(413, 497);
            this.cmdSync.Name = "cmdSync";
            this.cmdSync.Size = new System.Drawing.Size(106, 23);
            this.cmdSync.TabIndex = 1;
            this.cmdSync.Text = "Sync!";
            this.cmdSync.UseVisualStyleBackColor = true;
            this.cmdSync.Click += new System.EventHandler(this.cmdSync_Click);
            // 
            // cmdCopyLog
            // 
            this.cmdCopyLog.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left)));
            this.cmdCopyLog.Location = new System.Drawing.Point(6, 497);
            this.cmdCopyLog.Name = "cmdCopyLog";
            this.cmdCopyLog.Size = new System.Drawing.Size(75, 23);
            this.cmdCopyLog.TabIndex = 2;
            this.cmdCopyLog.Text = "Copy log";
            this.cmdCopyLog.UseVisualStyleBackColor = true;
            // 
            // playlistListBox1
            // 
            this.playlistListBox1.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.playlistListBox1.AutoScroll = true;
            this.playlistListBox1.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D;
            this.playlistListBox1.Location = new System.Drawing.Point(6, 19);
            this.playlistListBox1.Name = "playlistListBox1";
            this.playlistListBox1.Size = new System.Drawing.Size(469, 501);
            this.playlistListBox1.TabIndex = 0;
            this.playlistListBox1.PlaylistsChanged += new System.EventHandler(this.playlistListBox1_PlaylistsChanged);
            this.playlistListBox1.InformationRequested += new System.EventHandler<StreamtaggerSync.PlaylistControl.InformationRequestedEventArgs>(this.playlistListBox1_InformationRequested);
            // 
            // SyncForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1046, 571);
            this.Controls.Add(this.splitContainer1);
            this.Controls.Add(this.menuStrip1);
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.MainMenuStrip = this.menuStrip1;
            this.Name = "SyncForm";
            this.Text = "Streamtagger Sync";
            this.menuStrip1.ResumeLayout(false);
            this.menuStrip1.PerformLayout();
            this.splitContainer1.Panel1.ResumeLayout(false);
            this.splitContainer1.Panel2.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.splitContainer1)).EndInit();
            this.splitContainer1.ResumeLayout(false);
            this.gbPlaylists.ResumeLayout(false);
            this.gbSync.ResumeLayout(false);
            this.gbSync.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.MenuStrip menuStrip1;
        private System.Windows.Forms.ToolStripMenuItem fileToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem preferencesToolStripMenuItem;
        private System.Windows.Forms.ToolStripSeparator toolStripMenuItem1;
        private System.Windows.Forms.ToolStripMenuItem exitToolStripMenuItem;
        private System.Windows.Forms.SplitContainer splitContainer1;
        private System.Windows.Forms.GroupBox gbPlaylists;
        private PlaylistListBox playlistListBox1;
        private System.Windows.Forms.GroupBox gbSync;
        private System.Windows.Forms.Button cmdSync;
        private System.Windows.Forms.TextBox txtSyncLog;
        private System.Windows.Forms.Button cmdCopyLog;
    }
}

