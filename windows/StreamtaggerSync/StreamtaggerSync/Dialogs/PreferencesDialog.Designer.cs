namespace StreamtaggerSync
{
    partial class PreferencesDialog
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(PreferencesDialog));
            this.gbStorage = new System.Windows.Forms.GroupBox();
            this.cmdPlaylistsPath = new System.Windows.Forms.Button();
            this.lblPlaylistsPath = new System.Windows.Forms.Label();
            this.label4 = new System.Windows.Forms.Label();
            this.cmdMusicPath = new System.Windows.Forms.Button();
            this.lblMusicPath = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.gbCloud = new System.Windows.Forms.GroupBox();
            this.txtUsername = new System.Windows.Forms.TextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.txtStreamtaggerUrl = new System.Windows.Forms.TextBox();
            this.label1 = new System.Windows.Forms.Label();
            this.cmdOk = new System.Windows.Forms.Button();
            this.fbdMusicPath = new System.Windows.Forms.FolderBrowserDialog();
            this.fbdPlaylistsPath = new System.Windows.Forms.FolderBrowserDialog();
            this.lblInstructions = new System.Windows.Forms.Label();
            this.gbStorage.SuspendLayout();
            this.gbCloud.SuspendLayout();
            this.SuspendLayout();
            // 
            // gbStorage
            // 
            this.gbStorage.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.gbStorage.Controls.Add(this.cmdPlaylistsPath);
            this.gbStorage.Controls.Add(this.lblPlaylistsPath);
            this.gbStorage.Controls.Add(this.label4);
            this.gbStorage.Controls.Add(this.cmdMusicPath);
            this.gbStorage.Controls.Add(this.lblMusicPath);
            this.gbStorage.Controls.Add(this.label2);
            this.gbStorage.Location = new System.Drawing.Point(12, 96);
            this.gbStorage.Name = "gbStorage";
            this.gbStorage.Size = new System.Drawing.Size(580, 85);
            this.gbStorage.TabIndex = 0;
            this.gbStorage.TabStop = false;
            this.gbStorage.Text = "Local storage";
            // 
            // cmdPlaylistsPath
            // 
            this.cmdPlaylistsPath.BackgroundImage = global::StreamtaggerSync.Properties.Resources.folder_xxl;
            this.cmdPlaylistsPath.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch;
            this.cmdPlaylistsPath.Location = new System.Drawing.Point(110, 48);
            this.cmdPlaylistsPath.Name = "cmdPlaylistsPath";
            this.cmdPlaylistsPath.Size = new System.Drawing.Size(23, 23);
            this.cmdPlaylistsPath.TabIndex = 5;
            this.cmdPlaylistsPath.UseVisualStyleBackColor = true;
            this.cmdPlaylistsPath.Click += new System.EventHandler(this.cmdPlaylistsPath_Click);
            // 
            // lblPlaylistsPath
            // 
            this.lblPlaylistsPath.AutoSize = true;
            this.lblPlaylistsPath.Location = new System.Drawing.Point(139, 53);
            this.lblPlaylistsPath.Name = "lblPlaylistsPath";
            this.lblPlaylistsPath.Size = new System.Drawing.Size(25, 13);
            this.lblPlaylistsPath.TabIndex = 4;
            this.lblPlaylistsPath.Text = "???";
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(6, 53);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(71, 13);
            this.label4.TabIndex = 3;
            this.label4.Text = "Playlists path:";
            // 
            // cmdMusicPath
            // 
            this.cmdMusicPath.BackgroundImage = global::StreamtaggerSync.Properties.Resources.folder_xxl;
            this.cmdMusicPath.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch;
            this.cmdMusicPath.Location = new System.Drawing.Point(110, 19);
            this.cmdMusicPath.Name = "cmdMusicPath";
            this.cmdMusicPath.Size = new System.Drawing.Size(23, 23);
            this.cmdMusicPath.TabIndex = 2;
            this.cmdMusicPath.UseVisualStyleBackColor = true;
            this.cmdMusicPath.Click += new System.EventHandler(this.cmdMusicPath_Click);
            // 
            // lblMusicPath
            // 
            this.lblMusicPath.AutoSize = true;
            this.lblMusicPath.Location = new System.Drawing.Point(139, 24);
            this.lblMusicPath.Name = "lblMusicPath";
            this.lblMusicPath.Size = new System.Drawing.Size(25, 13);
            this.lblMusicPath.TabIndex = 1;
            this.lblMusicPath.Text = "???";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(6, 24);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(62, 13);
            this.label2.TabIndex = 0;
            this.label2.Text = "Music path:";
            // 
            // gbCloud
            // 
            this.gbCloud.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.gbCloud.Controls.Add(this.txtUsername);
            this.gbCloud.Controls.Add(this.label3);
            this.gbCloud.Controls.Add(this.txtStreamtaggerUrl);
            this.gbCloud.Controls.Add(this.label1);
            this.gbCloud.Location = new System.Drawing.Point(12, 12);
            this.gbCloud.Name = "gbCloud";
            this.gbCloud.Size = new System.Drawing.Size(580, 78);
            this.gbCloud.TabIndex = 1;
            this.gbCloud.TabStop = false;
            this.gbCloud.Text = "Cloud";
            // 
            // txtUsername
            // 
            this.txtUsername.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.txtUsername.Location = new System.Drawing.Point(110, 45);
            this.txtUsername.Name = "txtUsername";
            this.txtUsername.Size = new System.Drawing.Size(464, 20);
            this.txtUsername.TabIndex = 3;
            this.txtUsername.KeyPress += new System.Windows.Forms.KeyPressEventHandler(this.txt_KeyPress);
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(46, 48);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(58, 13);
            this.label3.TabIndex = 2;
            this.label3.Text = "Username:";
            // 
            // txtStreamtaggerUrl
            // 
            this.txtStreamtaggerUrl.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.txtStreamtaggerUrl.Location = new System.Drawing.Point(110, 19);
            this.txtStreamtaggerUrl.Name = "txtStreamtaggerUrl";
            this.txtStreamtaggerUrl.Size = new System.Drawing.Size(464, 20);
            this.txtStreamtaggerUrl.TabIndex = 1;
            this.txtStreamtaggerUrl.KeyPress += new System.Windows.Forms.KeyPressEventHandler(this.txt_KeyPress);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(6, 22);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(98, 13);
            this.label1.TabIndex = 0;
            this.label1.Text = "Streamtagger URL:";
            // 
            // cmdOk
            // 
            this.cmdOk.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)));
            this.cmdOk.Location = new System.Drawing.Point(517, 194);
            this.cmdOk.Name = "cmdOk";
            this.cmdOk.Size = new System.Drawing.Size(75, 23);
            this.cmdOk.TabIndex = 2;
            this.cmdOk.Text = "Ok";
            this.cmdOk.UseVisualStyleBackColor = true;
            this.cmdOk.Click += new System.EventHandler(this.cmdOk_Click);
            // 
            // lblInstructions
            // 
            this.lblInstructions.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left)));
            this.lblInstructions.AutoSize = true;
            this.lblInstructions.ForeColor = System.Drawing.Color.Red;
            this.lblInstructions.Location = new System.Drawing.Point(9, 204);
            this.lblInstructions.Name = "lblInstructions";
            this.lblInstructions.Size = new System.Drawing.Size(0, 13);
            this.lblInstructions.TabIndex = 3;
            // 
            // PreferencesDialog
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(604, 229);
            this.Controls.Add(this.lblInstructions);
            this.Controls.Add(this.cmdOk);
            this.Controls.Add(this.gbCloud);
            this.Controls.Add(this.gbStorage);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog;
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.Name = "PreferencesDialog";
            this.Text = "Preferences";
            this.gbStorage.ResumeLayout(false);
            this.gbStorage.PerformLayout();
            this.gbCloud.ResumeLayout(false);
            this.gbCloud.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.GroupBox gbStorage;
        private System.Windows.Forms.Label lblMusicPath;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.GroupBox gbCloud;
        private System.Windows.Forms.TextBox txtStreamtaggerUrl;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Button cmdPlaylistsPath;
        private System.Windows.Forms.Label lblPlaylistsPath;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Button cmdMusicPath;
        private System.Windows.Forms.Button cmdOk;
        private System.Windows.Forms.FolderBrowserDialog fbdMusicPath;
        private System.Windows.Forms.FolderBrowserDialog fbdPlaylistsPath;
        private System.Windows.Forms.TextBox txtUsername;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Label lblInstructions;
    }
}