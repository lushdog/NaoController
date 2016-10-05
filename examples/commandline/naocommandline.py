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
    prompt = '(nao)->'
    non_connected_commands = ('connect', 'EOF', 'exit', '?', 'help')
    
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
        except Exception as error: # pylint: disable=broad-except
            print error
            return

        self.core_controller = core_controller.CoreController(corebot)
        self.video_controller = video_controller.VideoController(vidbot)
        self.is_connected = True

    def precmd(self, line):
        if not self.is_connected:
            needs_connection = True
            for index in range(len(self.non_connected_commands)):
                non_connection_command = self.non_connected_commands[index]
                if  line.startswith(non_connection_command):
                    needs_connection = False
                    break
            if needs_connection:
                line = 'not_connected'
        return line

    def do_not_connected(self, arg):
        """This command is run if you attempt to run a command that needs a connection without connecting first.
        Do not use this command directly."""
        print 'To use this command you must first "connect".'

    def do_move(self, arg):
        """Rotate, then moves robot-'move <rotation in hours> <meters to move forward/backward>'"""
        split_args = self.parse(arg)
        if len(split_args) < 1:
            print 'Two arguments must be passed to the move command'
            return
        else:
            try:
                rotation_in_hours = int(split_args[0])
                distance = float(split_args[1])
                self.core_controller.move(rotation_in_hours, distance)
            except ValueError as error:
                print 'Invalid value passed to command.  Try numbers:{0}'.format(error)

    def do_rotate_head(self, arg):
        """Rotates head left and right-'rotate_head <rotation in hours>'"""
        split_args = self.parse(arg)
        if len(split_args) < 1:
            print 'One number must be passed to rotate_head command'
            return
        else:
            try:
                rotation_in_hours = split_args[0]
                self.core_controller.rotate_head(rotation_in_hours)
            except ValueError as error:
                print 'Invalid value passed to command.  Try a number:{0}'.format(error)


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
        try:
            self.core_controller.toggle_autolife()
        except ValueError as error:
            print 'Cannot change autolife state: {0}'.format(error)

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

    def do_set_autoexposure(self, arg):
        """Sets autoexposure from 0-3 - 'set_autoexposure 2'
        0: Average scene Brightness
        1: Weighted average scene Brightness (default)
        2: Adaptive weighted auto exposure for hightlights
        3: Adaptive weighted auto exposure for lowlights"""
        split_args = self.parse(arg)
        if len(split_args) < 1:
            print 'One number must be passed to rotate_head command'
            return
        else:
            self.video_controller.set_auto_exposure(split_args[0])

    def do_exit(self, arg):
        """Quits the interactive session"""
        return True

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
