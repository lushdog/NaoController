<html>
	<head>
		<title>
			Nao Web
		</title>
	<body style="padding:1%">
		%from bottle import url
		<script src="{{url('/static/<filename:path>', filename='jquery-3.1.1.min.js')}}"></script>
		<script src="{{url('/static/<filename:path>', filename='js.cookie.js')}}"></script>
		<div id="top_camera" style="width:50%; height:70%; border-bottom:1px; border-top:1px; border-left:1px; border-right:0px; border-style:solid; float:left;"></div>
		<div id="bottom_camera" style="width:50%; height:70%; border:1px; border-style:solid; margin-left:50%"></div>
		<div id="output" style="width:100%; height:20%; border:1px; border-style:solid; display: inline-block; background-color:#000000; color:#EEEEEE;">
			<div id="console" style="padding-left:1%">
				<div id="consoletext" style="width:100%; height:100%; overflow-y:auto;">
					<pre>Nao output:</pre>
				</div>
			</div>
		</div>
		<div id="input" style="width:100%; height:10%; border:1px; border-style:solid; display:inline-block; font-family:monospace">
			<div id="commandline" style="padding:1%">
				<label>Input nao command below:</label>
				<input type="text" id="textinput" style="width:90%; font-family:monospace"></input>
				<button type="button" id="submitbutton" style="float:right; width:10%; font-family:monospace" onclick="submit();">
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
						}).done(function(console_output) { 
							var console = $("#consoletext")
							console.append("<pre>" + console_output + "</pre>"); 
							console.scrollTop(console.prop('scrollHeight'));
							var cookie = Cookies.get('naoconnected');
								if (cookie == '1')  {
									setInterval(function() {
										$.ajax({
											type: "GET",
											url: "/camera",
											dataType: "text",
										}).done(function(image_in_base_64) {
												$("#top_camera > img").remove();
												$("#top_camera").append("<img style='max-width: 100%; height: auto; border:none' alt='Top Camera' src='data:image/png;base64," + image_in_base_64 +"'/>");
											});
										$.ajax({
											type: "GET",
											url: "/camera/bottom",
											dataType: "text",
										}).done(function(image_in_base_64) {
												$("#bottom_camera > img").remove();
												$("#bottom_camera").append("<img style='max-width:100%; height:auto; border:none' alt='Bottom Camera' src='data:image/png;base64," + image_in_base_64 +"'/>");
											});
									}, 5000); 
								}
							});
					}
				</script>
			</div>
		</div>
	</body>
</html>