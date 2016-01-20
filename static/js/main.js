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

$(document).on("ready", function(){
	// $.ajaxSetup({
 //    beforeSend: function(xhr, settings) {
 //      if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
 //        xhr.setRequestHeader("X-CSRFToken", csrftoken);
 //      }
 //    }
	// });
});

(function($) {

	'use strict';

	$(document).ready(function(){

		// VERTICAL PAGE
		var contentSections = $('.group'),
		navigationItems = $('#vertical-nav a');

		if ($("#vertical-nav").length > 0) {
			updateNavigation();
			$(".st-content").on('scroll', function(){
				updateNavigation();
			});
		}

        // fix dropdown menu on mobile
        $('.dropdown-toggle').click(function(e) {
            e.preventDefault();
            setTimeout($.proxy(function() {
                if ('ontouchstart' in document.documentElement) {
                    $(this).siblings('.dropdown-backdrop').off().remove();
                }
            }, this), 0);
        });

        // for contact form ajax
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

		//scroll to the section
		navigationItems.on('click', function(event){
	        event.preventDefault();
	        scrollGoTo($(this.hash));
	    });
	    
	    //scroll to second section
	    $('.scroll-down').on('click', function(event){
	        event.preventDefault();
	        scrollGoTo($(this.hash));
	    });

	    //close navigation on touch devices when selectin an elemnt from the list
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

		// Flex Slider
		$('.flexslider:not(.with-nav)').flexslider({
		    animation: "fade",
		    start: function(){updateNavigation();},
		    controlNav: false
		});
		$('.flexslider.with-nav').flexslider({
		    animation: "fade",
		    controlNav: true
		});


		// PARALAX EFFECT
		/* detect touch */
		if("ontouchstart" in window){
		    document.documentElement.className = document.documentElement.className + " touch";
		}
		if(!$("html").hasClass("touch")){
		    /* background fix */
		    $(".parallax").css("background-attachment", "fixed");
		}

		/* fix vertical when not overflow
		call fullscreenFix() if .fullscreen content changes */
		function fullscreenFix(){
		    var h = $('body').height();
		    // set .fullscreen height
		    $(".content-b").each(function(i){
		        if($(this).innerHeight() <= h){
		            $(this).closest(".fullscreen").addClass("not-overflow");
		        }
		    });
		}
		$(window).resize(fullscreenFix);
		fullscreenFix();

		/* resize background images */
		function backgroundResize(){
		    var windowH = $(window).height();
		    $(".background").each(function(i){
		        var path = $(this);
		        // variables
		        var contW = path.width();
		        var contH = path.height();
		        var imgW = path.attr("data-img-width");
		        var imgH = path.attr("data-img-height");
		        var ratio = imgW / imgH;
		        // overflowing difference
		        var diff = parseFloat(path.attr("data-diff"));
		        diff = diff ? diff : 0;
		        // remaining height to have fullscreen image only on parallax
		        var remainingH = 0;
		        if(path.hasClass("parallax") && !$("html").hasClass("touch")){
		            var maxH = contH > windowH ? contH : windowH;
		            remainingH = windowH - contH;
		        }
		        // set img values depending on cont
		        imgH = contH + remainingH + diff;
		        imgW = imgH * ratio;
		        // fix when too large
		        if(contW > imgW){
		            imgW = contW;
		            imgH = imgW / ratio;
		        }
		        //
		        path.data("resized-imgW", imgW);
		        path.data("resized-imgH", imgH);
		        path.css("background-size", imgW + "px " + imgH + "px");
		    });
		}
		$(window).resize(backgroundResize);
		$(window).focus(backgroundResize);
		backgroundResize();

		/* set parallax background-position */
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
		        // only when in range
		        if(bottomWindow > top && topWindow < bottom){
		            var imgW = path.data("resized-imgW");
		            var imgH = path.data("resized-imgH");
		            // min when image touch top of window
		            var min = 0;
		            // max when image touch bottom of window
		            var max = - imgH + heightWindow;
		            // overflow changes parallax
		            var overflowH = height < heightWindow ? imgH - height : imgH - heightWindow; // fix height on overflow
		            top = top - overflowH;
		            bottom = bottom + overflowH;
		            // value with linear interpolation
		            var value = min + (max - min) * (currentWindow - top) / (bottom - top);
		            // set background-position
		            var orizontalPosition = path.attr("data-oriz-pos");
		            orizontalPosition = orizontalPosition ? orizontalPosition : "50%";
		            $(this).css("background-position", orizontalPosition + " " + value + "px");
		        }
		    });
		}
		if(!$("html").hasClass("touch")){
		    $(window).resize(parallaxPosition);
		    //$(window).focus(parallaxPosition);
            $(".st-content").scroll(
                parallaxPosition
            );
		    parallaxPosition();
		}
		// END PARALAX EFFECT



	});

	$(window).height(function(){
		if (window.innerWidth > 768) {
            $('.onscreen').css('height', window.innerHeight);
        }
        $('.slides .onscreen').css('height', window.innerHeight);
	});

	$(window).load(function(){

		// Container
		var $container = $('#foliowrap');
		$container.isotope({
			filter:'*',
			animationOptions: {
				duration: 750,
				easing: 'linear',
				queue: false,
			}
		});

		// Isotope Button
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
				// don't proceed if already selected
				if ($this.hasClass('selected')) {
					return false;
				}
				var $optionSet = $this.parents('#options');
				$optionSet.find('.selected').removeClass('selected');
				$this.addClass('selected'); 
			});
		
	});

})( jQuery );

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
$(document).on("ready", function(){
	var template_id = $(this).find(".item.active").data('template_id');
	get_variations(template_id);
	$(".carousel").carousel('pause');
	$(".carousel").on('slid.bs.carousel', function (a, b) {
	  var template_id = $(this).find(".item.active").data('template_id');
	  get_variations(template_id);
	});
  setup_plupload();
  manipulation_ui = get_original_html_for_all_image_manipulation_ui();
});

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
        $modal = $("#edit-image-modal");
        var image_id_on_dom = $modal.data("image_id_on_dom");
        var temp_image_id = "temp_image_" + image_id_on_dom;
        var value = ui.value;
        modifications_to_current_image["transitions"][transition] = value;
        Caman("#" + temp_image_id, function () {
          caman_this = this;
          caman_this.revert(false);

          $.each(modifications_to_current_image["transitions"], function(transition_name, transition_value){
            caman_this[transition_name](transition_value)
          });
          caman_this.render();
        });
      }
    });
  });
}

