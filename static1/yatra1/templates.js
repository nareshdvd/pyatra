$(document).on("ready", function(){
  data = []
  $("#video-items-info input[type='hidden']").each(function(){
    var $this = $(this);
    var title = $this.data("title");
    var href = $this.val();
    var type = "video/mp4";
    data.push({
      title: title,
      href: href,
      type: type,
      templateid: $this.data("templateid"),
      categoryid: $this.data("categoryid")
    });
  });
  blueimp.Gallery(data, {
    container: '#blueimp-video-carousel',
    carousel: false,
    onslide: function (index, slide) {
        var template_list = this.list;
        var templateid = template_list[index].templateid;
        var categoryid = template_list[index].categoryid;
        $(".select-template").attr("href", "/yatra/" + categoryid + "/select/template/" + templateid);
    }
  });
});



// {
//             title: 'Sintel',
//             href: 'http://media.w3.org/2010/05/sintel/trailer.mp4',
//             type: 'video/mp4',
//             poster: 'http://media.w3.org/2010/05/sintel/poster.png'
//         },
//         {
//             title: 'Big Buck Bunny',
//             href: 'http://upload.wikimedia.org/wikipedia/commons/7/75/' +
//                 'Big_Buck_Bunny_Trailer_400p.ogg',
//             type: 'video/ogg',
//             poster: 'http://upload.wikimedia.org/wikipedia/commons/thumb/7/70/' +
//                 'Big.Buck.Bunny.-.Opening.Screen.png/' +
//                 '800px-Big.Buck.Bunny.-.Opening.Screen.png'
//         },
//         {
//             title: 'Elephants Dream',
//             href: 'http://upload.wikimedia.org/wikipedia/commons/transcoded/8/83/' +
//                 'Elephants_Dream_%28high_quality%29.ogv/' +
//                 'Elephants_Dream_%28high_quality%29.ogv.360p.webm',
//             type: 'video/webm',
//             poster: 'http://upload.wikimedia.org/wikipedia/commons/thumb/9/90/' +
//                 'Elephants_Dream_s1_proog.jpg/800px-Elephants_Dream_s1_proog.jpg'
//         },
//         {
//             title: 'LES TWINS - An Industry Ahead',
//             type: 'text/html',
//             youtube: 'zi4CIXpx7Bg'
//         },
//         {
//             title: 'KN1GHT - Last Moon',
//             type: 'text/html',
//             vimeo: '73686146',
//             poster: 'http://b.vimeocdn.com/ts/448/835/448835699_960.jpg'
//         }