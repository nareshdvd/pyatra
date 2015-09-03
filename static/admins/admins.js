$(document).on("click", ".add-new-variation", function(){
  var $new_panel = $(".main-template-panel").clone();
  var next_panel_index = $(".template-panel").length;
  $new_panel.addClass("latest-panel").removeClass("main-template-panel");
  $new_panel.find("input, textarea, select, radio, checkbox").each(function(){
    if($(this).hasClass("required-in-variation")){
      var old_name = $(this).attr("name");
      var new_name = next_panel_index + "_" + old_name;
      $(this).attr("name", new_name);
    }
    else{
      if($(this).attr("type") == "hidden"){
        $(this).remove();
      }
      else{
        $(this).closest(".form-group").remove();
      }

    }
    if($(this).hasClass("has-error")){
      $(this).parent().find(".error").remove()
    }
    $(this).val("")
  });

  $new_panel.find("input[name='main_variation']").val("False");
  $(".main-template-panel").closest("form").find(".save-btn").before($new_panel);
  if($(".main-template-panel").closest("form").find(".input-extra_variation_count").length == 0){
    $(".main-template-panel").closest("form").append("<input type='hidden' name='extra_variation_count' value='" + next_panel_index + "'/>");
  }
  else{
    $(".main-template-panel").closest("form").find(".input-extra_variation_count").val(next_panel_index);
  }
});


$(document).on("submit", ".new-templates-form", function(e){
  e.preventDefault();
  e.stopPropagation();
  var $form = $(this);
  var form_data = new FormData();
  $form.find('input, textarea, select, radio, checkbox').each(function(){
    var $input = $(this);
    if($input.attr("type") == "file"){
      var file = this.files[0];
      form_data.append($input.attr('name'), file);
    }
    else{
      form_data.append($input.attr('name'), $input.val())
    }
    if($input.hasClass('has-error')){
      $input.parent().find(".error").remove();
    }
  });
  $.ajax({
    url: $form.attr('action'),
    data: form_data,
    type: 'post',
    cache: false,
    dataType: 'json',
    processData: false, // Don't process the files
    contentType: false,
    success: function(retdata){
      if(retdata.status == 'error'){
        errors = retdata.errors
        $.each(errors, function(){
          var variation = this;
          $.each(this, function(k,v){
            var input_types = ['input', 'textarea', 'select', 'radio', 'checkbox']
            $.each(input_types, function(){
              var input_type = this;
              if($(input_type + '[name="' + k + '"]').length == 1){
                if($(input_type + '[name="' + k + '"]').parent().find(".error").length == 0){
                  $(input_type + '[name="' + k + '"]').parent().append('<span class="error">' + v + '</span>');
                }
                else{
                  $(input_type + '[name="' + k + '"]').parent().find(".error").html(v);
                }
                $(input_type + '[name="' + k + '"]').addClass('has-error');
              }
            });
          });
        });
      }
      else{
        window.location.href = '/admins/video_templates'
      }
    }
  })
});