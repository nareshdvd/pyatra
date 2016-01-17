
var applied_steakers = [], applied_texts = [];
function apply_steakers(){
  $.each(applied_steakers, function(){
    var steaker = this;
    apply_steaker_to_original_image(steaker);
  });
  $.each(applied_texts, function(){
    var text = this;
    apply_text_to_original_image(text)
  });
}


$(document).on("click", "#steaker-tab", function(){
  // var ctx = document.getElementById("temp-image-canvas").getContext("2d");
  // var steaker_url = '/static/yatra/images/steaker_01.png'
  // var steaker = new Image();
  // steaker.onload = function(){
  //   ctx.drawImage(steaker, 10, 0);
  // }
  // steaker.src = steaker_url;
});

$(document).on("click", ".steaker-sample", function(){
  var $this= $(this);
  $("#fake_img").remove();
  var img_src = $this.attr("src");
  var fake_img = new Image();
  fake_img.src=img_src;
  $("#temp-image-canvas").after(fake_img);
  var $fake_img = $(fake_img);
  $fake_img.attr("id", "fake_img");
  $fake_img.attr("style", "position: absolute; top: 10px; left: 10px;")
  $fake_img.draggable({
    containment: "#temp-image-canvas"
  });
});

$(document).on("click", "#add-steaker-btn", function(){
  var $fake_img = $("#fake_img");
  if($fake_img.length != 0){
    var top = parseInt($fake_img.css("top"));
    var left = parseInt($fake_img.css("left"));
    var ctx = document.getElementById("temp-image-canvas").getContext("2d");
    console.log(fake_img);
    ctx.drawImage(fake_img, left-15, top);
    applied_steakers.push({'steaker' : $fake_img.attr('src'), 'top' : top, 'left' : (left - 15)});
  }
});

function apply_steaker_to_original_image(applied_steaker_arr){
  var ctx = document.getElementById("original-image-canvas").getContext("2d");
  var $fake_img = $("#fake_img");
  var top = applied_steaker_arr['top'];
  var left = applied_steaker_arr['left'];
  ctx.drawImage(fake_img, left, top);
}

$(document).on("keyup", "#steaker-text", function(){
  var $fake_text;
  if($("#fake_text").length == 0){
    var $fake_text = $("<div id='fake_text'></div>");
    $fake_text.attr("style", "position: absolute; top: 10px; left: 10px;");
    $("#temp-image-canvas").after($fake_text);
  }
  else{
    $fake_text = $("#fake_text");
  }
  $fake_text.html($(this).val());
  $fake_text.draggable({
    containment: "#temp-image-canvas"
  });
});
$(document).on("click", "#add-steaker-text", function(){
  convert_text_to_image($("#fake_text"));
});
function convert_text_to_image($div){
  var txt = $div.html();
  var ctx = document.getElementById("temp-image-canvas").getContext("2d");

  ctx.font = '20px VideoJS';
  var top = parseInt($div.css("top"));
  var left = parseInt($div.css("left"));
  ctx.fillText(txt, left-15, top+19);
  applied_texts.push({'text' : txt, 'top' : top+19, 'left' : left-15});
}

function apply_text_to_original_image(applied_text_arr){
  var ctx = document.getElementById("original-image-canvas").getContext("2d");
  ctx.font = '20px VideoJS';
  var top = applied_text_arr['top'];
  var left = applied_text_arr['left'];
  ctx.fillText(applied_text_arr['text'], left, top);
}

$(document).on("change", "#group-pics", function(){
  var $this = $(this);
  var files = $this[0].files;
  var formdata = new FormData();
  $.each(files, function(item_number){
    var file = this;
    if(file.type == "image/jpeg"){
      formdata.append('files['+item_number+'][file_type]', 'image');
      formdata.append('files['+item_number+'][file_number]', item_number)
      formdata.append('files['+item_number+'][file]', file);
    }
  });
  $.ajax({
    url: '/yatra/items/upload_many',
    type: 'post',
    data: formdata,
    cache: false,
    dataType: 'json',
    processData: false,
    contentType: false,
    success: function(retdata){
      console.log(retdata)
    }
  });

});

