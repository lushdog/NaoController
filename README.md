#NaoController
Command line interface that can perform basic actions on the Nao robot.

Usage: python naocontroller.py [path to script file]

###How to use the console  
Type 'help' to see list of supported commands  
Type 'help command' to see help for certain command  

###Sample command usage
'quit' - exits the session  
'connect' - connects to nao using ip and port in the defaults.py file  
'connect 192.168.1.1 9559' - connects to nao using ip and port specified  
**Connection must be made before any commands below can be issued**  
'stand' - robot stands and commences body and arm breathing  
'sit' - robot sits and stops body and arm breathing  
'autolife' - toggles autonomous life setting on/off  
**Turn off autolife before issuing sit or stand (or other future pose) commands or else autolife will force the robot to return to its previous pose**  
'move 12 1' - moves the robot forward 1 meter  
'move 3 1' - rotates the robot to face its right and then moves the robot forward one meter  
'move 9 -2' - rotates the robot to face its left and then moves the robot backwards two meters  
'say' - user is prompted for text to say and an animation to run while text-to-speech is running  






