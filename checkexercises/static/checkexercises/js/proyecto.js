//var github
//retocar css y mirar lo de la transparencia del div(si no, poner el mismo color
//de fondo) donde estan los botones
//o probar a meter una imagen de fondo y centrar los botones con bootstrap
profesor = ""
repostudent = ""
function reconfigurar(accion){
	console.log("accion = " + accion);
	if(accion == 0){
		$("button").prop('disabled', false);
		$("button.prohib").css("cursor","pointer")
		$("#botonurlgit").click(obtenerforks)
		$("#botonurlgit1").click(analizarepo)
		$("#botonlogin").click(login)
		$("#botonnewuser").click(newUser)
		$("#botondeluser").click(deluser)
		$("#errorcreate").hide()
		$("#progreso").hide()
		$("#hayglobal").hide()
		$("#form").show()
		$("#form1").show()
		$(".menu").each(function(){
			$( this ).menu();
		});
		$("#resumen1").show()
		$("#fichrepo").hide()
		console.log("antes del tab")
		$(".tab").each(function() {
		  $( this ).tabs();
		});
		$("#errorurl").hide()
		$(".ocult").show()
		$(".ocult1").hide()
		$(".ocult2").hide()
		$("#isautenticado").show()
		autentic = $("#isautenticado").html()
		console.log("autentic = " + autentic)
		if(autentic == "SI"){
			console.log("esta autenticado")
			$(".ocult1").show()
			noshowbot3 = $("#showbotonocult3").html()
			if(noshowbot3 == "False"){
				console.log(" SI mostrar boton repositories")
				$(".ocult3").show()
				nografic = false
			}else{
				console.log(" NO mostrar boton repositories")
				$(".ocult3").hide()
				nografic = true
			}
		}
		$("#isautenticado").hide()
		//$("#botondelete").click(deleteRepo)
		$("#botonfichNot").click(putLibrary)
		$("#botonDelfichNot").click(delLibrary)
		$(function() {
		    $('a.page-scroll').bind('click', function(event) {
		        var $anchor = $(this);
		        $('html, body').stop().animate({
		            scrollTop: $($anchor.attr('href')).offset().top
		        }, 1500, 'easeInOutExpo');
		        event.preventDefault();
		    });
		});

		//creo las graficas del repositorio de profesor general
		if(nografic == false){
			createGraphic($("#infoerror").html(),"graferror",true)
			createcompararGraphic($("#diferror").html(),$("#infoerrorGlobalname").html())
			$("#infoerrorGlobalname").hide()
			$("#legend").show()
			$("#infoerror").hide()
			$("#infonamerepo").hide()
		}			
	}else if(accion == 1){ //cuando doy a mainmenu,newlogin,newuser,putlibrary,deletelibrary muestro la pagina de inicio
		console.log("reconfiguro despues de borrar");
		$("button").prop('disabled', false);
		$("button.prohib").css("cursor","pointer")
		$("#botonurlgit").click(obtenerforks)
		$("#botonurlgit1").click(analizarepo)
		//$("#botondelete").click(deleteRepo)
		$("#botonfichNot").click(putLibrary)
		$("#botonDelfichNot").click(delLibrary)
		$("#botonlogin").click(login)
		$("#botonnewuser").click(newUser)
		$("#botondeluser").click(deluser)
		$("#errorcreate").hide()
		$("#progreso").hide()
		$("#form").show()
		$("#form1").show()
		$("#porcentaje").hide()
		$("#resumen1").hide()
		$("#fichrepo").hide()
		$("#errorurl").hide()
		$(".ocult").hide()
		$(".ocult1").hide()
		$(".ocult2").hide()
		//hacer una pequena trampa de escribir en un div si esta logueado, y luego ocultarlo
		$("#isautenticado").show()
		autentic = $("#isautenticado").html()
		console.log("autentic = " + autentic)
		if(autentic == "SI"){
			console.log("esta autenticado")
			$(".ocult1").show()
			//pequena trampa para mostrar la informacion global
			$("#hayglobal").show()
			hayglobal = $("#hayglobal").html()
			if(hayglobal == "SI"){
				$(".ocult2").show()
				createGraphicGlobal($("#infoerrorGlobal").html(),$("#infoerrorGlobalname").html(),$("#hayteacher").html())
				$("#infoerrorGlobal").hide()
				$("#infoerrorGlobalname").hide()
				$("#hayteacher").hide()
			}
		}
		$("#hayglobal").hide()
		$("#isautenticado").hide()
		$("#legend").hide()
		$(function() {
		    $('a.page-scroll').bind('click', function(event) {
		        var $anchor = $(this);
		        $('html, body').stop().animate({
		            scrollTop: $($anchor.attr('href')).offset().top
		        }, 1500, 'easeInOutExpo');
		        event.preventDefault();
		    });
		});

	}else if(accion == 2){ //cuando hago logout tengo que poner la pagina inicial
		console.log("entra por 2")
		$(".ocult").hide()
		$(".ocult1").hide()
		$(".ocult2").hide()
		$("#isautenticado").hide()
		$("#crearusuario").hide()
		$("#delusuario").hide()
		$("#delusuario").hide()
		$("#botonlogin").click(login)
		$("#botonnewuser").click(newUser)
		$("#botondeluser").click(deluser)
		$("#hayglobal").hide()
		$(function() {
		    $('a.page-scroll').bind('click', function(event) {
		        var $anchor = $(this);
		        $('html, body').stop().animate({
		            scrollTop: $($anchor.attr('href')).offset().top
		        }, 1500, 'easeInOutExpo');
		        event.preventDefault();
		    });
		});
		console.log("sale por 2")
	}
	
}

