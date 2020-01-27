namespace StreamtaggerSync
{
    partial class PlaylistControl
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
            this.label1 = new System.Windows.Forms.Label();
            this.txtName = new System.Windows.Forms.TextBox();
            this.txtQuery = new System.Windows.Forms.TextBox();
            this.cmdDelete = new System.Windows.Forms.Button();
            this.llQuery = new System.Windows.Forms.LinkLabel();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(3, 6);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(38, 13);
            this.label1.TabIndex = 0;
            this.label1.Text = "Name:";
            // 
            // txtName
            // 
            this.txtName.Location = new System.Drawing.Point(47, 3);
            this.txtName.Name = "txtName";
            this.txtName.Size = new System.Drawing.Size(111, 20);
            this.txtName.TabIndex = 1;
            this.txtName.Leave += new System.EventHandler(this.txtName_Leave);
            // 
            // txtQuery
            // 
            this.txtQuery.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.txtQuery.Location = new System.Drawing.Point(208, 3);
            this.txtQuery.Name = "txtQuery";
            this.txtQuery.Size = new System.Drawing.Size(209, 20);
            this.txtQuery.TabIndex = 3;
            this.txtQuery.Leave += new System.EventHandler(this.txtQuery_Leave);
            // 
            // cmdDelete
            // 
            this.cmdDelete.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.cmdDelete.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(225)))), ((int)(((byte)(192)))), ((int)(((byte)(192)))));
            this.cmdDelete.Location = new System.Drawing.Point(423, 1);
            this.cmdDelete.Name = "cmdDelete";
            this.cmdDelete.Size = new System.Drawing.Size(23, 23);
            this.cmdDelete.TabIndex = 4;
            this.cmdDelete.Text = "-";
            this.cmdDelete.UseVisualStyleBackColor = false;
            this.cmdDelete.Click += new System.EventHandler(this.cmdDelete_Click);
            // 
            // llQuery
            // 
            this.llQuery.AutoSize = true;
            this.llQuery.Location = new System.Drawing.Point(164, 6);
            this.llQuery.Name = "llQuery";
            this.llQuery.Size = new System.Drawing.Size(38, 13);
            this.llQuery.TabIndex = 5;
            this.llQuery.TabStop = true;
            this.llQuery.Text = "Query:";
            this.llQuery.LinkClicked += new System.Windows.Forms.LinkLabelLinkClickedEventHandler(this.llQuery_LinkClicked);
            // 
            // PlaylistControl
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.Controls.Add(this.llQuery);
            this.Controls.Add(this.cmdDelete);
            this.Controls.Add(this.txtQuery);
            this.Controls.Add(this.txtName);
            this.Controls.Add(this.label1);
            this.Name = "PlaylistControl";
            this.Size = new System.Drawing.Size(450, 26);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.TextBox txtName;
        private System.Windows.Forms.TextBox txtQuery;
        private System.Windows.Forms.Button cmdDelete;
        private System.Windows.Forms.LinkLabel llQuery;
    }
}
