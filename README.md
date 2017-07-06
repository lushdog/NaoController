#naocontroller
API written in Python to abstract commands from NaoQI code

##usage
Extract .zip to c:\yourfoldername\naocontroller

Put `c:\yourfoldername` on your PYTHONPATH

Install naoqi python package

Install PIL python package

Create instance of a robot and connect to it

Pass robot instance to matching controller

    import core_robot, core_controller  
	robot = core_robot.CoreRobot()
	robot.connect(host, port)
	controller = core_controller.CoreController(robot) 
    controller.move(rotation, distance)  
	controller.say()
	