function analizarepo(repeatrepo, repeatrama,numorden){
	console.log("Esta pulsado rama = " + $('input:radio[name=optionsRadios]:checked').val())
	$("#errorurl").hide()
	console.log("entro a analizarepo")
	console.log("repeatrepo = " + repeatrepo)
	console.log("type of repeatrepo = " + typeof repeatrepo )
	if(typeof repeatrepo != 'string'){ //si es distinto de string es porque viene del formulario,si es string es porque he pulsao
		console.log("Repo " + $("#urlgit").val()) //en repos ya analizados
		var urlstudent = $("#urlgit").val();
		$("#urlgit").val(""); //quito la url del formulario
		urlsplit = urlstudent.split("/");
		console.log("urlsplit = " + urlsplit);
		if((urlsplit[0] == "https:") && (urlsplit[1] == "") &&
			(urlsplit[2] == "github.com") && (urlsplit[3] != "CursosWeb") && (urlsplit.length == 5)){
			descargar = true
			console.log("descargar")
		}else{
			console.log("NO descargar")
			descargar = false
		}
		if (descargar == true){
			github = new Github({});
			repo = github.getRepo(urlsplit[3], urlsplit[4]);
			hayrepo = true
			repo.show(function(err, repo1) {
				console.log("!!!!!!!!!type of repo1 = " + typeof repo1 )
				if(typeof repo1 == "undefined"){ //para comprobar si el repositorio existe
					console.log("repo es false")
					hayrepo = false
				}
				console.log("hayrepo = " + hayrepo)
				if(hayrepo == true){ //si repo existe y es de CursosWeb, es de profe
					//var myObject = JSON.stringify(repo1);
					//console.log("repo1 = " + myObject)
					//sconsole.log("repo1.owner.avatar_url = " + repo1.owner.avatar_url)
					$("#form").hide()
					$("#progreso").show()
					$("#barraprogreso").css( "width", "100%" ).html("ANALYZING REPOSITORY. WAIT FEW SECONDS PLEASE.");
					//deshabilitarboton de deleted
					$("button.prohib").prop('disabled', true);
					$("button.prohib").css("cursor","not-allowed")
					$.post("",{urlanalizstudent: urlstudent,
								rama: $('input:radio[name=optionsRadios]:checked').val(),
								urlavatar: repo1.owner.avatar_url
										},function(data){
										console.log("dentro de la funcion del POST de analizar estudiante")
										//ajaxHTTP.open("GET", "index");
										//ajaxHTTP.send()
										document.documentElement.innerHTML = data;//para actualizar el html
										reconfigurar(0);
										//creo la primera grafica de fichero para que se vea
										noshowbot3 = $("#showbotonocult3").html()
										if(noshowbot3 == "False"){
											createGraphic($("#graficfich1").html(),$("#graficfich1namediv").html(),false)
											$("#graficfich1").hide()
											$("#graficfich1namediv").hide()
										}
										$("#showbotonocult3").hide()
										
										console.log("despues del open post alumno")
					})
				}else{
					console.log("mostrar errorurl")
					$("#errorurl").show()
					$("#errorurl").html("<div id='errorurl1' class='alert alert-danger alert-dismissible' role='alert'><button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button><strong>Error!</strong> Repository's name is wrong</div><br>")
				}
			});
		}else{
			console.log("mostrar errorurl")
			$("#errorurl").show()
			$("#errorurl").html("<div id='errorurl1' class='alert alert-danger alert-dismissible' role='alert'><button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button><strong>Error!</strong> Repository's name is wrong</div><br>")
		}			
	}else{
		console.log("hay repeatrepo")
		$.post("",{urlrepeat: repeatrepo,
				   rama: repeatrama, num: numorden},function(data){
					console.log("dentro de la funcion del POST")
					//ajaxHTTP.open("GET", "index");
					//ajaxHTTP.send()
					document.documentElement.innerHTML = data;//para actualizar el html
					reconfigurar(0);
					//creo la primera grafica de fichero para que se vea
					noshowbot3 = $("#showbotonocult3").html()
					if(noshowbot3 == "False"){
						createGraphic($("#graficfich1").html(),$("#graficfich1namediv").html(),false)
						$("#graficfich1").hide()
						$("#graficfich1namediv").hide()
					}
					$("#showbotonocult3").hide()
					console.log("despues del open post repeatrepo alumno")
		})
	}
}

