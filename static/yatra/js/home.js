$(document).on("click", ".start-here", function(){
  var data_in = $(this).data("in");
  if(data_in == 'True'){
    window.location.href = "/yatra/categories"
  }
  else{
    $(".center-box").hide('slow');
    $('a[href="#panel-signin"]').closest("li").addClass("active");
    $("#panel-signin").addClass("active");
    $(".auth-box").show('slow');
  }
});

$(document).on("submit", "#signin-form", function(e){
  e.preventDefault();
  var $form = $(this);
  $.ajax({
    url: $form.attr("action"),
    type: "post",
    data: $form.serialize(),
    success: function(retdata){
      if(retdata.status == 'error'){
        $(".signin-error").html(retdata.message);
        $(".signin-error").show();
      }
      else{
        window.location.href = "/yatra/categories"
      }
    }
  })
});