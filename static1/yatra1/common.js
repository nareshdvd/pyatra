$(document).ready(function() {
  if($("#bd-overlay").length != 0){
    var body = document.body, html = document.documentElement;
    var height = Math.max( body.scrollHeight, body.offsetHeight, html.clientHeight, html.scrollHeight, html.offsetHeight );
    $("#bd-overlay").css("height", height + "px");
  }
  // --------------------------------------------------------
  //  Navigation Bar
  // --------------------------------------------------------
  $(window).scroll(function(){
    "use strict";
    var scroll = $(window).scrollTop();
    if( scroll > 10 ){
      $(".navbar").addClass("scroll-fixed-navbar");
    } else {
      $(".navbar").removeClass("scroll-fixed-navbar");
    }
  });
  $(window).resize(function(){
    if($("#bd-overlay").length != 0){
      var body = document.body, html = document.documentElement;
      var height = Math.max( body.scrollHeight, body.offsetHeight, html.clientHeight, html.scrollHeight, html.offsetHeight );
      $("#bd-overlay").css("height", height + "px");
    }
  });
});