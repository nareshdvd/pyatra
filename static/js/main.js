(function($) {
  'use strict';
  $(document).ready(function(){
    var contentSections = $('.group'),
    navigationItems = $('#vertical-nav a');
    if ($("#vertical-nav").length > 0) {
      updateNavigation();
      $(".st-content").on('scroll', function(){
        updateNavigation();
      });
    }
    $('.dropdown-toggle').click(function(e) {
      e.preventDefault();
      setTimeout($.proxy(function() {
        if ('ontouchstart' in document.documentElement) {
          $(this).siblings('.dropdown-backdrop').off().remove();
        }
      }, this), 0);
    });

    jQuery.support.cors = true;
    $("#formContact").submit(function() {
      var url = "send.php";
      $.ajax({
        type: "POST",
        url: url,
        data: $("#formContact").serialize(),
        beforeSend: function(xhr){
          $("#formContact").css('cssText', 'display: none !important');
          $(".loading").css('cssText', 'display: table !important');
        },
        success: function(data)
        {
          var msg = jQuery.parseJSON(data);
          $(".loading").css('cssText', 'display: none !important');
          if (msg.status == "success") {
            $(".form-contact-status").css('cssText', 'display: block !important');
          } else {
            $("#formContact").css('cssText', 'display: block !important');
            alert("Fail send contact");
          }
        },
        error: function(msg)
        {
          $(".loading").css('cssText', 'display: none !important');
          $("#formContact").css('cssText', 'display: block !important');
          alert("Fail send contact");
        }
      });
      return false;
    });

    navigationItems.on('click', function(event){
      event.preventDefault();
      scrollGoTo($(this.hash));
    });

    $('.scroll-down').on('click', function(event){
      event.preventDefault();
      scrollGoTo($(this.hash));
    });

    $('.touch #vertical-nav a').on('click', function(){
      $('.touch #vertical-nav').removeClass('open');
    });

    function updateNavigation() {
      contentSections.each(function(){
        var $this = $(this);
        var activeSection = $('#vertical-nav a[href="#'+$this.attr('id')+'"]').data('number') - 1;
        if ( ( $this.offset().top - $(window).height()/2 < $(window).scrollTop() ) && ( $this.offset().top + $this.height() - $(window).height()/2 > $(window).scrollTop() ) ) {
          navigationItems.eq(activeSection).addClass('is-selected');
        }else {
          navigationItems.eq(activeSection).removeClass('is-selected');
        }
      });
    }

    var firstSectionId = $('#vertical-nav a[data-number="' + 1 + '"]').attr("href"),
    $firstSection = $('section' + firstSectionId);
    function scrollGoTo(target) {
      var pageTopPadding = ($('.st-content-inner #page').length > 0) ? parseInt($('.st-content-inner #page').css('padding-top')) : 0;
      var offsets = (target.offset().top - $firstSection.offset().top + pageTopPadding);
      if (offsets < 0 ) { offsets * -1 };
      $('body,html,.st-content').animate(
        {'scrollTop':offsets},
        600
        );
    }

    $('.flexslider:not(.with-nav)').flexslider({
      animation: "fade",
      start: function(){updateNavigation();},
      controlNav: false
    });
    $('.flexslider.with-nav').flexslider({
      animation: "fade",
      controlNav: true
    });

    if("ontouchstart" in window){
      document.documentElement.className = document.documentElement.className + " touch";
    }
    if(!$("html").hasClass("touch")){
      $(".parallax").css("background-attachment", "fixed");
    }

    function fullscreenFix(){
      var h = $('body').height();
      $(".content-b").each(function(i){
        if($(this).innerHeight() <= h){
          $(this).closest(".fullscreen").addClass("not-overflow");
        }
      });
    }
    $(window).resize(fullscreenFix);
    fullscreenFix();

    function backgroundResize(){
      var windowH = $(window).height();
      $(".background").each(function(i){
        var path = $(this);
        var contW = path.width();
        var contH = path.height();
        var imgW = path.attr("data-img-width");
        var imgH = path.attr("data-img-height");
        var ratio = imgW / imgH;
        var diff = parseFloat(path.attr("data-diff"));
        diff = diff ? diff : 0;
        var remainingH = 0;
        if(path.hasClass("parallax") && !$("html").hasClass("touch")){
          var maxH = contH > windowH ? contH : windowH;
          remainingH = windowH - contH;
        }
        imgH = contH + remainingH + diff;
        imgW = imgH * ratio;
        if(contW > imgW){
          imgW = contW;
          imgH = imgW / ratio;
        }
        path.data("resized-imgW", imgW);
        path.data("resized-imgH", imgH);
        path.css("background-size", imgW + "px " + imgH + "px");
      });
    }
    $(window).resize(backgroundResize);
    $(window).focus(backgroundResize);
    backgroundResize();

    function parallaxPosition(e){
      var heightWindow = $(window).height();
      var topWindow = $(window).scrollTop();
      var bottomWindow = topWindow + heightWindow;
      var currentWindow = (topWindow + bottomWindow) / 2;
      $(".parallax").each(function(i){
        var path = $(this);
        var height = path.height();
        var top = path.offset().top;
        var bottom = top + height;
        if(bottomWindow > top && topWindow < bottom){
          var imgW = path.data("resized-imgW");
          var imgH = path.data("resized-imgH");
          var min = 0;
          var max = - imgH + heightWindow;
          var overflowH = height < heightWindow ? imgH - height : imgH - heightWindow;
          top = top - overflowH;
          bottom = bottom + overflowH;
          var value = min + (max - min) * (currentWindow - top) / (bottom - top);
          var orizontalPosition = path.attr("data-oriz-pos");
          orizontalPosition = orizontalPosition ? orizontalPosition : "50%";
          $(this).css("background-position", orizontalPosition + " " + value + "px");
        }
      });
    }
    if(!$("html").hasClass("touch")){
      $(window).resize(parallaxPosition);
      $(".st-content").scroll(
        parallaxPosition
        );
      parallaxPosition();
    }
  });

  $(window).height(function(){
    if (window.innerWidth > 768) {
      $('.onscreen').css('height', window.innerHeight);
    }
    $('.slides .onscreen').css('height', window.innerHeight);
  });

  $(window).load(function(){

    var $container = $('#foliowrap');
    $container.isotope({
      filter:'*',
      animationOptions: {
        duration: 750,
        easing: 'linear',
        queue: false,
      }
    });

    $('#options li a').click(function(){
      var selector = $(this).attr('data-filter');
      $container.isotope({
        filter:selector,
        animationOptions: {
          duration: 750,
          easing: 'linear',
          queue: false,
        }
      });
      return false;
    });

    var $optionSets = $('#options'),
    $optionLinks = $optionSets.find('a');

    $optionLinks.click(function(){
      var $this = $(this);
      if ($this.hasClass('selected')) {
        return false;
      }
      var $optionSet = $this.parents('#options');
      $optionSet.find('.selected').removeClass('selected');
      $this.addClass('selected'); 
    });
  });
})( jQuery );


