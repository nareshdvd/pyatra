$(document).on("ready", function(){
  $(".filter-image-original").cropper({
    aspectRatio: 16 / 9,
    autoCropArea: 0.65,
    strict: false,
    guides: false,
    highlight: false,
    dragCrop: false,
    cropBoxMovable: true,
    cropBoxResizable: true,
    rotatable: false
  });
});

$(document).on("click", "#crop", function(){
  var cropped_data = $(".filter-image-original").cropper("getData");
  console.log(cropped_data);
  $.ajax({
    url: '/yatra/items/2/save_crop',
    data: cropped_data,
    type: 'post',
    success: function(retdata){
      console.log(retdata)
    }
  })
  // Caman(".filter-image-original", function(){
  //   this.crop(cropped_data['width'], cropped_data['height'], cropped_data['x'], cropped_data['y'])
  //   this.render();
  // });
});