$(document).on("click", ".view-edit-item", function(){
  var $this = $(this);
  var item_number = $this.data("itemnumber");
  var item_type = $this.data("itemtype");
  if(item_type == "image"){
    var $item_image_div = $this.closest('.item-image-div')
    $.ajax({
      url: "/yatra/items/" + item_number + "/edit",
      data: '',
      type: 'get',
      success: function(retdata){
        $('body').append(retdata);
        $('.modal').modal('show');
        $('.modal').find('#apply_changes').data('item_image_div', $item_image_div)
        if($(".filter-image-canvas").length != 0){
          add_slider_filter_handlers();
          add_slider_preset_handlers();
          Caman(".filter-image-canvas", function(){
            this.render();
          });
        }
      }
    });
  }
  else{
    // if item_type is video then do following
    var $item_video_div = $this.closest('.item-video-div')
    $.ajax({
      url: "/yatra/items/" + item_number + "/edit",
      data: '',
      type: 'get',
      success: function(retdata){
        $('body').append(retdata);
        $('.modal').modal('show');
        $('.modal').find('#apply_changes').data('item_video_div', $item_video_div);
          $("video#id_edit_video").each(function(){
            var $video = $(this);
            $video[0].load();
            $video[0].pause();
            var popcorn = Popcorn("#id_edit_video");
            var duration = 0;

            popcorn.on('timeupdate', function(){
              var this_popcorn = this;
              var $curr_slider = $("#cutter-slider")
              var curr_range = $curr_slider.slider("values");
              var last = curr_range[1];
              if(this_popcorn.currentTime() >= last){
                popcorn.pause();
              }
            });
            popcorn.on('loadedmetadata', function() {
              var this_popcorn = this;
              duration = parseInt(this_popcorn.duration())
              var diff = 3;
              $("#cutter-slider").slider({
                range: true,
                values: [0,diff],
                animate: "fast",
                min: 0,
                max: duration,
                slide: function( event, ui ) {
                  var $target = $(event.target);
                  var val_1 = ui.values[0];
                  var val_2 = ui.values[1];
                  if($target.data("val_1") == undefined){
                    $target.data("val_1", val_1);
                  }
                  if($target.data("val_2") == undefined){
                    $target.data("val_2", val_2);
                  }
                  if($target.data("val_1") != val_1){
                    val_2 = val_1 + diff;
                  }
                  else{
                    if($target.data("val_2") != val_2){
                      val_1 = val_2 - diff;
                    }
                  }
                  if(((ui.values[1] == duration) && ((ui.values[1] - ui.values[0]) < diff)) || (ui.values[0] == 0 && ((ui.values[1] - ui.values[0]) < diff))){
                    console.log('i m here')
                    $target.slider("values", [parseInt($target.data("val_1")), parseInt($target.data("val_2"))]);
                  }
                  else{
                    $target.data("val_1", val_1);
                    $target.data("val_2", val_2);
                    console.log("val_1 " + val_1);
                    console.log("val_2 " + val_2);
                    this_popcorn.currentTime(val_1)
                    $target.slider("values", [val_1, val_2] );
                  }
                }
              });
            });
          });
      }
    });
  }
});

$(document).on('hidden.bs.modal', '#image-edit-modal', function (e) {
  $(this).remove();
})


$(document).on("change", ".item-upload-input", function(){
  var $this = $(this);
  var required_file_type = $this.data("filetype");
  var item_number = $this.data("itemnumber");
  var files = $this[0].files;
  var file = files[0];
  var formdata = new FormData();
  if(required_file_type == "image"){
    if(file.type == "image/jpeg"){
      formdata.append('file_type', 'image');
      formdata.append('file_number', item_number)
      $.each(files, function(key, value){
        formdata.append('file', value);
      });
    }
  }
  else{
    if(required_file_type == "video"){
      if(file.type == "video/mp4"){
        formdata.append('file_type', 'video');
        formdata.append('file_number', item_number)
        $.each(files, function(key, value){
          formdata.append('file', value);
        });
      }
    }
  }
  $.ajax({
    url: '/yatra/items/' + item_number + "/upload",
    type: 'post',
    data: formdata,
    cache: false,
    dataType: 'json',
    processData: false,
    contentType: false,
    success: function(retdata){
      if(retdata.status == "success"){
        if(required_file_type == "image"){
          $this.closest(".item-image-div").find(".item-img").attr("src", retdata.attachment_url + "?ts=" + get_timestamp());
          // $this.closest(".item-image-div").css("background-image", "url('" + retdata.attachment_url + "?ts=" + get_timestamp() + "')");
        }
        else{
          $this.closest(".item-video-div").find('video').find("source[type='video/mp4']").attr('src', retdata.attachment_url + "?ts=" + get_timestamp());
          // console.log($this.closest(".item-video-div").find('video').find("source[type='video/mp4']").attr('src'));
          $this.closest(".item-video-div").find('video')[0].load();
        }
      }
    }
  })
});