//All Global Variables
var added_files = []
var plupload_this;
var modifications_to_current_image = {
  transitions: {},
  preset: "",
  crop_data: {width: '', height: ''},
  added_texts: [],
  added_steakers: []
}
var manipulation_ui = "";
var cropper;
var current_template_items_info;

//Document on ready callback
$(document).on("ready", function(){
	var template_id = $(".parent_templates").find(".item.active").data('template_id');
  var category_id = $(".parent_templates").data('category_id');
	get_variations(category_id, template_id);
	$(".carousel").carousel('pause');
	$(".carousel").on('slid.bs.carousel', function (a, b) {
	  var template_id = $(this).find(".item.active").data('template_id');
    var category_id = $(".parent_templates").data('category_id');
	  get_variations(category_id, template_id);
	});
  manipulation_ui = get_original_html_for_all_image_manipulation_ui();
});


//All Click Event handlers
$(document).on("click", "a[href='#crop']", function(){
  setup_cropper();
});

$(document).on("click", "a[href='#presets']", function(){
  destroy_cropper();
});

$(document).on("click", "a[href='#transitions']", function(){
  destroy_cropper();
});

$(document).on("click", ".presets", function(){
  var temp_image_id = get_temp_image_id();
  var preset = $(this).data("preset");
  modifications_to_current_image["preset"] = preset;
  apply_preset(temp_image_id, preset);
});

