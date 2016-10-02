"""NaoController.py: Creates an interactive shell session with a Nao robot
This class inherits cmd and passes commands and processed args to controller.py"""
import sys
import cmd2 as cmd
from naocontroller.core import controller

# disable too many public methods
# pylint: disable=R0904
class NaoCommandLine(cmd.Cmd):
    """NaoController is a subclass of cmd which enables simple line interpretation. 
    https://docs.python.org/2/library/cmd.html"""

    intro = 'Welcome to the Nao controller.   Type help or ? to list commands.'
    prompt = '(nao)'

    def do_connect(self, arg):
        """Connect to nao robot-'connect <ip/host> <port>' or 'connect' alone (uses defaults.py)"""
        split_args = self.parse(arg)
        try:
            if len(split_args) > 1: #very weak param validation
                host = split_args[0]
                port = int(split_args[1]) 
            else:
                host = None
                port = None
        except ValueError as exception:
            print 'Connection argument invalid: {0}'.format(exception)
            return
        self.controller.connect(host, port)

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
        self.controller.move(rotation_in_hours, distance)

    # pragma pylint: disable=unused-argument
    def do_say(self, arg): 
        """Robot will say a line of text and play an animation."""
        self.stdout.write('What would you like the robot to say?\n')
        speech = self.stdin.readline()
        self.stdout.write('What animation would you like the robot to perform?\n')
        animation = self.stdin.readline()
        self.controller.say(animation, speech)

    def do_stand(self, arg):
        """Robot will stand and start breathing."""
        self.controller.stand()

    def do_sit(self, arg):
        """Robot will sit and stop breathing."""
        self.controller.sit()

    def do_autolife(self, arg):
        """Toggles autonomous life state of the robot."""
        self.controller.toggle_autolife()

    def do_hold(self, arg):
        """Open hand for 2 seconds, then closes it.  Use 'drop' command to release ."""
        self.controller.hold()

    def do_drop(self, arg):
        """Opens hand and returns arm to idle position"""
        self.controller.drop()

    def do_EOF(self, line):
        return True
    # pragma pylint: enable=unused-argument

    @staticmethod
    def parse(arg):
        '''Splits args'''
        return arg.split()

    def __init__(self, script):
        '''Pass path to script to run or None for interactive'''
        if script is not None:
            cmd.Cmd.__init__(self, stdin=script)
            self.use_rawinput = False
        else:
            cmd.Cmd.__init__(self)
        self.controller = controller.Controller()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        SCRIPT = open(sys.argv[1], 'rt')
        try:
            NaoCommandLine(SCRIPT).cmdloop()
        finally:
            SCRIPT.close()
    else:
        NaoCommandLine(None).cmdloop()
