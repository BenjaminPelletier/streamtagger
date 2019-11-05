# Streamtagger system

## Developing on an external host

### Linux
To develop the UI using the database and media storage on an external host:
* [Set up an SSH mount](https://askubuntu.com/questions/412477/mount-remote-directory-using-ssh) to /streamtagger/system/storage/media
* `sshfs user@host:/remote_directory /local_directory`
* `sudo chown -R $USER media`

### Windows
* Install [WinFsp](https://github.com/billziss-gh/winfsp/releases)
* Install [SSHFS-Win](https://github.com/billziss-gh/sshfs-win/releases)
* Open File Explorer, right-click on Computer and choose Map network drive. Choose a drive to mount at and in the Folder field enter `\\sshfs\remoteusername@remotehostname

### Both
* Install the Python packages specified in `Dockerfile_template`
* Create a run configuration pointing to `ui/streamtagger.py` with these environment variables:
  * ST_MEDIA_PATH=/path/to/your/media/folder
  * ST_DB_CONNECTIONSTRING="host=myhost port=5432 dbname=streamtagger user=streamtagger password=mysecretpassword"
