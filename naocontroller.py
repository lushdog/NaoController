"""NaoController.py: Creates an interactive shell session with a Nao robot"""
import sys
import re
import math
import defaults
from naoqi import ALProxy
import cmd2 as cmd

# disable too many public methods and docsctring linting
# pylint: disable=R0904, C0111

class NaoController(cmd.Cmd):

    ANIM_SPEECH_LIB = "ALAnimatedSpeech"
    MOTION_LIB = "ALMotion"
    POSTURE_LIB = "ALRobotPosture"
    BASIC_AWARE_LIB = "ALBasicAwareness"
    AUTONOMOUS_MOVES_LIB = "ALAutonomousMoves"
    AUTONOMOUS_LIFE_LIB = "ALAutonomousLife"
    PROXY_LIBS = [ANIM_SPEECH_LIB, MOTION_LIB, POSTURE_LIB,
                  BASIC_AWARE_LIB, AUTONOMOUS_MOVES_LIB, AUTONOMOUS_LIFE_LIB]

    is_connected = False
    intro = 'Welcome to the Nao controller.   Type help or ? to list commands.'
    prompt = '(nao)'

    def do_connect(self, arg):
        """Connect to nao robot-'connect <ip/host> <port>' or 'connect' alone (uses defaults.py)"""
        if self.is_connected:
            self.stdout.write('There is already a connection to a robot.\n')
            return
        self.invoke_connect(arg)

    def do_move(self, arg):
        """Rotate, then moves robot-'move <rotation in hours> <meters to move forward/backward>'"""
        if not self.is_connected:
            self.print_not_connected_error()
            return
        self.invoke_move(arg)
    
    # pragma pylint: disable=unused-argument
    def do_say(self, arg): 
        """Robot will say a line of text and play an animation."""
        if not self.is_connected:
            self.print_not_connected_error()
            return
        self.invoke_say(*self.get_say_inputs())

    def do_stand(self, arg):
        """Robot will stand and start breathing."""
        if not self.is_connected:
            self.print_not_connected_error()
            return
        self.invoke_stand()

    def do_sit(self, arg):
        """Robot will sit and stop breathing."""
        if not self.is_connected:
            self.print_not_connected_error()
            return
        self.invoke_sit()

    def do_autolife(self, arg):
        """Toggles autonomous life state of the robot."""
        if not self.is_connected:
            self.print_not_connected_error()
            return
        self.invoke_toggle_autolife()

    def do_EOF(self, line):
        return True
    # pragma pylint: enable=unused-argument

    def invoke_connect(self, arg):
        """Takes connection params and builds list of ALProxies"""
        split_args = self.parse(arg)
        try:
            if len(split_args) > 1: #very weak param validation
                host = split_args[0]
                port = int(split_args[1]) 
            else:
                host = defaults.DEFAULT_IP
                port = defaults.DEFAULT_PORT
        except ValueError as exception:
            self.stdout.write('Connection argument invalid: {0}\n'.format(exception))
            self.is_connected = False
            return
                    
        self.stdout.write('Connecting to robot on {0}:{1}...\n'.format(host, port))
        for lib in self.PROXY_LIBS:
            try:
                self.robot_proxies[lib] = ALProxy(lib, host, port)
            except Exception as exception: # pylint: disable=broad-except
                self.stdout.write('\nCould not create proxy to {0}\n'.format(lib))
                self.stdout.write('Error was: {0}\n'.format(exception))
                self.is_connected = False
                return
        self.is_connected = True
        #self.set_autonomous_life(False)

    def invoke_say(self, animation, speech):
        cleaned_animation = self.clean_speech(animation)
        cleaned_speech = self.clean_speech(speech)
        animated_speech = self.format_say_inputs(cleaned_animation, cleaned_speech)
        self.robot_proxies[self.ANIM_SPEECH_LIB].say(animated_speech)

    def get_say_inputs(self):
        self.stdout.write('What would you like the robot to say?\n')
        speech = self.stdin.readline()
        self.stdout.write('What animation would you like the robot to perform?\n')
        animation = self.stdin.readline()
        return animation, speech

    def invoke_stand(self):
        self.stdout.write('Standing...\n')
        self.set_body_stiffness(1.0)
        self.set_pose('Stand')
        self.set_breathing(True)
        
    def invoke_sit(self):
        self.stdout.write('Sitting...\n')
        self.set_breathing(False)
        self.set_pose('Sit')
        self.set_body_stiffness(0.0)  

    def set_body_stiffness(self, stiffness):
        self.stdout.write('Setting stiffness to {0}...\n'.format(stiffness))
        self.robot_proxies[self.MOTION_LIB].stiffnessInterpolation("Body", stiffness, 1.0) 

    def set_pose(self, pose):
        self.robot_proxies[self.POSTURE_LIB].goToPosture(pose, 0.5)

    def invoke_move(self, arg):
        processed_arg = self.process_move_arg(arg)
        if processed_arg is None:
            self.stdout.write("Invalid arguments passed to move command.\n")
            return
        rotation = processed_arg[0]
        distance = processed_arg[1]
        
        motion = self.robot_proxies[self.MOTION_LIB]
        motion.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])
        motion.setMotionConfig([["ENABLE_STIFFNESS_PROTECTION", True]])
        motion.setMoveArmsEnabled(True, True)
        motion.setCollisionProtectionEnabled('Arms', True)
        motion.setExternalCollisionProtectionEnabled('All', True)
        motion.moveTo(0, 0, rotation)
        motion.moveTo(distance, 0, 0)
        
    def process_move_arg(self, arg):
        """Parse move arg,validate,clamp and convert to values usable by ALProxy Move()
        
        arguments:
        arg[0] - relative rotation in hours (clock)
        arg[1] - distance in meters to move

        returns:
        {relative rotation in radians, distance in meters to move}
        None if args are invalid"""

        parsed_args = self.parse(arg)
        if len(parsed_args) < 2:
            self.stdout.write("Two arguments must be passed to the move command\n")
            return None
        try:
            theta = self.convert_hour_to_radians(self.clamp(1, int(parsed_args[0]), 12))
            distance = self.clamp(-10, float(parsed_args[1]), 10)
        except ValueError as error:
            self.stdout.write("\nError:{0}\n".format(error))
            return None   
        return theta, distance

    def invoke_toggle_autolife(self):
        current_state = self.robot_proxies[self.AUTONOMOUS_LIFE_LIB].getState()
        if current_state == 'interactive':
            #changing state while in interactive mode throws exception
            self.stdout.write('Cannot change autolife state when in interactive mode.\n')
            return
        elif current_state == 'solitary':
            self.set_autonomous_life(False)
        else:
            self.set_autonomous_life(True)

    def set_autonomous_life(self, set_on):
        self.print_sub_system_update(set_on, 'Autonomous Life')
        target_state = 'solitary' if set_on else 'disabled'
        self.robot_proxies[self.AUTONOMOUS_LIFE_LIB].setState(target_state)
        
    def get_autonomous_life(self):
        return self.robot_proxies[self.AUTONOMOUS_LIFE_LIB].getState() != 'disabled'
  
    def set_autonomous_moves(self, set_on):
        self.print_sub_system_update(set_on, 'Autonomous Moves')
        target_state = 'backToNeutral' if set_on else 'none'
        self.robot_proxies[self.AUTONOMOUS_MOVES_LIB].setBackgroundStrategy(target_state)
        
    def set_awareness(self, set_on):
        self.print_sub_system_update(set_on, 'Basic Awareness')
        proxy = self.robot_proxies[self.BASIC_AWARE_LIB]
        if set_on:
            proxy.startAwareness() 
        else:
            proxy.stopAwareness()

    def set_breathing(self, set_on):
        self.print_sub_system_update(set_on, 'body breathing')
        self.robot_proxies[self.MOTION_LIB].setBreathEnabled('Body', set_on)
        self.print_sub_system_update(set_on, 'arm breathing')
        self.robot_proxies[self.MOTION_LIB].setBreathEnabled('Arms', set_on)

    def print_not_connected_error(self):
        self.stdout.write(
            'You cannot run this command until you connect to robot with the CONNECT command\n')

    def print_sub_system_update(self, set_on, sub_process):
        on_off = ['off', 'on']
        self.stdout.write('Turning {0} {1}...\n'.format(on_off[set_on], sub_process))

    @staticmethod
    def parse(arg):
        return arg.split()

    @staticmethod
    def convert_hour_to_radians(hour):
        if hour >= 1 and hour <= 6:
            hours_from_12 = -1 * hour
        else:
            hours_from_12 = 12 - hour
        return (hours_from_12 * math.pi) / 6

    @staticmethod
    def clamp(minvalue, value, maxvalue):
        return max(minvalue, min(value, maxvalue))

    @staticmethod
    def clean_speech(speech):
        regex = re.compile('[^a-zA-Z., ]')
        cleaned = regex.sub('', speech).replace('.', '\\pau=800\\').replace(',', '\\pau=400\\')
        return cleaned

    @staticmethod
    def format_say_inputs(animation, speech):
        animated_speech = '^startTag({0}) "\\rspd={2}\\{1}" ^waitTag({0})'.format(
            animation.lower(), speech, defaults.SPEECH_SPEED)
        return animated_speech

    #def main(self):

    def __init__(self, script):
        '''Pass path to script to run or None for interactive'''
        self.robot_proxies = {}
        if script is not None:
            cmd.Cmd.__init__(self, stdin=script)
            self.use_rawinput = False
        else:
            cmd.Cmd.__init__(self)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        SCRIPT = open(sys.argv[1], 'rt')
        try:
            NaoController(SCRIPT).cmdloop()
        finally:
            SCRIPT.close()
    else:
        NaoController(None).cmdloop()


    
