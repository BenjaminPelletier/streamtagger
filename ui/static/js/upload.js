upload_filenames_by_id = {}


$(function(){
  $('#drag-and-drop-zone').dmUploader({ //
    url: 'upload',
    maxFileSize: 20000000, // 20 Megs
    onDragEnter: function() {
      // Happens when dragging something over the DnD area
      this.addClass('active');
    },
    onDragLeave: function() {
      // Happens when dragging something OUT of the DnD area
      this.removeClass('active');
    },
    onInit: function() {
      // Plugin is ready to use
      ui_add_log('Plugin initialized', 'info');
    },
    onComplete: function() {
      // All files in the queue are processed (success or error)
      ui_add_log('All pending tranfers finished');
    },
    onNewFile: function(id, file) {
      // When a new file is added using the file selector or the DnD area
      upload_filenames_by_id[id] = file.name
      ui_add_log('Added new upload ' + file.name);
      ui_multi_add_file(id, file);
    },
    onBeforeUpload: function(id) {
      // about tho start uploading a file
      ui_add_log('Started uploading ' + upload_filenames_by_id[id]);
      ui_multi_update_file_status(id, 'uploading', 'Uploading...');
      ui_multi_update_file_progress(id, 0, '', true);
    },
    onUploadCanceled: function(id) {
      // Happens when a file is directly canceled by the user.
      ui_add_log('User canceled upload of ' + upload_filenames_by_id[id]);
      ui_multi_update_file_status(id, 'warning', 'Canceled by User');
      ui_multi_update_file_progress(id, 0, 'warning', false);
    },
    onUploadProgress: function(id, percent) {
      // Updating file progress
      ui_multi_update_file_progress(id, percent);
    },
    onUploadSuccess: function(id, data) {
      if (data.status == 'ok') {
        // A file was successfully uploaded
        ui_add_log('Successfully uploaded ' + upload_filenames_by_id[id] + ': ' + JSON.stringify(data));
        ui_multi_update_file_status(id, 'success', 'Upload Complete');
        ui_multi_update_file_progress(id, 100, 'success', false);
      } else {
        ui_add_log('Unexpected response uploading ' + upload_filenames_by_id[id] + ': ' + JSON.stringify(data));
        ui_multi_update_file_status(id, 'danger', message);
        ui_multi_update_file_progress(id, 0, 'danger', false);
      }
    },
    onUploadError: function(id, xhr, status, message) {
      if (xhr.hasOwnProperty('responseJSON') && 'message' in xhr.responseJSON) {
        var message = xhr.responseJSON['message'];
      } else {
        var message = xhr.responseText.replace(/<[^>]*>?/gm, '');
      }
      ui_add_log('Server ' + status + ' uploading file ' + upload_filenames_by_id[id] + ': ' + message);
      ui_multi_update_file_status(id, 'danger', message);
      ui_multi_update_file_progress(id, 0, 'danger', false);
    },
    onFallbackMode: function() {
      // When the browser doesn't support this plugin :(
      ui_add_log('Plugin cant be used here, running Fallback callback', 'danger');
    },
    onFileSizeError: function(file) {
      ui_add_log('File \'' + file.name + '\' cannot be added: size excess limit', 'danger');
    }
  });
});


// Adds an entry to our debug area
function ui_add_log(message, color)
{
  var d = new Date();

  var dateString = (('0' + d.getHours())).slice(-2) + ':' +
    (('0' + d.getMinutes())).slice(-2) + ':' +
    (('0' + d.getSeconds())).slice(-2);

  color = (typeof color === 'undefined' ? 'muted' : color);

  var template = $('#debug-template').text();
  template = template.replace('%%date%%', dateString);
  template = template.replace('%%message%%', message);
  template = template.replace('%%color%%', color);

  $('#debug').find('li.empty').fadeOut(); // remove the 'no messages yet'
  $('#debug').prepend(template);
}

// Creates a new file and add it to our list
function ui_multi_add_file(id, file)
{
  var template = $('#files-template').text();
  template = template.replace('%%filename%%', file.name);

  template = $(template);
  template.prop('id', 'uploaderFile' + id);
  template.data('file-id', id);

  $('#files').find('li.empty').fadeOut(); // remove the 'no files yet'
  $('#files').prepend(template);
}

// Changes the status messages on our list
function ui_multi_update_file_status(id, status, message)
{
  $('#uploaderFile' + id).find('span').html(message).prop('class', 'status text-' + status);
}

// Updates a file progress, depending on the parameters it may animate it or change the color.
function ui_multi_update_file_progress(id, percent, color, active)
{
  color = (typeof color === 'undefined' ? false : color);
  active = (typeof active === 'undefined' ? true : active);

  var bar = $('#uploaderFile' + id).find('div.progress-bar');

  bar.width(percent + '%').attr('aria-valuenow', percent);
  bar.toggleClass('progress-bar-striped progress-bar-animated', active);

  if (percent === 0){
    bar.html('');
  } else {
    bar.html(percent + '%');
  }

  if (color !== false){
    bar.removeClass('bg-success bg-info bg-warning bg-danger');
    bar.addClass('bg-' + color);
  }
}