function get_timestamp(){
  return new Date().getTime();
}





var applied_filters = [];
var applied_preset = null;
function filter_handler(event, ui){
  $("#apply_changes").html("Save");
  var $slider_ele = $(event.target);
  var value = ui.value;
  var filter_name = $slider_ele.data("filter");
  Caman(".filter-image-canvas", function () {
    this.revert();
    update_applied_filters(filter_name, value)
    apply_filters(this);
    this.render();
  });
}
function apply_filter(filter_ele, func_name, value){
  filter_ele[func_name](value)
  return filter_ele
}

function update_applied_filters(func_name, value){
  filter_updated = false
  $.each(applied_filters, function(i){
    if(this.func_name == func_name){
      filter_updated = true;
      applied_filters[i].value = value;
    }
  });
  if(filter_updated == false){
    applied_filters.push({
      'func_name' : func_name,
      'value' : value
    })
  }
}

function apply_filters(filter_ele){
  var func_name;
  var value;
  applied_preset = null;
  for(var i=0;i< applied_filters.length; i++){
    func_name = applied_filters[i]['func_name'];
    value = applied_filters[i]['value'];
    apply_filter(filter_ele, func_name, value);
  }
}

function apply_preset(filter_ele){
  $("#apply_changes").html("Save");
  applied_filters = [];
  filter_ele[applied_preset]()
}

function apply_filters_on_original_image_and_save($save_btn){
  var itemnumber = $save_btn.data("itemnumber");
  var $item_image_div = $save_btn.data('item_image_div');
  if($save_btn.data("curraction") == "filter"){
    Caman("#original-image-canvas", function () {
      this.revert();
      if(applied_filters.length != 0){
        apply_filters(this);
      }
      else{
        if(applied_preset != null){
          apply_preset(this);
        }
      }
      this.render(function () {
        var attachment = this.toBase64('jpeg').replace('data:image/jpeg;base64,', '').replace(' ', '+');
        $.ajax({
          url: '/yatra/items/' + itemnumber + "/save_modified",
          type: 'post',
          data: {'attachment' : attachment},
          success: function(retdata){
            // console.log(retdata);
            // $item_image_div.css("background-image", "url('" + retdata.attachment_url + "?ts=" + get_timestamp() + "')");
            $item_image_div.find(".item-img").attr("src", retdata.attachment_url + "?ts=" + get_timestamp());
            // console.log($item_image_div.css('background-image').replace('url("', '').replace('")', '').replace("url('", "").replace("')", ""))
            $save_btn.html("saved");
          }
        });
      });
    });
  }
  else{
    if($save_btn.data("curraction") == "crop"){
      var cropped_data = $(".filter-image-original").cropper("getData");
      console.log(cropped_data);
      $.ajax({
        url: '/yatra/items/' + itemnumber + '/save_cropped_image',
        data: cropped_data,
        type: 'post',
        success: function(retdata){
          // console.log(retdata);
          // $item_image_div.css("background-image", "url('" + retdata.attachment_url + "?ts=" + get_timestamp() + "')");
          $item_image_div.find(".item-img").attr("src", retdata.attachment_url + "?ts=" + get_timestamp());
          // console.log($item_image_div.css('background-image').replace('url("', '').replace('")', '').replace("url('", "").replace("')", ""))
          $save_btn.html("saved");
        }
      });
    }
    else{
      if($save_btn.data("curraction") == "steaker"){
        // apply_steakers();
        Caman("#original-image-canvas", function () {
          $.each(applied_steakers, function(){
            var steaker = this;
            apply_steaker_to_original_image(steaker);
          });
          $.each(applied_texts, function(){
            var text = this;
            apply_text_to_original_image(text)
          });
          this.render(function () {
          var attachment = this.toBase64('jpeg').replace('data:image/jpeg;base64,', '').replace(' ', '+');
          $.ajax({
            url: '/yatra/items/' + itemnumber + "/save_modified",
            type: 'post',
            data: {'attachment' : attachment},
            success: function(retdata){
              // console.log(retdata);
              // $item_image_div.css("background-image", "url('" + retdata.attachment_url + "?ts=" + get_timestamp() + "')");
              $item_image_div.find(".item-img").attr("src", retdata.attachment_url + "?ts=" + get_timestamp());
              // console.log($item_image_div.css('background-image').replace('url("', '').replace('")', '').replace("url('", "").replace("')", ""))
              $save_btn.html("saved");
            }
          });
        });
        });
      }
    }
  }
}

