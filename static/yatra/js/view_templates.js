videojs.options.flash.swf = "video-js.swf";

$(document).on("click", ".view-variations", function(e){
  e.preventDefault();
  var $this = $(this);
  $.ajax({
    url: $this.attr("href"),
    type: "get",
    success: function(retdata){
      $("body").append(retdata);
      $("#template-variation-modal").modal("show");
    }
  });
})

$(document).on("hidden.bs.modal", "#template-variation-modal", function(){
  $("#template-variation-modal").remove();
});