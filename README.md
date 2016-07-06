# NaoController
Command line interface that can perform basic actions on the Nao robot.

INVOKING THE SCRIPT

Invoke via command line: 'python naocontroller.py'

usage: naocontroller.py [-h] [-ip IP] [-port PORT]

Connect to and start interactive session to send talk and animation commands
to Nao.

optional arguments:
  -h, --help  show this help message and exit
  -ip IP      IP (or hostname) of your Nao robot.
  -port PORT  Port of your Nao robot.
  
If you invoke via python IDE or import NaoController class into another python script the intitial IP and Port 
values are retrieved from defaults.py.


HOW TO USE THE CONSOLE

Text to speech command:"Text to say" "Animation tag while text is playing"
Posture command: Posture
Subsystem state toggle: Subsystem

Example:> "Hello, how are you" "bow"

Example:> "That is not correct" "incorrect"

Example:> Sit

Example:> Stand


Quit console by typing "exit" (without quotes)


COMMANDS SUPPORTED

	*Text to Speech*

	Command format: "Text to say" "Animation tag while text is playing" 
	List of animation tags can be found for convenience in the 'animationtags.txt' file.  Note that this file is not used by the script and just
	included with this package for convenience.
	Text and animation should be wrapped in quotes.
	An animation tag is just a single word.

	*Posture*

	Command format: "Posture to assume"
	Supported postures:
	-Sit 
	-Stand

	*Sub-Systems*
	Command format: "Subsystem to toggle"
	Support subsystems:
	-Autolife
