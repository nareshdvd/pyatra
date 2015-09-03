


// document.addEventListener( "DOMContentLoaded", function() {
//   $("video").each(function(){
//     var $video = $(this);
//     var popcorn = Popcorn("#" + $(this).attr("id"));
//     var duration = 0;

//     popcorn.on('timeupdate', function(){
//       var this_popcorn = this;
//       var cutter_slider_id = $video.data("templateid")
//       var $curr_slider = $("#cutter-slider-" + cutter_slider_id)
//       var curr_range = $curr_slider.slider("values");
//       var last = curr_range[1];
//       print(this_popcorn.currentTime())
//       if(this_popcorn.currentTime() >= last){
//         popcorn.pause();
//       }
//     });
//     popcorn.on('loadedmetadata', function() {
//       var this_popcorn = this;
//       duration = parseInt(this_popcorn.duration())
//       var cutter_slider_id = $video.data("templateid")
//       $("#cutter-slider-" + cutter_slider_id).slider({
//         range: true,
//         values: [0,2],
//         animate: "fast",
//         min: 0,
//         max: duration,
//         slide: function( event, ui ) {
//           var $target = $(event.target);
//           var val_1 = ui.value;
//           var val_2 = val_1 + 2;
//           this_popcorn.currentTime(val_1)
//           $target.slider("values", [val_1, val_2] );
//         }
//       });
//     });
//   });
// });

// function print(dt){
//   console.log(dt)
// }