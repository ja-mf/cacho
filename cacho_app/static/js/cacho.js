// socket.io specific code
// funciones de socket del cliente.
var socket = io.connect("/game");
var sessid;
var user_list;

var numeros = ['ningun', 'un', 'dos', 'tres', 'cuatro', 'cinco',
					'seis', 'siete', 'ocho', 'nueve', 'diez', 'once',
					'doce', 'trece', 'catorce', 'quince', 'dieciseis',
					'diecisiete', 'dieciocho', 'diecinueve', 'veinte']
var pintas = ['0', 'aces', 'tontos', 'trenes', 'cuartas', 'quintas', 'sextas']

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
	socket.emit('get_dados');
	if (turno == sessid) {
		message("server", "mi turno");
		socket.emit('get_jugadas_posibles');
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
		 if (v['confirm']) 
			$('#userlist').append('<li id="'+ v['user_name'] +'"><i class="icon-ok"></i> '+v['user_name']+'</li>');
		 else
			$('#userlist').append('<li id="'+ v['user_name'] +'"><i class="icon-remove"></i> '+v['user_name']+'</li>');
	 });
});

socket.on('jugadas_posibles', function(jugadas) {
	$('#jugadas').empty();
	$('#jugadas').append('<option value="[0,0]">Calzo</option>');
	$('#jugadas').append('<option value="[0,1]">Dudo</option>');
	$.each(jugadas, function(k, v) {
		$('#jugadas').append('<option value="['+v[0]+','+v[1]+']">'+numeros[v[0]]+' '+pintas[v[1]]+'</option>');
	});
});

socket.on('dados_user', function(dados) {
	$('#dados').empty();
	$.each(dados, function(k, v) {
		$('#dados').append('<img src="/static/img/die_face_'+v+'.png" /> ');
	});
});

socket.on('revolver_dados', function() {
	socket.emit('revolver');
	socket.emit("get_dados");
});

socket.on('server_message', function (data) {
	message('server', data);
	if (data == 'todos_confirmaron')
		$('#confirmar').hide();
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

	 $('#jugar').click(function() {
		 message('debug',$('#jugadas').val());
		 socket.emit('jugada', $('#jugadas').val());
		socket.emit('user message', $('#jugadas').val());
	 });
	$('#dudo').click(function () {
		socket.emit('jugada', '[0,1]');
	});

	$('#calzo').click(function () {
		socket.emit('jugada', '[0,0]');
	});
});
