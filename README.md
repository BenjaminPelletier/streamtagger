## Introduction
streamtagger is a self-hosted cloud music player and associated utilities focused on sharing music and ideas about music with trusted friends.  The main viewer is a Python-Flask app which stores music files on the local file system, and stores site information and cached music metadata in a PostgreSQL database.

On the back end, streamtagger attempts to store information about a particular music file in the file itself, generally in ID3v2 tags.  This functionality is currently not fully working (see issue #4), but when it does, it should be possible to almost fully reconstitute a streamtagger site (including database) with just the folders of music files along with new passwords for each user.

To bring up your own system, see [the system documentation](system/README.md).

## Web UI

### Songs
The root page displays and enables playing and/or editing tags of all music.  A particular song or songs by an artist can be found at `/songs/<partial name of song or artist>`, or a specific song can be found at `/songs/<partial artist name>/<partial song name>`.

### Tags
Song tags are at the heart of streamtagger; they enable users to attach useful information to songs and then later view, sort, and filter via that information.

#### Showing
A list of all defined tags can be found at `/tags` and the values for those tags can be displayed on most song-listing pages by using the `show` URL parameter, separating multiple tags by commas (e.g., `http://localhost:5000?show=letsdance,latenight`).  Because tag values are per-user, the tag value given by a specific user can be viewed (and edited, if the user is logged in) by prefacing the tag with `username@`; e.g., `http://localhost:5000?show=ben@letsdance,lucy@latenight`.

#### Filtering / queries
To limit songs displayed to only ones with certain tags, use the `hastag` URL parameter in this form: `?hastag=[username@]tag1name[=tag1value]`.  So, for instance, to see songs that anyone has tagged with any value in the "letsdance" tag, `?hastag=letsdance`.  To see only songs that are rated a 5 for the "letsdance" tag, `?hastag=letsdance=5`.  To see only songs that ben has rated a 5 for the "letsdance" tag, `?hastag=ben@letsdance=5`.

To match any one of multiple conditions, append additional conditions with a `|` character.  For instance, to see only songs that have some value for "justlisten" or a value of 5 for "latenight", `?hastag=justlisten|latenight=5`.  To match every one of multiple conditions, add additional conditions with additional `hastag` parameters.  For instance, to see only songs that are rated a 5 for "letsdance" and a 5 for "latenight", `?hastag=letsdance=5&hastag=latenight=5`.

#### Uploading
The upload form can be found under the + menu on the root page.  Currently, only MP3 and unprotected M4A files are supported, and M4As will be converted to MP3s before long-term storage.

### Users
Additional users can only be added by the admin user at `/users/admin`.  Upon first-time UI execution, an admin user will be automatically created by the UI and the password will be stored in a file in the UI container.  This password can be printed to the console with [`print_admin_password.sh`](system/print_admin_password.sh), but it will disappear when that container is destroyed.  If this password is lost, the password hash can be manually set directly in the database through [adminer](system/db_adminer.sh).  The algorithm to compute the hash can be found in [login.js](ui/app/static/js/login.js) and can be executed using [an online SHA1 calculator](https://www.miraclesalad.com/webtools/sha1.php) by manually constructing the string to encode.  For instance, for username "ben" and password "notsecure", the text to hash would be `K80Tgi^w1&jcbennotsecureK80Tgi^w1&jcben` and the resulting hash should be `d3c477fa4eb121d839c9e499f7ec770ff77ce458`.

## Windows sync tool
[StreamtaggerSync](windows/StreamtaggerSync/StreamtaggerSync.exe) is [a simple .NET application](windows/StreamtaggerSync) that automatically synchronizes a set of music from streamtagger to a local computer, and also creates playlists according to specified filters/queries.
 