function mainMenu(){
	$.post("",{mainMenu: true},function(data){
				console.log("dentro de la funcion de mainmenu POST ")
				//ajaxHTTP.open("GET", "index");
				//ajaxHTTP.send()
				document.documentElement.innerHTML = data;//para actualizar el html
				reconfigurar(1);
				$("#crearusuario").hide()
				$("#delusuario").hide()
				console.log("despues del open post de la funcion de mainmenu")
	})
}

function deluser(){
	$("#autenticarse").hide()
	$("#errorcreate").hide()
	$("#crearusuario").hide()
	$("#delask").hide()
	$("#delusuario").show()
	$("#progreso1").hide()
	$("#botonreturn1").click(function(){
		$("#delusuario").hide()
		$("#autenticarse").show()	
	})
	$("#deluserdefinit").click(function(){ 
		nameUser = $("#nameuser2").val()
		console.log("nameUser = " + nameUser)
		key = document.getElementById("password3").value;
		console.log("key3 = " + key)
		if(nameUser != "" && key != ""){
			$("#delask").show()
			$("#delask").html("<strong>DANGER!</strong> are you sure you want to delete '"+nameUser+"'?<button id='deluserdefinit1'>YES</button><button id='deluserdefinit2'>NO</button>")
			$("#deluserdefinit1").click(function(){
				$("#delask").hide()
				$("#progreso1").show()
				$("#form4").hide()
				$.post("",{deluser: nameUser,delpassword: key},function(data){
							console.log("dentro de la funcion de delusuario POST ")
							//ajaxHTTP.open("GET", "index");
							//ajaxHTTP.send()
							document.documentElement.innerHTML = data;//para actualizar el html
							reconfigurar(2);
							//$("#autenticarse").show()
							console.log("despues del open post de la funcion de delusuario")
				})
			})
			$("#deluserdefinit2").click(function(){
				$("#delask").hide()
			})
		}else{
			$("#errordel").show()                              
			$("#errordel").html("<div id='errordel2' class='alert alert-warning alert-dismissible text1 mes1' role='alert'><button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button><strong>Warning!</strong> CHECK YOUR DATA</div><br>")
		}
	})	
}