$(document).on("click", "#apply_changes", function(){
  var $this = $(this);
  var htm = $this.html();
  $this.html("Saving...");
  var filetype = $this.data("itemtype");
  if(filetype == "image"){
    apply_filters_on_original_image_and_save($this);
  }
  else{
    save_modified_video($this);
  }
});

$(document).on("click", "#render", function(){
  var $this = $(this);
  var url = $this.data("href");
  $.ajax({
    url: url,
    data: {},
    type: 'get',
    success: function(retdata){
      $(".progress-row").show();
    }
  });
});

function save_modified_video($save_btn){
  console.log($("#cutter-slider").slider("values"));
  var values = $("#cutter-slider").slider("values");
  var itemnumber = $save_btn.data("itemnumber");
  $.ajax({
    url: '/yatra/items/' + itemnumber + '/save_cropped_video',
    data: {'vid_start' : values[0], 'vid_end' : values[1]},
    type: 'post',
    success: function(retdata){
      console.log(retdata)
    }
  });
}


function add_slider_filter_handlers(){
  $(".slider-filter").each(function(){
    var $this = $(this);
    var min = parseInt($this.data("min"));
    var max = parseInt($this.data("max"));
    var filterFunc = filter_handler;
    $this.slider({
      animate: "fast",
      min: min,
      max: max,
      stop: filterFunc
    });
  });
}

function add_slider_preset_handlers(){
  $('.preset-filter').each(function(){
    var $this = $(this);
    $this.on("click", function(){
      var $this = $(this);
      var preset = $this.data("preset");
      Caman(".filter-image-canvas", function () {
        this.revert();
        var htm = $this.html();
        $this.html("Processing...")
        applied_preset = preset
        apply_preset(this)
        this.render();
        $this.html(htm);
      });
    });
  });
}
$(document).on("click", "#crop-tab", function(){
  add_cropper();
  $("#apply_changes").data("curraction", "crop");
});
$(document).on("click", "#filters-tab", function(){
  remove_cropper();
  $("#apply_changes").data("curraction", "filter");
});
$(document).on("click", "#presets-tab", function(){
  remove_cropper();
  $("#apply_changes").data("curraction", "filter");
});

$(document).on("click", "#steaker-tab", function(){
  remove_cropper();
  $("#apply_changes").data("curraction", "steaker");
});

function add_cropper(){
  $(".filter-image-canvas").cropper({
    aspectRatio: 16 / 9,
    autoCropArea: 0.65,
    strict: false,
    guides: false,
    highlight: false,
    dragCrop: false,
    cropBoxMovable: true,
    cropBoxResizable: true,
    rotatable: true,
    minCropBoxWidth: 300,
    minCropBoxHeight: 168,
    maxCropBoxWidth: 600,
    maxCropBoxHeight: 337,
  }).on("built.cropper", function(e){
    data = $(".filter-image-canvas").cropper('getData', true);
    $("#demo-cropped-image").css({
      'background-image' : 'url("' + $(".cropper-canvas img").attr("src") + '")',
      'width' : data.width,
      'height': data.height,
      'background-position' : "-" + data.x + "px -" + data.y + "px"
    });
  }).on("cropmove.cropper", function(e){
    data = $(".filter-image-canvas").cropper('getData', true);
    $("#demo-cropped-image").css({
      'background-image' : 'url("' + $(".cropper-canvas img").attr("src") + '")',
      'width' : data.width,
      'height': data.height,
      'background-position' : "-" + data.x + "px -" + data.y + "px"
    });
  });
}

function remove_cropper(){
  $(".filter-image-canvas").cropper('destroy');
}
