var http = require('http');
var fs = require('fs');
var amqp = require('amqp');

var server = http.createServer(function(req, res) {
  console.log("server started")
}).listen(9043, '0.0.0.0');

server.on('error', function (e) {
  // Handle your error here
  console.log(e);
});

var io = require('socket.io').listen(server);
var io_socket;
io.sockets.on('connection', function (socket) {
  io_socket = socket;
});



var connection = amqp.createConnection({ url: 'amqp://pYaTrAuSeR:uSerpYAtra089@localhost:5672/pyatrarabbitmqvhost' });

connection.on('ready', function(){
  connection.queue('my-queue', {autoDelete: false, durable: true}, function(queue){
    queue.subscribe({ack: true, prefetchCount: 1}, function(msg){
      var body = msg.data.toString('utf-8');
      console.log(body)
      var json_body = JSON.parse(body)
      console.log(json_body)
      if(json_body.render_process_status != undefined){
        setTimeout(function(){
          if(io_socket != undefined){
            var channel = 'progresschannel'
            io_socket.emit(channel, body);
          }
          queue.shift();
        }, (body.split('.').length - 1) * 1000);
      }
    });
  });
});