function logout(){
	$.post("",{logoutuser: true},function(data){
				console.log("dentro de la funcion de logout POST ")
				//ajaxHTTP.open("GET", "index");
				//ajaxHTTP.send()
				document.documentElement.innerHTML = data;//para actualizar el html
				reconfigurar(2);
				console.log("despues del open post de la funcion de logout")
	})
}

function login(){
	nameUser = $("#namelogin").val()
	console.log("nameUser = " + nameUser)
	key = document.getElementById("password2").value;
	console.log("key = " + key)
	if(nameUser != "" && key != ""){
		$.post("",{loginuser: nameUser,loginpassword: key},function(data){
					console.log("dentro de la funcion de login POST ")
					//ajaxHTTP.open("GET", "index");
					//ajaxHTTP.send()
					document.documentElement.innerHTML = data;//para actualizar el html
					reconfigurar(1);
					$("#crearusuario").hide()
					$("#delusuario").hide()
					console.log("despues del open post de la funcion de login")
		})
	}else{
			$("#errorlog").show()                              
			$("#errorlog").html("<div id='errorlog1' class='alert alert-warning alert-dismissible text1 mes1' role='alert'><button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button><strong>Warning!</strong> CHECK YOUR DATA</div><br>")
	}
}

function newUser(){
	$("#autenticarse").hide()
	$("#errorcreate").hide()
	$("#crearusuario").show()
	$("#botonreturn").click(function(){
		$("#crearusuario").hide()
		$("#autenticarse").show()	
	})
	$("#botoncreate").click(function(){
		//comprobar si el usuario a metido bien los datos primero
		nameUser = $("#nameuser").val()
		console.log("nameUser = " + nameUser)
		email = $("#email").val()
		console.log("email = " + email)
		key = document.getElementById("password1").value;
		console.log("key = " + key)
		rol = $('input:radio[name=optionsRol]:checked').val()
		console.log("rol = " + rol)
		if(nameuser != "" && email != "" && key != ""){
			if(key.length >= 6){
				$.post("",{createuser: nameUser,createmail: email,createpassword: key,
					createrol: rol},function(data){
					console.log("dentro de la funcion de putlibrary POST ")
					//ajaxHTTP.open("GET", "index");
					//ajaxHTTP.send()
					document.documentElement.innerHTML = data;//para actualizar el html
					reconfigurar(1);
					$("#crearusuario").hide()
					$("#delusuario").hide()
					console.log("despues del open post de la funcion de create new user")
				})
			}else{
				$("#errorcreate").show()                              
				$("#errorcreate").html("<div id='errorcreate1' class='alert alert-warning alert-dismissible text1 mes1' role='alert'><button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button><strong>Warning!</strong> PASSWORD MUST CONTAIN 6 CHARACTERS MIN</div><br>")
			}
			
		}else{
			$("#errorcreate").show()                              
			$("#errorcreate").html("<div id='errorcreate1' class='alert alert-warning alert-dismissible text1 mes1' role='alert'><button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button><strong>Warning!</strong> CHECK YOUR DATA</div><br>")
		}		
	})
}

function putLibrary(){
	nameLibrary = $("#notAnalizefich").val()
	console.log("nameLibrary to save = " + nameLibrary)
	if(nameLibrary != ""){
		$.post("",{savelibrary: nameLibrary},function(data){
					console.log("dentro de la funcion de putlibrary POST ")
					//ajaxHTTP.open("GET", "index");
					//ajaxHTTP.send()
					document.documentElement.innerHTML = data;//para actualizar el html
					reconfigurar(1);
					console.log("despues del open post de la funcion de putLibrary")
		})
	}
}