$(document).on("click", ".cropping-done-btn", function(){
  var temp_image_id = get_temp_image_id();
  apply_crop(temp_image_id, modifications_to_current_image.crop_data, make_changes_permanent_to_temp_image);
  destroy_cropper();
});

$(document).on("click", ".show-edit-image-btn", function(e){
  var $show_edit_image_btn = $(this);
  var $modal = $("#edit-image-modal");
  var image_id_on_dom = $show_edit_image_btn.data("id");
  $modal.data("image_id_on_dom", image_id_on_dom)
  reset_image_manipulation_modal();
  setup_image_edit_modal($modal, image_id_on_dom);
  $modal.modal("show");
});

$(document).on("click", ".show-edit-video-btn", function(e){
  var file_id = $(this).data("id");
  $temp_video = $("#original_video_" + file_id).clone();
  $temp_video.attr("id", "temp_video_" + file_id);
  $temp_video.addClass("temp_modal_video");
  $temp_video.prop("controls", true);
  $("#temp_video_div").append($temp_video);
  $temp_video[0].currentTime = 1;
  $("#edit-video-modal").modal("show");
});

$(document).on("click", "a.category_template_select", function(e){
  var $category_menu_item = $(".category_menu_item.selected");
  var $category_template_select = $(this);
  var category_id = $category_menu_item.data("category_id");
  var template_id = $category_template_select.data("template_id");

  if(category_id == 0){
    category_id = $category_template_select.data("category_id");
  }
  go_to_category_with_selected_template(category_id, template_id);
});

$(document).on("click", ".steaker-btn", function(){
  var temp_image_id = get_temp_image_id();
  var $steaker_image = $(this).clone();
  $(".steaker-instance").remove();
  $steaker_image.removeClass("steaker-btn");
  $steaker_image.attr("id", "temp_steaker_instance");
  $steaker_image.data("steakerid", $(this).attr("id"));
  $steaker_image.addClass("steaker-instance");
  $steaker_image.attr("style", "position: absolute; top: 0px; left: 0px;");
  $steaker_image.insertAfter("#" + temp_image_id);
  $steaker_image.draggable({
    containment: "#" + temp_image_id
  });
});

$(document).on("click", ".place-steaker-btn", function(){
  if(confirm("This action is not reverable, Press OK if you want to place this steaker")){
    var $steaker_image = $(".steaker-instance");
    var left = parseInt($steaker_image.css("left"));
    var top = parseInt($steaker_image.css("top"));

    var temp_image_id = get_temp_image_id();
    
    modifications_to_current_image.added_steakers.push({
      id_on_dom : $steaker_image.data("steakerid"),
      top: top,
      left: left
    });

    place_steaker_over_canvas(temp_image_id, $steaker_image.data("steakerid"), left, top);
  }
});

$(document).on("click", ".add-text-btn", function(){
  var temp_image_id = get_temp_image_id();
  add_text_over_canvas($("#image-text-input").val(), temp_image_id, 18, 'arial');
});

$(document).on("click", ".place-text-btn", function(){
  var temp_image_id = get_temp_image_id();
  var top = parseInt($("#text-instance").css("top"));
  left = parseInt($("#text-instance").css("left"));
  place_text_over_canvas($("#text-instance").html(), temp_image_id, top, left, 18, 'arial');
});

