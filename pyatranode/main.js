var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var ZongJi = require('zongji');
var dsn = {
  host:     'localhost',
  user:     'root',
  password: 'pyatrapass098',
  database: 'pyatra'
};
var zongji = new ZongJi(dsn);


io.on('connection', function(socket){
  console.log('a user connected');
});

http.listen(3000, function(){
  console.log('listening on *:3000');
});

zongji.on('binlog', function(evt) {
  if(evt._hasTwoRows){
    for(var tableId in evt.tableMap){
      if(evt.tableMap[tableId]['tableName'] == 'yatra_app_videosession'){
        for(row in evt.rows){
          if(evt.rows[row]['before']['rendering_started'] == 0 && evt.rows[row]['after']['rendering_started'] == 1){
            console.log("ROW CHANGED for video_session_id" + evt.rows[row]['after']['id']);
            io.emit('some event', { for: 'everyone' });
          }
          if(evt.rows[row]['before']['final_video'] == '' && evt.rows[row]['after']['final_video'] != ''){
            console.log("ROW CHANGED for video_session_id" + evt.rows[row]['after']['final_video']);
            io.emit('some event', {for:  evt.rows[row]['before']['id'], final_video:  evt.rows[row]['after']['final_video']})
          }

        }
      }
    }
  }
});

zongji.on('query', function(evt){
  console.log("event");
  console.log(evt);
});
zongji.start({
  includeEvents: ['tablemap', 'writerows', 'updaterows', 'deleterows']
});

process.on('SIGINT', function() {
  console.log('Got SIGINT.');
  zongji.stop();
  process.exit();
});