$(document).on("click", "a[href='#crop']", function(){
  setup_cropper();
})
$(document).on("click", "a[href='#presets']", function(){
  destroy_cropper();
})
$(document).on("click", "a[href='#transitions']", function(){
  destroy_cropper();
})

function setup_cropper(){
  $modal = $("#edit-image-modal");
  var image_id_on_dom = $modal.data("image_id_on_dom");
  var temp_image_id = "temp_image_" + image_id_on_dom;

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
  }
}

$(document).on("click", ".presets", function(){
  $modal = $("#edit-image-modal");
  var image_id_on_dom = $modal.data("image_id_on_dom");
  var temp_image_id = "temp_image_" + image_id_on_dom;
  var preset = $(this).data("preset");
  modifications_to_current_image["preset"] = preset;
  Caman("#" + temp_image_id, function () {
    caman_this = this;
    caman_this.revert(false);
    caman_this[preset]();
    caman_this.render();
  });
});

$(document).on("click", ".cropping-done-btn", function(){
  $modal = $("#edit-image-modal");
  var image_id_on_dom = $modal.data("image_id_on_dom");
  var temp_image_id = "temp_image_" + image_id_on_dom;
  Caman("#" + temp_image_id, function () {
    this.crop(modifications_to_current_image.crop_data.width, modifications_to_current_image.crop_data.height, parseInt(modifications_to_current_image.crop_data.x), parseInt(modifications_to_current_image.crop_data.y))
    modifications_to_current_image.crop_data.is_done = true;
    this.render();
    destroy_cropper();
    $("#" + temp_image_id).removeClass("cropper-hidden");
    var $temp_image = $(new Image());
    $temp_image.attr("id", temp_image_id);
    $temp_image.attr("src", $("#" + temp_image_id)[0].toDataURL("image/jpeg"));
    $temp_image.attr("style", "display:block; margin: 0 auto;");
    $("#" + temp_image_id).remove();
    $("#final_img_" + image_id_on_dom).after($temp_image);
    Caman(("#" + temp_image_id), function(){
      this.resize({
        width: 720
      });
      this.render();
    });
  });
});

function setup_plupload(){
  $("#uploader").plupload({
    // General settings
    runtimes : 'html5,html4',
    url : '/',

    // User can upload no more then 20 files in one go (sets multiple_queues to false)
    max_file_count: 20,
    
    chunk_size: '1mb',

    // Resize images on clientside if we can
    resize : {
      width : 200, 
      height : 200, 
      quality : 90,
      crop: true // crop to exact dimensions
    },
    
    filters : {
      // Maximum file size
      max_file_size : '1000mb',
      // Specify what files to browse for
      mime_types: [
        {title : "Image files", extensions : "jpg,jpeg,JPEG,JPG,png,PNG"}
      ]
    },

    // Rename files by clicking on their titles
    rename: true,
    
    // Sort files
    sortable: true,

    // Enable ability to drag'n'drop files onto the widget (currently only HTML5 supports that)
    dragdrop: true,

    // Views to activate
    views: {
      list: true,
      thumbs: true, // Show thumbs
      active: 'thumbs'
    },
    init: {
      FilesAdded: function(up, files) {
        added_files = files
        console.log('[FilesAdded]');
        plupload_this = this;
        plupload.each(files, function(file) {
          var preloader = new mOxie.Image();
          preloader.onload = function() {
            var $image = $(new Image()).appendTo("body");
            $image.prop( "src", preloader.getAsDataURL());
            $image.prop("id", "original_img_" + file.id);
            $image.css("display", "none");
          };
          preloader.load(file.getSource());
        });
      },
    } 
  });
}