$(document).on("click", ".select-template-link", function(){
  var $this = $(this);
  var template_id = $this.data("template_id");
  var category_id = $this.data("category_id");
  $.ajax({
    url: '/select_variation/' + category_id + "/" + template_id,
    type: 'get',
    data: {},
    success: function(retdata){
      current_template_items_info = retdata.items;
      $("#uploader_images").html("");
      $("#uploader_videos").html("");
      var image_items = $(retdata.items).map(function(){
        if(this.item_type == "image"){
          return this;
        }
        else{
          return null;
        }
      });
      $("#uploader_images").data("items_count", image_items.length);
      $("#uploader_videos").data("items_count", retdata.items.length - image_items.length);
      $.each(retdata.items, function(){
        var item = this;
        if(item.item_file != "" && item.item_type == "image"){
          create_preview_of_file(item.item_file, "uploader_images", item.item_type);
        }
        else{
          if(item.item_file != "" && item.item_type == "video"){
            create_preview_of_file(item.item_file, "uploader_videos", item.item_type);
          }
        }
      });
      document.getElementById("uploader_images").ondragover = function(e){
        e.preventDefault();
        return false;
      }
      document.getElementById("uploader_images").ondrop = function(e){
        e.preventDefault();
        handle_dragged_files(e.dataTransfer.files, this.id, "image");
      }
      document.getElementById("uploader_videos").ondragover = function(e){
        e.preventDefault();
        return false;
      }
      document.getElementById("uploader_videos").ondrop = function(e){
        e.preventDefault();
        handle_dragged_files(e.dataTransfer.files, this.id, "video");
      }
    }
  });
});

$(document).on("click", ".update_changes_to_original_image", function(e){
  var temp_image_id = get_temp_image_id();
  update_changes_to_original_image(temp_image_id);
  $("#edit-image-modal").modal("hide");
});

$(document).on("hidden.bs.modal", "#edit-image-modal", function(){
  var $modal = $("#edit-image-modal");
  var temp_image_id = get_temp_image_id();
  var object_id = temp_image_id.replace("temp_img_", "");
  reset_image_manipulation_modal();
  destroy_cropper();
  setup_image_edit_modal($modal, object_id);
});

$(document).on("click", "#upload_added_files", function(){
  var all_data_to_upload = [];
  var sorted_image_ids = [];
  var sorted_video_ids = [];
  var combined_sorted_ids = [];
  $("#uploader_images").find(".item_row").each(function(){
    var $item_row = $(this);
    sorted_image_ids.push($item_row.sortable("toArray"));
  });
  sorted_image_ids = $(sorted_image_ids).map(function(){if(this.length != 0) return this;});
  $("#uploader_videos").find(".item_row").each(function(){
    var $item_row = $(this);
    sorted_video_ids.push($item_row.sortable("toArray"));
  });
  sorted_video_ids = $(sorted_video_ids).map(function(){if(this.length != 0) return this;});

  $.each(current_template_items_info, function(){
    if(this.item_type == 'image'){
      combined_sorted_ids.push(sorted_image_ids[0]);
      sorted_image_ids.splice(0,1);
    }
    else{
      combined_sorted_ids.push(sorted_video_ids[0]);
      sorted_video_ids.splice(0,1);
    }
  });
  $.each(combined_sorted_ids, function(i, val){
    var dom_element_id = val;
    console.log(dom_element_id)
    console.log(typeof dom_element_id);
    if((typeof dom_element_id) == "string"){
      var $dom_item = $("#" + dom_element_id);
      var src;
      if($dom_item.hasClass("img_col")){
        src = $dom_item.find(".portlet-content img").first().attr("src");
      }
      else{
        src = $dom_item.find(".portlet-content video source").first().attr("src");
      }
      current_template_items_info[i].item_file = src;
    }
  });
});

function update_changes_to_original_image(temp_image_id){
  var object_id = temp_image_id.replace("temp_img_", "");
  var canvas = document.getElementById(temp_image_id);
  var image_base64 = canvas.toDataURL();
  var original_image_object = document.getElementById("original_img_" + object_id);
  $(original_image_object).attr("src", image_base64);
}

function handle_dragged_files(files, uploader_div_id, file_type){
  $.each(files, function(){
    var file = this;
    var $uploader_div = $("#" + uploader_div_id);
    var max_items_count = parseInt($uploader_div.data("items_count"));
    var already_added_items_count = $uploader_div.find(".item_col").length;
    if(already_added_items_count < max_items_count){
      create_preview_of_file(file, uploader_div_id, file_type);
    }
  })
}

