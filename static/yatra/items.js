/* CSRF addition to ajax post requests */
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
/* END CSRF addition to ajax post requests */



$(document).on("change", ".image-container input[type=\"file\"]", function(){
  var $file_input = $(this);
  var $image_container = $(this).closest('.image-container');
  if(is_file_selected_an_image($file_input)){
    save_file($file_input);
  }
  else{
    alert("Not an image file");
  }
});

function is_file_selected_an_image($file_input){
  var file_name = $file_input.val()
  return file_name.endsWith("jpg") || file_name.endsWith("jpeg")
  // for file validations, will use it later
  // var file = this.files[0];
  // var name = file.name;
  // var size = file.size;
  // var type = file.type;
}

function save_file($file_input){
  var $form = $file_input.closest("form");
  var form = $form[0]
  var form_data = new FormData($form[0])
  // console.log(form_data)
  $.ajax({
    url: '/yatra/items/save',
    type: 'post',
    data: form_data,
    cache: false,
    contentType: false,
    processData: false,
    success: function(retdata){
      console.log($form.closest(".item-box"));
      console.log(retdata)
      $form.closest(".item-box").html(retdata);
    }
  });
  $file_input.data("itemselected", "true");
}