function delLibrary(){
	nameLibrary = $("#notAnalizefich").val()
	console.log("nameLibrary to delete = " + nameLibrary)
	if(nameLibrary != ""){
		$.post("",{deletelibrary: nameLibrary},function(data){
					console.log("dentro de la funcion de putlibrary POST ")
					//ajaxHTTP.open("GET", "index");
					//ajaxHTTP.send()
					document.documentElement.innerHTML = data;//para actualizar el html
					reconfigurar(1);
					console.log("despues del open post de la funcion de putLibrary")
		})
	}
}

/*function deleteRepo(){ //creo que despues de borrar un repositorio mandar al usuario a la pagina principal
	repo = $("#repodelete").val()
	$("button.prohib").prop('disabled', true);
	$("button.prohib").css("cursor","not-allowed")
	$("#repodelete").val("");
	$("#form1").hide()
	$("#progreso1").show()
	console.log("repo a borrar = "+ repo)
	if(repo == ""){
		repo = "0"
	}		
	$.post("",{repodelete: repo,
				rama: $('input:radio[name=optionsRadios1]:checked').val()},function(data){
					console.log("dentro de la funcion de deleteRepo POST ")
					//ajaxHTTP.open("GET", "index");
					//ajaxHTTP.send()
					document.documentElement.innerHTML = data;//para actualizar el html
					reconfigurar(1);
					console.log("despues del open post de la funcion de deleteRepo")
	})
}*/

function createcompararGraphic(info,user){
	console.log("entro en CREATECOMPARARGRAPHIC -------------------------------------")
	if(info != ""){
		arraydat = info.split("errorspace")
		datosvalores = []
		datosnombres = []
		
		console.log("len arraydat" + arraydat.length)
		console.log("arraydat = " + arraydat);
		nummax = 0;
		nummin = 0;
		for(i=0;i<arraydat.length-1;i++){ //creo el array de datos que le paso al objeto json
			console.log("arraydat["+i+"] = " + arraydat[i]);
			console.log("arraydat["+(i+1)+"] = " + arraydat[i+1]);
			datosnombres.push(arraydat[i])
			datosvalores.push(parseInt(arraydat[i+1]))
			if(parseInt(arraydat[i+1]) > nummax){
				nummax = parseInt(arraydat[i+1])
			}
			if(parseInt(arraydat[i+1]) < nummin){
				nummin = parseInt(arraydat[i+1])
			}
			i = i + 1
		}
		console.log("nummax antes = " + nummax)
		salir = false
		cont = 2000
		while(salir == false){ //bucle para fijar el umbral de la grafica
			if(nummax >= cont){
				nummax = cont + 50 //cojo el umbral por arriba
				salir = true
			}
			cont = cont - 50
		}
		console.log("nummax despues = " + nummax)
		console.log("nummin antes = " + nummin)
		salir = false
		cont = -2000
		while(salir == false){ //bucle para fijar el umbral de la grafica
			if(nummin <= cont){
				nummin = cont - 50 //cojo el umbral por arriba
				salir = true
			}
			cont = cont + 50
		}
		console.log("nummin despues = " + nummin)
		//console.log("datos nombres = " + datosnombres)
		objectjson = { //para la grafica de los errores
		        chart: {
		            type: 'column'
		        },
		        title: {
		            text: 'Errors\' difference'
		        },
		        yAxis: {
		            min: parseInt(nummin),
		            max: parseInt(nummax),
		            title: {
		                text: 'Number of errors'
		            }
		        },
		        xAxis: {
		            categories: datosnombres
		        },
		        credits: {
		            enabled: false
		        },
		        series: [{
		            name: user,
		            data: datosvalores
		        }]
		    }
		$('#diferror').highcharts(objectjson);
	}else{
		$('#diferror').html("NO ERRORS TO COMPARE")
	}
	console.log("despues de createcompararGraphicG")
} 