function create_preview_of_file(file, uploader_div_id, file_type){
  var $holder = $("#" + uploader_div_id);
  if($holder.find(".row").length == 0)
  {
   $holder.append("<div class='row item_row'></div>"); 
  }
  var $last_row = $holder.find(".row").last();
  if($last_row.find(".col-sm-2").length == 6){
    $holder.append("<div class='row item_row'></div>");
  }
  $last_row = $holder.find(".row").last();
  $last_row.append("<div class='col-sm-2'></div>");
  $last_row.sortable({
    connectWith: '#'+ uploader_div_id + ' div.row',
    distance: 0,
    dropOnEmpty: true,
    handle: ".sortable-item-mover"
  })
  var $last_col = $last_row.find(".col-sm-2").last();
  if(file_type == "image"){
    $last_col.html(get_new_portlet("show-edit-image-btn"));
    $last_col.addClass("img_col").addClass("item_col");
  }
  else{
    $last_col.html(get_new_portlet("show-edit-video-btn"));
    $last_col.addClass("video_col").addClass("item_col"); 
  }
  var file_id = Math.random().toString(36).substr(2, 35);
  $last_col.attr("id", file_id);
  if(file_type == "image"){
    if(file.name != undefined){
      // file is a file
      var reader = new FileReader();  
      reader.onload = function (event) {
        var image = new Image();
        image.src = event.target.result;
        $(image).attr("style", "width : 100%; min-height: 105px;");
        
        $(image).attr("id", "original_img_" + file_id);
        $last_col.find(".portlet-content").html($(image));
        $last_col.find(".show-edit-image-btn").data("id", file_id);
      };
      reader.readAsDataURL(file);
    }
    else{
      // file is a url
      var image = new Image();
      image.src = file;
      $(image).attr("style", "width : 100%; min-height: 105px;");
      $(image).attr("id", "original_img_" + file_id);
      $last_col.find(".portlet-content").html($(image));
      $last_col.find(".show-edit-image-btn").data("id", file_id);
    }
  }
  else{
    if(file.name != undefined){
      // file is a file
      var URL = window.URL || window.webkitURL
      var reader = new window.FileReader();
      reader.onload = function(evt) {
        var $video = $("<video style='width: 100px;' id='original_video_" + file_id + "'>" + "<source src='"+evt.target.result+"' type='video/mp4'></source >Your browser does not support the video tag." + "</video>");
        $last_col.find(".portlet-content").html($video);
        var video = document.getElementById("original_video_" + file_id);
        video.currentTime = 1;
        $last_col.find(".show-edit-video-btn").data("id", file_id);
        
      };
      reader.readAsDataURL(file);
    }
    else{
      // file is a url of video file on server
      var $video = $("<video style='width: 100px;' id='original_video_" + file_id + "'>" + "<source src='"+file+"' type='video/mp4'></source >Your browser does not support the video tag." + "</video>");
      $last_col.find(".portlet-content").html($video);
      var video = document.getElementById("original_video_" + file_id);
      video.currentTime = 1;
      $last_col.find(".show-edit-video-btn").data("id", file_id);
    }
  }
}

function get_new_portlet(edit_btn_class){
  var htm = '<div class="portlet ui-widget ui-widget-content ui-helper-clearfix ui-corner-all">';
    htm += '<div class="portlet-header ui-widget-header ui-corner-all">'
      htm += '<div class="pull-left"><span class="sortable-item-mover"><i class="glyphicon glyphicon-move"></i></span><span>Image<span></div>';
      htm += '<div class="pull-right text-right">';
        htm += "<span style='display: inline-block;'><i class='glyphicon glyphicon-edit " + edit_btn_class + "'></i></span>";
        htm += "<span style='display: inline-block;'><i class='glyphicon glyphicon-remove'></i></span>";
      htm += '</div>';
    htm += '</div>';
    htm += '<div class="portlet-content"></div>';
  htm += '</div>';
  return htm;
}

