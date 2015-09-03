var applied_filters = [];

function filter_handler(event, ui){
  var $slider_ele = $(event.target);
  var value = ui.value;
  var filter_name = $slider_ele.data("filter");
  Caman(".filter-image-canvas", function () {
    this.revert();
    apply_filters(this, filter_name, value);
    this.render();
  });
}

function apply_filter(filter_ele, func_name, value){
  switch(func_name){
    case "brightness":
      filter_ele.brightness(value);
      break;
    case "contrast":
      filter_ele.contrast(value);
      break;
    case "vibrance":
      filter_ele.vibrance(value);
      break;
    case "saturation":
      filter_ele.saturation(value);
      break;
    case "hue":
      filter_ele.hue(value);
      break;
    case "sepia":
      filter_ele.sepia(value);
      break;
    case "noise":
      filter_ele.noise(value);
      break;
    case "stackBlur":
      filter_ele.stackBlur(value);
      break;
  }
  return filter_ele
}


function apply_filters(filter_ele, curr_filter_name, curr_filter_value){
  var func_name;
  var value;
  var curr_func_found_in_applied_filters = false;
  for(var i=0;i< applied_filters.length; i++){
    func_name = applied_filters[i]['func_name'];
    value = applied_filters[i]['value'];
    if(func_name==curr_filter_name){
      applied_filters[i] = {
        'func_name' : func_name,
        'value' : curr_filter_value
      }
      curr_func_found_in_applied_filters = true
      apply_filter(filter_ele, func_name, curr_filter_value);
    }
    else{
      apply_filter(filter_ele, func_name, value);
    }
  }
  if(!curr_func_found_in_applied_filters){
    applied_filters.push({
      'func_name' : curr_filter_name,
      'value' : curr_filter_value
    });
  }
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

$(document).on("ready", function(){
  add_slider_filter_handlers();
  Caman(".filter-image-canvas", function(){
    this.render();
  });
});