function createGraphic(info, id,is_repo_teacher){
	console.log("entro en CREATEGRAPHIC -------------------------------------")
	console.log("is_repo_teacher = " + is_repo_teacher)
	console.log("id es = " + id)
	console.log("infoerrores despues de borrar es = " + $('div.infoerrores').html())
	console.log("LA INFO ES ///////////////////////////////////////////////////")
	console.log(info)
	console.log("FIN LA INFO ES ///////////////////////////////////////////////////")
	datos = info;
	arraydat = datos.split("errorspace")
	arraydatos = []
	console.log("len arraydat" + arraydat.length)
	console.log("arraydat = " + arraydat);
	//data = ""
	nummax = 0;
	if(is_repo_teacher == true){
		empiece = 0
	}else{
		empiece = 1
	}
	console.log("empiece = "+ empiece)
	cambiarTool = false
	for(i=empiece;i<arraydat.length-1;i++){ //creo el array de datos que le paso al objeto json
		console.log("arraydat["+i+"] = " + arraydat[i]);
		console.log("arraydat["+(i+1)+"] = " + arraydat[i+1]);
		if(arraydat[i] == "JSHint"){
			cambiarTool = true
			i++ //subo uno porque el otro lo sube en el bucle,tengo que subir de dos en dos
		}else{
			if(cambiarTool == false){
				if(parseInt(arraydat[i+1]) > nummax){
					nummax = parseInt(arraydat[i+1])
				}
				dato = {name: arraydat[i],color: "blue", y: parseInt(arraydat[i+1])} //esto es por la forma en que highcharts recibe data(array de arrays)
				arraydatos.push(dato)
				i++ //subo uno porque el otro lo sube en el bucle,tengo que subir de dos en dos
			}else{
				if(parseInt(arraydat[i+1]) > nummax){
					nummax = parseInt(arraydat[i+1])
				}
				dato = {name: arraydat[i],color: "red", y: parseInt(arraydat[i+1])} //esto es por la forma en que highcharts recibe data(array de arrays)
				arraydatos.push(dato)
				i++ //subo uno porque el otro lo sube en el bucle,tengo que subir de dos en dos
			}
		}
	}
	//console.log("arraydatos = " + arraydatos)
	console.log("nummax antes = " + nummax)
	salir = false
	if(is_repo_teacher == true){ //si es de profesor
		cont = 2000
		while(salir == false){ //bucle para fijar el umbral de la grafica
			if(nummax >= cont){
				nummax = cont + 50 //cojo el umbral por arriba
				salir = true
			}
			cont = cont - 50
		}
	}else{ //si es de fichero de alumno
		cont = 100
		while(salir == false){ //bucle para fijar el umbral de la grafica
			if(nummax == 100){
				salir = true
			}else if(nummax >= cont){
				nummax = cont + 10 //cojo el umbral por arriba
				salir = true
			}
			cont = cont - 10
		}
	}
	console.log("nummax despues = " + nummax)
	if(is_repo_teacher == true){
		title = 'Student\'s Errors'
		subtitle = $("#infonamerepo").html()
	}else{
		title = arraydat[0] +'\'s Errors'
		subtitle = ""
	}
	//console.log("arraydatos1 = " + arraydatos1)
	objectjson = { //para la grafica de los errores
	        chart: {
	            type: 'column',
	            backgroundColor: '#FFFAFA'  //#FDF5E6 otro color que me gustaba de fondo
	        },
	        title: {
	            text: title
	        },
	        subtitle: {
	            text: subtitle
	        },
	        xAxis: {
	            type: 'category',
	            labels: {
	                rotation: -45,
	                style: {
	                    fontSize: '13px',
	                    fontFamily: 'Verdana, sans-serif'
	                }
	            }
	        },
	        yAxis: {
	            min: 0,
	            max: parseInt(nummax),
	            title: {
	                text: 'Number of errors'
	            }
	        },
	        legend: {
	        	enabled: false
	        },
	        tooltip: {
	            pointFormat: 'Errors: <b>{point.y}</b>'
	        },
	        series: [{
	            name: 'JSLint',
	            data: arraydatos,
	            dataLabels: {
	                enabled: true,
	                rotation: -90,
	                color: '#FFFFFF',
	                align: 'right',
	                format: '{point.y}', // one decimal
	                y: 10, // 10 pixels down from the top
	                style: {
	                    fontSize: '13px',
	                    fontFamily: 'Verdana, sans-serif'
	                }
	            },
	        }]
	    }
	    //document.getElementById(id).innerHTML = highcharts(objectjson)
	    $('[id^="'+id+'"]').highcharts(objectjson);
		//$('div.infoerrores').highcharts(objectjson);
		console.log("FIN DE CREATEGRAPHIC-------------------------------------")
}  