// All Image Modification Functions
function apply_transition(canvas_id, transitions, value){
  Caman("#" + canvas_id, function () {
    caman_this = this;
    caman_this.revert(false);

    $.each(transitions, function(transition_name, transition_value){
      caman_this[transition_name](transition_value)
    });
    caman_this.render();
  });
}

function apply_preset(canvas_id, preset){
  Caman("#" + canvas_id, function () {
    caman_this = this;
    caman_this.revert(false);
    caman_this[preset]();
    caman_this.render();
  });
}

function apply_crop(canvas_id, crop_data, after_crop_callback){
  Caman("#" + canvas_id, function () {
    this.crop(crop_data.width, crop_data.height, parseInt(crop_data.x), parseInt(crop_data.y))
    this.render();
    if(after_crop_callback != undefined && after_crop_callback != null){
      after_crop_callback(canvas_id);
    }
    modifications_to_current_image.crop_data.is_done = true;
  });
}

function make_changes_permanent_to_temp_image(canvas_id){
  var image_id_on_dom = canvas_id.replace("temp_img_", "");
  $("#" + canvas_id).removeClass("cropper-hidden");
  var $temp_image = $(new Image());
  $temp_image.attr("id", canvas_id);
  $temp_image.attr("src", $("#" + canvas_id)[0].toDataURL("image/jpeg"));
  $temp_image.attr("style", "display:block; margin: 0 auto;");
  $("#" + canvas_id).remove();
  $("#final_img_" + image_id_on_dom).after($temp_image);
  Caman(("#" + canvas_id), function(){
    this.resize({
      width: 720
    });
    this.render();
  });
}

function place_steaker_over_canvas(canvas_id, steaker_id, left, top){
  var ctx    = $("#" + canvas_id)[0].getContext("2d");
  var image = $("#" + steaker_id)[0];
  ctx.drawImage(image, left, top);
  make_changes_permanent_to_temp_image(canvas_id);
  $("#temp_steaker_instance").remove();
}

function place_text_over_canvas(text, canvas_id, top, left, font_size, font_name){
  var canvas = document.getElementById(canvas_id);
  var context = canvas.getContext("2d");
  context.font=font_size + "px " + font_name;
  context.fillText(text, left, top + font_size -2);
  make_changes_permanent_to_temp_image(canvas_id);
  $("#text-instance").remove();
}

//Other Used Functions

/* 
  Tasks for tomorrow:
  1. create div#all_uploaded_images to contain all the img tags after edit in the uploaded image and other uploaded images that are without any effects.
  2. Add code here to add images to a div#all_uploaded_images after the "Save Changes" button is clicked over the image edit modal.
  3. Add code to get all the img tags in div#all_uploaded_images, get their src attribute which will be the base64 images and make an ajax call to upload those to server

  4. Add code to crop a video, for that we need to save the duration of the video added in sample template and provide that duration to user so that user can pick the part of video uploaded by him with same duration.
  5. Add code to upload the video using ajax call. 

  6. Add code to pre-load already added files to plupload widget
  <li class="plupload_file ui-state-default plupload_delete" id="o_1a9m762idhjalcs11379ef1vauo" style="width:100px;"><div class="plupload_file_thumb plupload_thumb_embedded" style="width: 100px; height: 60px;"><div class="plupload_file_dummy ui-widget-content" style="line-height: 60px;"><span class="ui-state-disabled">png </span></div><canvas width="100" height="60" id="uid_1a9m762m51ci2137fqdgiclgir_canvas"></canvas></div><div class="plupload_file_status"><div class="plupload_file_progress ui-widget-header" style="width: 0%"> </div><span class="plupload_file_percent"> </span></div><div class="plupload_file_name" title="Fitness.png"><span class="plupload_file_name_wrapper">Fitness.png </span></div><div class="plupload_file_action"><div class="plupload_action_icon fa fa-minus-square"> </div><div class="show-edit-image-btn fa fa-pencil-square" data-id="o_1a9m762idhjalcs11379ef1vauo"> </div></div><div class="plupload_file_size">223 kb </div><div class="plupload_file_fields"> </div></li>
*/

