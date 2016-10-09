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
				<textarea id="consoletext" style="width:100%;max-height:100%;min-height:100%;resize:none" disabled="true"></textarea>
			</div>
		</div>
		<div id="input" style="width:100%;height:10%;border:all=1px;border-style:solid;display:inline-block">
			<div id="commandline" style="padding:1%">
				<label>Input nao command:</label>
				<input type="text" id="textinput" style="width:90%"></input>
				<button type="button" id="submitbutton" style="float:right;width:10%"">
					Submit
				</button>
				<script type="text/javascript">
					$(function()
					 	{
							document.getElementById('submitbutton').onclick =
								function() 
								{
									alert('test!');
								};
						});
				</script>
		</div>
	</body>
</html>