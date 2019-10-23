$(document).ready(function() {
    $( "#dialog-confirm-delete-song" ).hide();

    $(".moment-relative").each(function() {
        $(this).text(moment($(this).text()).fromNow());
    });

    $('#audio').on('ended', function() {
        play_next_song(1);
    });

    $('#file_input').change(function(event) {
        for (var i = 0; i < fileInput.files.length; i++) {
    	    fileList.push(fileInput.files[i]);
        }
    });
} );

var playing_song_id = null;

// Get the <button> element that will play song with specified id
function get_play_song_button_by_id(id) {
    return $("tr[data-songid='" + id + "'] .song_button")[0];
}

// Click on play/pause/resume <button> element button
function play_song(button) {
    var row = button.closest('tr');
    var path = row.getAttribute('data-path');
    var song_id = row.getAttribute('data-songid');
    var audio = $('#audio')[0];

    var button_classes = button.classList;
    if (button_classes.contains("play_song_button")) {
        // Song controlled by button was not playing
        if (playing_song_id != null) {
            // Reset button for song that was previously playing
            var old_button_classes = get_play_song_button_by_id(playing_song_id).classList;
            old_button_classes.remove("pause_song_button");
            old_button_classes.remove("resume_song_button");
            old_button_classes.add("play_song_button");
        }

        button_classes.remove("play_song_button");
        button_classes.add("pause_song_button");
        var source = document.getElementById('audio_source');
        source.src = path;
        playing_song_id = song_id;

        audio.load();
        audio.play();
    } else if (button_classes.contains("pause_song_button")) {
        // Song controlled by button was playing
        button_classes.remove("pause_song_button");
        button_classes.add("resume_song_button");

        audio.pause();
    } else if (button_classes.contains("resume_song_button")) {
        // Song controlled by button was paused
        button_classes.remove("resume_song_button");
        button_classes.add("pause_song_button");

        audio.play();
    }
}

function play_next_song(index_delta) {
    // Get the current ordered list of song_ids from table
    var song_ids = $(".song_button").map(function() {
        return this.closest('tr').getAttribute('data-songid');
    }).get();

    var index = song_ids.indexOf(playing_song_id);
    if (index < 0) {
        // Nothing seems to be playing right now; play the first song
        play_song($('.song_button').first()[0]);
    } else {
        // Move index by index_delta then play the song at that location in the table
        var song_id = song_ids[(index + song_ids.length + index_delta) % song_ids.length];
        play_song(get_play_song_button_by_id(song_id));
    }
}

function delete_song(song_id) {
    $( "#dialog-confirm-delete-song" ).dialog({
        resizable: false,
        height: "auto",
        width: 400,
        modal: true,
        buttons: {
            "Delete all items": function() {
                $( this ).dialog( "close" );
            },
            Cancel: function() {
                $( this ).dialog( "close" );
            }
        },
        open: function() {
            $(this).siblings('.ui-dialog-buttonpane').find('button:eq(1)').focus();
        }
    });
}