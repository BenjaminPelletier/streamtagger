# Streamtagger system

## Bringing up a system

### Database
Streamtagger uses a PostgreSQL database.  By default, `start_db.sh` will create or restart a database that stores its data in `${PWD}/storage/db`, a folder which must already exist when `start_db.sh` is run.  In Linux, a symbolic link can be used to actually store the data elsewhere.

By default, a weak default password is used under the assumption that the database will not be externally accessible; this can be changed in `start_db.sh`, and a matching change must then be made to `start_ui.sh`.

### User interface
The streamtagger UI can be started from existing docker images using `start_ui.sh`, but it will probably be more common to use `rebuild_ui.sh` which rebuilds the docker images before starting or restarting the UI with the new images, initially following the UI logs (though log-following can be exited without killing the docker container).  The UI hosts an HTTP endpoint on port 5000, so can be viewed at http://localhost:5000 when the UI is running.

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
* Create a run configuration pointing to `ui/streamtagger.py` with these environment variables (set to the appropriate values) and a working directory of streamtagger/ui:
  * ST_MEDIA_PATH=/path/to/your/media/folder
  * ST_DB_CONNECTIONSTRING=postgresql://streamtagger:mysecretpassword@db.host.name/streamtagger
  * ST_SECRET_KEY=a random string probably produced by make_secret_key.sh
