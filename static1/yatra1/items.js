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
      var itemnumber = $save_btn.data("itemnumber");
      $.ajax({
        url: '/yatra/item/' + itemnumber + "/save_modified",
        type: 'post',
        data: {'attachment' : attachment},
        success: function(retdata){
          console.log(retdata);
          $save_btn.html("saved");
        }
      });
    });
  });
}

$(document).on("click", "#apply_changes", function(){
  var $this = $(this);
  var htm = $this.html();
  $this.html("Saving...")
  apply_filters_on_original_image_and_save($this);
});

$(document).on("click", ".show-upload-btn", function(){
  var $this = $(this);
  var item_number = $this.data("number");
  $.ajax({
    url: "/yatra/item/" + item_number + "/upload/form",
    data: '',
    type: 'get',
    success: function(retdata){
      $('body').append(retdata);
      $('.modal').modal('show');
      if($(".filter-image-canvas").length != 0){
        add_slider_filter_handlers();
        add_slider_preset_handlers();
        Caman(".filter-image-canvas", function(){
          this.render();
        });
      }
    }
  })
});

$(document).on('hidden.bs.modal', '#upload_modal', function (e) {
  $(this).remove();
})

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
});
$(document).on("click", "#filters-tab", function(){
  remove_cropper();
});
$(document).on("click", "#presets-tab", function(){
  remove_cropper();
});

$(document).on("change", "#label-upload-file input[type='file']", function(event){
  var files = event.target.files;
  var $this = $(this);
  var data = new FormData();
  var file_number = $this.data('filenumber');
  data.append('file_type', 'image');
  data.append('file_number', file_number)
  var $this = $(this);
  $.each(files, function(key, value){
    data.append('fi_' + file_number, value);
  });


  $.ajax({
    url: '/yatra/items/save',
    data: data,
    type: 'post',
    cache: false,
    dataType: 'json',
    processData: false, // Don't process the files
    contentType: false, // Set content type to false as jQuery will tell the server its a query string request
    success: function(retdata)
    {
      if(retdata.status == 'success'){
        if($(".template-example-image").length != 0){
          $(".template-example-image").addClass("filter-image-canvas").removeClass("template-example-image").after("<img id='original-image-canvas' src='" + retdata.attachment_url + "' data-caman-hidpi='" + retdata.attachment_url + "'/>");
          $(".filter-image-canvas").attr("width", "600");
          $(".filter-image-canvas").attr("src", retdata.resized_url);
          $(".filter-image-canvas").data("caman-hidpi", retdata.resized_url);
          add_slider_filter_handlers();
          add_slider_preset_handlers();
          Caman(".filter-image-canvas", function(){
            this.render();
          });
        }
      }
    }
  });
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


// $(document).on("click", "label-upload-file")

// $(document).on("ready", function(){
//   add_slider_filter_handlers();
//   Caman(".filter-image-canvas", function(){
//     this.render();
//   });
// });

// $(window).on("scroll", function(){
//   console.log("i m here")
//   "use strict";
//   var scroll = $(window).scrollTop();
//   if( scroll > 400 ){
//     $(".video-row").addClass("fixed-video-row");
//   } else {
//     $(".video-row").removeClass("fixed-video-row");
//   }
// });
// $(document).on("change", ".image-container input[type=\"file\"]", function(){
//   var $file_input = $(this);
//   var $image_container = $(this).closest('.image-container');
//   if(is_file_selected_an_image($file_input)){
//     save_file($file_input);
//   }
//   else{
//     alert("Not an image file");
//   }
// });

// function is_file_selected_an_image($file_input){
//   var file_name = $file_input.val()
//   return file_name.endsWith("jpg") || file_name.endsWith("jpeg")
//   // for file validations, will use it later
//   // var file = this.files[0];
//   // var name = file.name;
//   // var size = file.size;
//   // var type = file.type;
// }

// function save_file($file_input){
//   var $form = $file_input.closest("form");
//   var form = $form[0]
//   var form_data = new FormData($form[0])
//   // console.log(form_data)
//   $.ajax({
//     url: '/yatra/items/save',
//     type: 'post',
//     data: form_data,
//     cache: false,
//     contentType: false,
//     processData: false,
//     success: function(retdata){
//       console.log($form.closest(".item-box"));
//       console.log(retdata)
//       $form.closest(".item-box").html(retdata);
//     }
//   });
//   $file_input.data("itemselected", "true");
// }

// $(document).on("submit", ".item_form", function(e){
//   e.preventDefault()
//   e.stopPropagation()

// })

// $(document).on("click", ".filter-btn", function(e){
//   $('.filter-image').cropper("crop")

// });

// $(document).on("click", ".rotate-btn", function(){
//   $(".filter-image").cropper("rotate", "1")
// });

// $('.filter-image').cropper({
//   aspectRatio: 16 / 9,
//   autoCropArea: 0.65,
//   strict: false,
//   guides: false,
//   highlight: false,
//   dragCrop: false,
//   cropBoxMovable: true,
//   cropBoxResizable: true
// });