// 1. create div#all_uploaded_files to contain all the files after edit in the uploaded image and other uploaded images that are without any effects.




function get_temp_image_id(){
  var $modal = $("#edit-image-modal");
  var image_id_on_dom = $modal.data("image_id_on_dom");
  var temp_image_id = "temp_img_" + image_id_on_dom;
  return temp_image_id;
}

function get_original_html_for_all_image_manipulation_ui(){

  return $("#modifications_div").html();
}

function reset_image_manipulation_modal(){
  $("#modifications_div").html(manipulation_ui);
  modifications_to_current_image = {
    transitions: {},
    preset: "",
    crop_data: {width: '', height: '', x: '', y: '', is_done: false},
    added_texts: [],
    added_steakers: []
  } 
}

function setup_sliders_for_transitions(){
  $("div#transitions").find("div.transitions").each(function(){
    var min = $(this).data("min");
    var max = $(this).data("max");
    var transition = $(this).data("transition");
    $(this).slider({
      min: min,
      max: max,
      change: function(event, ui){
        var temp_image_id = get_temp_image_id();
        var value = ui.value;
        modifications_to_current_image["transitions"][transition] = value;
        apply_transition(temp_image_id, modifications_to_current_image["transitions"], value);
      }
    });
  });
}

function add_text_over_canvas(text, canvas_id, font_size, font_name){
  $("#text-instance").remove();
  var $text_div = $("<div id='text-instance' style='position: absolute; top: 0px; left: 0px; line-height: 1; font-size: " + font_size + "px; border: none; font-family: " + font_name + ";'>" + text + "</div>");
  $text_div.insertAfter("#" + canvas_id);
  $text_div.draggable({
    containment: "#" + canvas_id
  });
}

function setup_cropper(){
  var temp_image_id = get_temp_image_id();
  var image = document.getElementById(temp_image_id);
  if(cropper == undefined || cropper == null){
    cropper = new Cropper(image, {
      aspectRatio: 4 / 3,
      movable: false,
      scalable: false,
      zoomable: false,
      minCropBoxWidth: 720,
      minCropBoxHeight: 576,
      minCanvasWidth: 720,
      minCanvasHeight: 576,
      cropBoxResizable: false,
      viewMode: 1,
      cropend: function() {
        crop_data = cropper.getData();
        modifications_to_current_image.crop_data.width = crop_data.width;
        modifications_to_current_image.crop_data.height = crop_data.height;
        modifications_to_current_image.crop_data.x = crop_data.x;
        modifications_to_current_image.crop_data.y = crop_data.y;
      }
    });
  }
}

function destroy_cropper(){
  if (cropper != undefined){
    cropper.destroy();
    cropper = undefined;
  }
}

function setup_image_edit_modal($modal, image_id_on_dom){
  var original_image_id = "original_img_" + image_id_on_dom;
  var final_image_id = "final_img_" + image_id_on_dom;
  var temp_image_id = "temp_img_" + image_id_on_dom;
  var $original_image = $("#" + original_image_id);
  var $final_image = $original_image.clone();
  var $temp_image = $original_image.clone();
  $final_image.prop("id", final_image_id);
  $temp_image.prop("id", temp_image_id);
  $final_image.attr("style", "display: none;");
  $temp_image.attr("style", "display: block;");
  $modal.find("#temp_image_div").html($final_image);
  $modal.find("#temp_image_div").append($temp_image);
  Caman(("#" + temp_image_id), function(){
    this.resize({
      width: 720
    });
    this.render();
  });
  setup_sliders_for_transitions();
}

function go_to_category_with_selected_template(category_id, template_id){

  window.location.href = '/edit/' + category_id + "?template_id=" + template_id 
}

function get_variations(category_id, parent_template_id){
  $.ajax({
    url: '/variations/' + category_id + '/' + parent_template_id,
    type: 'get',
    success: function(retdata){
      $(".carousel-inner.variation_templates").html(retdata);
    }
  });
}