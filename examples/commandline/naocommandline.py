"""naocommandline.py: Interactive shell session with a Nao robot"""
import sys
import cmd
import core_controller
import core_robot
import video_controller
import video_robot
import defaults

#pylint: disable=unused-argument,line-too-long,invalid-name,no-self-use

class NaoCommandLine(cmd.Cmd):
    """NaoCommandLine is a subclass of cmd which enables simple line interpretation. 
    https://docs.python.org/2/library/cmd.html"""

    intro = 'Welcome to the Nao controller.   Type help or ? to list commands.'
    prompt = '(nao)'
    case_insensitive = False 

    def __init__(self, script):
        '''Pass path to script to run or None for interactive'''
        if script is not None:
            cmd.Cmd.__init__(self, stdin=script)
            self.use_rawinput = False
        else:
            cmd.Cmd.__init__(self)

        self.core_controller = None
        self.video_controller = None
        self.is_connected = False

    def do_connect(self, arg):
        """Connect to nao robot-'connect <ip/host> <port>' or 'connect' alone (uses api\\defaults.py)"""
        host = defaults.DEFAULT_IP
        port = defaults.DEFAULT_PORT
        
        try:
            split_args = self.parse(arg)
            if len(split_args) > 1: 
                host = split_args[0]
                port = int(split_args[1]) 
        except ValueError as exception:
            print 'Connection argument invalid: {0}'.format(exception)
            return

        try:
            corebot = core_robot.CoreRobot()
            vidbot = video_robot.VideoRobot()
            corebot.connect(host, port)
            vidbot.connect(host, port)
        except ValueError as error:
            print error
            return

        self.core_controller = core_controller.CoreController(corebot)
        self.video_controller = video_controller.VideoController(vidbot)
        self.is_connected = True

    def precmd(self, line):
        if not self.is_connected:
            if not line.startswith('connect') and not line.startswith('EOF') and not line.startswith('help') and not line.startswith('?'):
                line = 'not_connected'
        return line

    def do_not_connected(self, arg):
        """This command is run if you attempt to run a command that needs a connection without connecting first.
        Do not use this command directly."""
        print 'To use this command you must first "connect".'

    def do_move(self, arg):
        """Rotate, then moves robot-'move <rotation in hours> <meters to move forward/backward>'"""
        split_args = self.parse(arg)
        if len(split_args) > 1:
            try:
                rotation_in_hours = int(split_args[0])
                distance = float(split_args[1])
            except ValueError as error:
                print '\nError:{0}'.format(error)
        else:
            print 'Two arguments must be passed to the move command'
            return
        self.core_controller.move(rotation_in_hours, distance)

    def do_say(self, arg): 
        """Robot will say a line of text and play an animation."""
        self.stdout.write('What would you like the robot to say?\n')
        speech = self.stdin.readline()
        self.stdout.write('What animation would you like the robot to perform?\n')
        animation = self.stdin.readline()
        self.core_controller.say(animation, speech)

    def do_stand(self, arg):
        """Robot will stand and start breathing."""
        self.core_controller.stand()

    def do_sit(self, arg):
        """Robot will sit and stop breathing."""
        self.core_controller.sit()

    def do_autolife(self, arg):
        """Toggles autonomous life state of the robot."""
        self.core_controller.toggle_autolife()

    def do_hold(self, arg):
        """Open hand for 2 seconds, then closes it.  Use 'drop' command to release ."""
        self.core_controller.hold()

    def do_drop(self, arg):
        """Opens hand and returns arm to idle position"""
        self.core_controller.drop()

    def do_picture(self, arg):
        """Takes a picture with upper camera and shows it on the screen"""
        self.video_controller.get_picture()

    def do_picture_bottom(self, arg):
        """Takes a picture with bottom camera and shows it on the screen"""
        self.video_controller.get_picture(True)


    def do_EOF(self, line): 
        """This command is called when a script ends.  
        Do not use this command directly."""
        return True
    
    @staticmethod
    def parse(arg):
        """Splits line"""
        return arg.split()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        SCRIPT = open(sys.argv[1], 'rt')
        try:
            NaoCommandLine(SCRIPT).cmdloop()
        finally:
            SCRIPT.close()
    else:
        NaoCommandLine(None).cmdloop()
