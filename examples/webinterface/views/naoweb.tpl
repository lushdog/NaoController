<html>
	<head>
		<title>
			Nao Web
		</title>
	<body style="margin:1%;padding:1%">
		%from bottle import url
		<script src="{{url('/static/<filename:path>', filename='jquery-3.1.1.min.js') }}"></script>
		<div id="camera" style="width:50%;height:70%;border:all=1px;border-style:solid;float:left;"><img alt="Top Camera"></img></div>
		<div id="camera" style="width:50%;height:70%;border:all=1px;border-style:solid;margin-left:50%"><img alt="Bottom Camera"></div></div>
		<div id="output" style="width:100%;height:20%;border:all=1px;border-style:solid;display:inline-block;">
			<div id="console">
				<div id="consoletext" style="width:100%;height:100%;overflow-y:auto"></div>
			</div>
		</div>
		<div id="input" style="width:100%;height:10%;border:all=1px;border-style:solid;display:inline-block">
			<div id="commandline" style="padding:1%" style="display:none;">
				<label>Input nao command:</label>
				<input type="text" id="textinput" style="width:90%"></input>
				<button type="button" id="submitbutton" style="float:right;width:10%" onclick="submit();">
					Submit
				</button>
				<script type="text/javascript">
				
								function submit() 
								{
									var input = $("#textinput").val().trim();
									if (input == '') return;
									$.ajax({
										  type: "POST",
										  contentType: "application/json; charset=utf-8",
										  url: "/command",
										  data: "{\"command\":\""+input+"\"}",
										  dataType: "text",
										}).done( function(console_output) { 
											var console = $("#consoletext")
											console.append("<pre>" + console_output + "</pre>"); 
											console.scrollTop(console.prop('scrollHeight'));
										});
								}
							/*2 timers, one for each GET to camera image after we see the naoconnected cookie is = 1
							/*<img src="data:image/png:base64,' + contents + ' />"*/
				</script>
			</div>
		</div>
	</body>
</html>