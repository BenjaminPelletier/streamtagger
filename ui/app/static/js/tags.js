$(document).ready(function() {
    $('#new_tagdef_info').submit(click_add_tag);
});


function click_add_tag(event) {
    $.post('/tags', $('#new_tagdef_info').serialize())
        .done(function( data ) {
            // Tagdef created successfully
            location.reload(); //TODO: just insert new tagdef in table instead of doing full reload
        })
        .fail(function(jqXHR, textStatus, error) {
            // Failed to create tagdef
            alert('Error creating tag: ' + error + '\n' + jqXHR.responseText);
        });
    event.preventDefault();
}