$(document).on("click", ".show-edit-image-btn", function(e){
  var $show_edit_image_btn = $(this);
  var image_id_on_dom = $show_edit_image_btn.data("id");
  $modal = $("#edit-image-modal");
  $modal.data("image_id_on_dom", image_id_on_dom)
  reset_image_manipulation_modal();
  setup_sliders_for_transitions();
  setup_image_edit_modal($modal, image_id_on_dom);
  $modal.modal("show");
});

function setup_image_edit_modal($modal, image_id_on_dom){
  var original_image_id = "original_img_" + image_id_on_dom;
  var final_image_id = "final_img_" + image_id_on_dom;
  var temp_image_id = "temp_image_" + image_id_on_dom;
  var $original_image = $("#" + original_image_id);
  var $final_image = $original_image.clone();
  var $temp_image = $original_image.clone();
  $final_image.prop("id", final_image_id);
  $temp_image.prop("id", temp_image_id);
  $temp_image.attr("style", "display: block;");
  $modal.find("#temp_image_div").html($final_image);
  $modal.find("#temp_image_div").append($temp_image);
  Caman(("#" + temp_image_id), function(){
    this.resize({
      width: 720
    });
    this.render();
  });
}


$(document).on("click", "a.category_template_select", function(e){
  var $category_menu_item = $(".category_menu_item.selected");
  var $category_template_select = $(this);
  var category_id = $category_menu_item.data("category_id");
  var template_id = $category_template_select.data("template_id");
  go_to_category_with_selected_template(category_id, template_id);
});


function go_to_category_with_selected_template(category_id, template_id){
  window.location.href = '/edit/' + category_id + "?template_id=" + template_id 
}

function get_variations(parent_template_id){
	$.ajax({
  	url: '/variations/' + parent_template_id,
  	type: 'get',
  	success: function(retdata){
  		$(".carousel-inner.variation_templates").html(retdata);
  	}
  });
}

$(document).on("click", ".steaker-btn", function(){
  $modal = $("#edit-image-modal");
  var image_id_on_dom = $modal.data("image_id_on_dom");
  var temp_image_id = "temp_image_" + image_id_on_dom;
  var $steaker_image = $(this).clone();
  $(".steaker-instance").remove();
  $steaker_image.removeClass("steaker-btn");
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

    $modal = $("#edit-image-modal");
    var image_id_on_dom = $modal.data("image_id_on_dom");
    var temp_image_id = "temp_image_" + image_id_on_dom;
    var image = $steaker_image[0];
    var ctx    = $("#" + temp_image_id)[0].getContext("2d");
    modifications_to_current_image.added_steakers.push({
      id_on_dom : $steaker_image.attr("id"),
      top: top,
      left: left
    })
    ctx.drawImage(image, left, top);
  }
});


$(document).on("click", ".add-text-btn", function(){
  $modal = $("#edit-image-modal");
  var image_id_on_dom = $modal.data("image_id_on_dom");
  var temp_image_id = "temp_image_" + image_id_on_dom;
  add_text_over_canvas($("#image-text-input").val(), temp_image_id, 18, 'arial');
});
function add_text_over_canvas(text, canvas_id, font_size, font_name){
  $("#text-instance").remove();
  var $text_div = $("<div id='text-instance' style='position: absolute; top: 0px; left: 0px; line-height: 1; font-size: " + font_size + "px; border: none; font-family: " + font_name + ";'>" + text + "</div>");
  $text_div.insertAfter("#" + canvas_id);
  $text_div.draggable({
    containment: "#" + canvas_id
  });
}

$(document).on("click", ".place-text-btn", function(){
  $modal = $("#edit-image-modal");
  var image_id_on_dom = $modal.data("image_id_on_dom");
  var temp_image_id = "temp_image_" + image_id_on_dom;
  var top = parseInt($("#text-instance").css("top"));
  left = parseInt($("#text-instance").css("left"));
  place_text_over_canvas($("#text-instance").html(), temp_image_id, top, left, 18, 'arial');
});
function place_text_over_canvas(text, canvas_id, top, left, font_size, font_name){
  var canvas = document.getElementById(canvas_id);
  var context = canvas.getContext("2d");
  context.font=font_size + "px " + font_name;
  context.fillText(text, left, top + font_size -2);
}
