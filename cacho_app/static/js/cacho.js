// socket.io specific code
// funciones de socket del cliente.

// variables globales
// sessid mantiene el session id, proveido por el servidor (gevent-socketio)
var socket = io.connect("/game");
var sessid;
var user_list;

// conversion de numeros, jugadas (tuplas) a frases
var numeros = ['ningun', 'un', 'dos', 'tres', 'cuatro', 'cinco',
					'seis', 'siete', 'ocho', 'nueve', 'diez', 'once',
					'doce', 'trece', 'catorce', 'quince', 'dieciseis',
					'diecisiete', 'dieciocho', 'diecinueve', 'veinte']
var pintas = ['0', 'aces', 'tontos', 'trenes', 'cuartas', 'quintas', 'sextas']

// conexion al servidor
socket.on('connect', function (username) {
   $('#chat').addClass('connected');
   socket.emit('join', window.room);
});

// guardar el sessid al obtenerlo.
socket.on('user_sessid', function(id) {
	sessid = id;
});

// llego un turno, la variable turno
// es el sessid del jugador con el turno
socket.on('turno', function(turno) {
	socket.emit('get_dados');
	// es mi turno
	socket.emit('check_winner');
	if (turno == sessid) {
		alert_info("te toca a ti oeh","success");
		socket.emit('get_jugadas_posibles');
		$('#input-jugadas').show();		
	} 
		// poner icono de estrella al usuario con turno
		// recorrer la userlist y modificar el HTML id
		$.each(user_list, function (k, v) {
			$('#'+v['user_name']+"-icon").removeClass("icon-star");
			if (v['sessid'] == turno) {
				alert_info("El turno es de "+v['user_name'],"info");
				$('#'+v['user_name']+"-icon").addClass("icon-star");
			}
		});
	
});

// llega una lista de usuarios con informacion
// user_name, estado de confirmacion, sessid y user_id
socket.on('usuarios_room', function (usernames) {
	user_list = usernames;
    $('#userlist').empty();

	 $.each(user_list, function(k, v) {
		 if (v['confirm']) 
			$('#userlist').append('<li id="'+ v['user_name'] +'">'+v['user_name']+' <i id="'+v['user_name']+'-icon" class="icon-ok"></i></li>');
		 else
			$('#userlist').append('<li id="'+ v['user_name'] +'">'+v['user_name']+' <i id="'+v['user_name']+'-icon" class="icon-remove"></i></li>');
	 });
});

// llega una lista de jugadas posibles
// poblar el formulario con tales jugadas
socket.on('jugadas_posibles', function(jugadas,not_first) {
	$('#jugadas').empty();

	// no es la primera jugada
	if(not_first){
		$('#jugadas').append('<option value="[0,0]">Calzo</option>');
		$('#jugadas').append('<option value="[0,1]">Dudo</option>');
		}
	$.each(jugadas, function(k, v) {
		$('#jugadas').append('<option value="['+v[0]+','+v[1]+']">'+numeros[v[0]]+' '+pintas[v[1]]+'</option>');
	});
});

// llegaron los dados del usuario,
// mostrar imagenes de los dados
socket.on('dados_user', function(dados) {
	$('#dados').empty();
	$.each(dados, function(k, v) {
		$('#dados').append('<img src="/static/img/die_face_'+v+'.png" /> ');
	});
});

// el servidor dijo que el jugador perdio,
// hacer desaparecer el formulario y los dados
socket.on('player_lost', function() {
	$('#jugadas').empty();
	$('#dados').empty();
});

// llego el evento revolver_dados
socket.on('winner', function(ganador) {
	alert_info("El ganador es "+ganador,"info");
	$('#input-jugadas').hide();
	$('#salir').show();		
});

socket.on('revolver_dados', function() {
	socket.emit('revolver');
	socket.emit("get_dados");
});

// llego un mensaje del servidor, mostrarlo en un
// alert, mediante alert_info
socket.on('server_message', function (data) {
	alert_info(data, 'info');

	// si el mensaje es todos confirmaron, esconder
	// el boton de confirmar
	if (data == 'todos_confirmaron') {
		$('#confirmar').hide();	

		$.each(user_list, function(k, v) {
			$('#'+v['user_name']+'-icon').removeClass("icon-ok");
		});
	}
});

// llego un anuncio, mostrarlo en el chat
socket.on('announcement', function (msg) {
    $('#lines').append($('<p>').append($('<em>').text(msg)));
});

// ejecutar la funcion message cuando llegue
// un mensaje de un usuario
socket.on('msg_to_room', message);

// reconectar al servidor
socket.on('reconnect', function () {
    $('#lines').remove();
    message('cacho: ', 'r');
});

socket.on('reconnecting', function () {
    alert_info('reconectando al servidor','alert');
});

// mostrar un error que llego
socket.on('error', function (e) {
    alert_info(e ? e : 'error del servidor!', 'error');
});

// mostrar un mensaje en el chat
function message (from, msg) {
    $('#lines').append($('<p>').append($('<b>').text(from), msg));
}

// mostrar un mensaje en el cuadro de alerta
// type=error, succcess, info
function alert_info(msg, type) {
	$('#alerts').empty();
	$('#alerts').addClass("alert-" + type);
	$('#alerts').append('<h4>' + msg + '</h4>');
	$('#alerts').show();
}

// funciones de botones
$(function () {
	// enviar un mensaje por el chat
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

	// click en el boton confirmar enviara el mensaje confirmar al servidor
	 $('#confirmar').click(function () {
		socket.emit('confirmar', 'YES');
//		alert('CONFIRMEICHON');
	 });

	// envio de jugadas
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
		location.href="/play/";
	});

	$('#calzo').click(function () {
		socket.emit('jugada', '[0,0]');
	});
});