function createGraphicGlobal(info,user,isteacher){
	console.log("entro a createGraphicGlobal")
	arraydat = info.split("errorspace")
	datosvalores = []
	datosnombres = []
	if(isteacher == "SI"){ //esta parte la podre quitar si veo que al final no la uso junto al isteacher y lo que conlleva
		title = "STUDENTS' EVOLUTION"
	}else{
		title = user + "'S EVOLUTION"
	}
	

	console.log("len arraydat" + arraydat.length)
	console.log("arraydat = " + arraydat);
	for(i=0;i<arraydat.length-1;i++){ //creo el array de datos que le paso al objeto json
		console.log("arraydat["+i+"] = " + arraydat[i]);
		console.log("arraydat["+(i+1)+"] = " + arraydat[i+1]);
		datosnombres.push(arraydat[i])
		datosvalores.push(parseInt(arraydat[i+1]))
		i = i + 1
	}
	objectjson = { //para la grafica de los errores
		chart: {
            type: 'line'
        },
		title: {
            text: '',
            x: -20 //center
        },
        subtitle: {
            text: '',
            x: -20
        },
     	xAxis: {
            categories: datosnombres
        },
        yAxis: {
            title: {
                text: 'Errors'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            valueSuffix: ' errors'
        },
        legend: {
            layout: 'vertical',
            align: 'center',
            verticalAlign: 'bottom',
            borderWidth: 0
        },
        plotOptions: {
            line: {
                dataLabels: {
                    enabled: true
                },
                enableMouseTracking: true
            }
        },
        series: [{
            name: user,
            data: datosvalores
        }]
	}
	$('#graferrorGlobal').highcharts(objectjson);
	console.log("despues de createGraphicGlobals")
}


function obtenerforks(repeatrepo, repeatrama, numorden){
	console.log("Esta pulsado rama = " + $('input:radio[name=optionsRadios]:checked').val())
	$("#errorurl").hide()
	console.log("entro a obtenerforks")
	console.log("repeatrepo = " + repeatrepo)
	console.log("type of repeatrepo = " + typeof repeatrepo )
	if(typeof repeatrepo != 'string'){ //si es distinto de string es porque viene del formulario,si es string es porque he pulsao
		console.log("Repo " + $("#urlgit").val()) //en repos ya analizados
		var urlteach = $("#urlgit").val();
		$("#urlgit").val(""); //quito la url del formulario
		profesor = urlteach; //creo que ya no necesito la variable profesor
		urlsplit = urlteach.split("/");
		console.log("urlsplit = " + urlsplit);
		if((urlsplit[0] == "https:") && (urlsplit[1] == "") &&
			(urlsplit[2] == "github.com") && (urlsplit[3] == "CursosWeb")){
			descargar = true
			console.log("descargar")
		}else{
			console.log("NO descargar")
			descargar = false
		}
		if (descargar == true){
			github = new Github({});
			repo = github.getRepo(urlsplit[3], urlsplit[4]);
			hayrepo = true
			repo.show(function(err, repo1) {
				console.log("!!!!!!!!!type of repo1 = " + typeof repo1 )
				if(typeof repo1 == "undefined"){ //para comprobar si el repositorio existe
					console.log("repo es false")
					hayrepo = false
				}
				console.log("hayrepo = " + hayrepo)
				if(hayrepo == true){ //si repo existe y es de CursosWeb, es de profe
					$("#form").hide()
					$("#progreso").show()
					$("#barraprogreso").css( "width", "100%" ).html("ANALYZING REPOSITORY. WAIT FEW SECONDS PLEASE.");
					//deshabilitarboton de deleted
					$("button.prohib").prop('disabled', true);
					$("button.prohib").css("cursor","not-allowed")
					var arrayforks = ""
					repo.listForks(function(err, forks) {
						console.log("num forks = " + forks.length);
						//console.log("giturl : "+forks[0].git_url)
						//copyfich(forks[0].svn_url)//forks[0].svn_url
						for(i=0;i<forks.length;i++){ //este bucle lo tengo que hacer para copyfich() para cada alumno
							console.log("fork = "+forks[i]);
							console.log("fork "+i+" =" +forks[i].svn_url);
							if(i != forks.length - 1){
								console.log("avatar url = " + forks[i].owner.avatar_url)
								arrayforks += forks[i].svn_url+","+forks[i].owner.avatar_url +","
							}else{
								arrayforks += forks[i].svn_url +","+forks[i].owner.avatar_url //es el ultimo no hace falta la coma
							}
						}
						console.log("arrayforks  = " + arrayforks)
						repostudent = arrayforks.split(",")
						$.post("",{urlanalizall: urlteach,
										listForks : arrayforks,
											rama: $('input:radio[name=optionsRadios]:checked').val()
											},function(data){
											console.log("dentro de la funcion del POST")
											//ajaxHTTP.open("GET", "index");
											//ajaxHTTP.send()
											document.documentElement.innerHTML = data;//para actualizar el html
											reconfigurar(0);
											$("#showbotonocult3").hide()
											console.log("despues del open post")
						})
					});
				}else{
					console.log("mostrar errorurl")
					$("#errorurl").show()
					$("#errorurl").html("<div id='errorurl1' class='alert alert-danger alert-dismissible' role='alert'><button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button><strong>Error!</strong> Repository's name is wrong</div><br>")
				}
			});
		}else{
			console.log("mostrar errorurl")
			$("#errorurl").show()
			$("#errorurl").html("<div id='errorurl1' class='alert alert-danger alert-dismissible' role='alert'><button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button><strong>Error!</strong> Repository's name is wrong</div><br>")
		}			
	}else{
		console.log("hay repeatrepo")
		urlteach = repeatrepo
		$.post("",{urlrepeat: urlteach,
				   rama: repeatrama, num: numorden},function(data){
					console.log("dentro de la funcion del POST")
					//ajaxHTTP.open("GET", "index");
					//ajaxHTTP.send()
					document.documentElement.innerHTML = data;//para actualizar el html
					reconfigurar(0);
					$("#showbotonocult3").hide()
					console.log("despues del open post")
		})
	}
}

/*jQuery(document).ready(function() {
	console.log("estoy en el js para barra progreso en bootstrap");
	$("#botonurlgit").click(obtenerforks)
	$("#botondelete").click(deleteRepo)
	$("#botonfichNot").click(putLibrary)
	$("#botonDelfichNot").click(delLibrary)
	$("#progreso").hide()
	$("#progreso1").hide()
	$("#porcentaje").hide()
	$("#resumen1").hide()
	$("#fichrepo").hide()
	$("#errorurl").hide()
	$(".ocult").hide()
	$("#legend").hide()
}); */

jQuery(document).ready(function() {
	$(".ocult").hide()
	$(".ocult1").hide()
	$(".ocult2").hide()
	$("#isautenticado").hide()
	$("#crearusuario").hide()
	$("#delusuario").hide()
	$("#botonlogin").click(login)
	$("#botonnewuser").click(newUser)
	$("#botondeluser").click(deluser)
	$("#hayglobal").hide()
});