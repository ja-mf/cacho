// socket.io specific code
// funciones de socket del cliente.
var socket = io.connect("/game");
var sessid;
var user_list;

socket.on('connect', function (username) {
   $('#chat').addClass('connected');
   socket.emit('join', window.room);
});

socket.on('user_sessid', function(id) {
	sessid = id;
//	alert(sessid);
});

socket.on('turno', function(turno) {
//	alert(turno);
	if (turno == sessid) {
		alert("mi turno");
		// es el turno de este cliente
		// poblar el select box
	} else {
		$.each(user_list, function (k, v) {
			$('#'+v['user_name']).removeClass("turno");
			if (v['sessid'] == turno) {
				$('#'+v['user_name']).addClass("turno");
			}
		});
	}
});

socket.on('usuarios_room', function (usernames) {
	user_list = usernames;
    $('#userlist').empty();
//	 alert(JSON.stringify(usernames));

	 $.each(usernames, function(k, v) {
		$('#userlist').append('<li id="'+ v['user_name'] +'">'+v['user_name']+' '+v['confirm']+'</li>');
	 });
});

socket.on('server_message', function (data) {
	alert(data)
});

socket.on('announcement', function (msg) {
    $('#lines').append($('<p>').append($('<em>').text(msg)));
});

socket.on('msg_to_room', message);

socket.on('reconnect', function () {
    $('#lines').remove();
    message('cacho: ', 'r');
});

socket.on('reconnecting', function () {
    message('cacho', 'reconectando al servidor');
});

socket.on('error', function (e) {
    message('cacho:', e ? e : 'error del servidor!');
});

function message (from, msg) {
    $('#lines').append($('<p>').append($('<b>').text(from), msg));
}

$(function () {
    $('#send-message').submit(function () {
	    message('me', $('#message').val());
	    socket.emit('user message', $('#message').val());
	    clear();
	    $('#lines').get(0).scrollTop = 10000000;
	    return false;
    });

    function clear () {
        $('#message').val('').focus();
    };

	 $('#confirmar').click(function () {
		socket.emit('confirmar', 'YES');
//		alert('CONFIRMEICHON');
	 });
});
