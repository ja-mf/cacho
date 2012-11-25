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
	socket.emit('check_winner');
	if (turno == sessid) {
		alert_info("te toca a ti oeh","success");
		socket.emit('get_jugadas_posibles');
		$('#input-jugadas').show();		
	} 
		$.each(user_list, function (k, v) {
			$('#'+v['user_name']+"-icon").removeClass("icon-star");
			if (v['sessid'] == turno) {
				alert_info("el turno es de "+v['user_name'],"info");
				$('#'+v['user_name']+"-icon").addClass("icon-star");
			}
		});
	
});

socket.on('usuarios_room', function (usernames) {
	user_list = usernames;
    $('#userlist').empty();
//	 alert(JSON.stringify(usernames));

	 $.each(user_list, function(k, v) {
		 if (v['confirm']) 
			$('#userlist').append('<li id="'+ v['user_name'] +'">'+v['user_name']+' <i id="'+v['user_name']+'-icon" class="icon-ok"></i></li>');
		 else
			$('#userlist').append('<li id="'+ v['user_name'] +'">'+v['user_name']+' <i id="'+v['user_name']+'-icon" class="icon-remove"></i></li>');
	 });
});

socket.on('jugadas_posibles', function(jugadas,not_first) {
	$('#jugadas').empty();
	if(not_first){
		$('#jugadas').append('<option value="[0,0]">Calzo</option>');
		$('#jugadas').append('<option value="[0,1]">Dudo</option>');
		}
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

socket.on('player_lost', function() {
	$('#jugadas').empty();
	$('#dados').empty();
});

socket.on('winner', function(ganador) {
	alert_info("El ganador es "+ganador,"info");
	$('#input-jugadas').hide();
	$('#salir').show();		
});

socket.on('revolver_dados', function() {
	socket.emit('revolver');
	socket.emit("get_dados");
});

socket.on('server_message', function (data) {
	alert_info(data, 'info');
	if (data == 'todos_confirmaron') {
		$('#confirmar').hide();	

		$.each(user_list, function(k, v) {
			$('#'+v['user_name']+'-icon').removeClass("icon-ok");
		});
	}
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
    alert_info('reconectando al servidor','alert');
});

socket.on('error', function (e) {
    alert_info(e ? e : 'error del servidor!', 'error');
});

function message (from, msg) {
    $('#lines').append($('<p>').append($('<b>').text(from), msg));
}

// type=error, succcess, info
function alert_info(msg, type) {
	$('#alerts').empty();
	$('#alerts').addClass("alert-" + type);
	$('#alerts').append('<h4>' + msg + '</h4>');
	$('#alerts').show();
}

$(function () {
    $('#send-message').submit(function () {
	    message('yo', $('#message').val());
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
		 var j = $.parseJSON($('#jugadas').val());
		 message('jugada',  numeros[j[0]] + " " + pintas[j[1]]);
		 socket.emit('jugada', $('#jugadas').val());
		 socket.emit('user message', numeros[j[0]] + " " + pintas[j[1]]);
		 $('#input-jugadas').hide();
	 });
	$('#dudo').click(function () {
		socket.emit('jugada', '[0,1]');
	});
	
	$('#salir').click(function () {
		location.href="http://localhost:8000/play/";
	});

	$('#calzo').click(function () {
		socket.emit('jugada', '[0,0]');
	});
});
