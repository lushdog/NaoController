import argparse, sys, string, re, os, math
import defaults
from naoqi import ALProxy
import cmd2 as cmd

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

    '''COMMAND PROCESSORS'''
    def do_connect(self, arg):
        '''Connect to nao robot via 'connect <ip/host of robot> <port>' or 'connect' alone (uses defaults.py)'''
        if (self.is_connected):
            self.stdout.write('There is already a connection to a robot.\n')
            return
        self.invoke_connect(arg)
                 
    def do_say(self, args):
        '''Robot will say a line of text and play an animation.'''
        if (not self.is_connected):
            self.print_not_connected_error()
            return
        self.invoke_say(*self.get_say_inputs())

    def do_stand(self, arg):
        '''Robot will stand and start breathing.'''
        if (not self.is_connected):
            self.print_not_connected_error()
            return
        self.invoke_stand()

    def do_sit(self, arg):
        '''Robot will sit and stop breathing.'''
        if (not self.is_connected):
            self.print_not_connected_error()
            return
        self.invoke_sit()

    def do_autolife(self, arg):
        '''Toggles autonomous life state of the robot.'''
        if (not self.is_connected):
            self.print_not_connected_error()
            return
        self.invoke_toggle_autolife()

    def do_move(self, arg):
        '''Moves the robot'''
        if (not self.is_connected):
            self.print_not_connected_error()
            return
        self.invoke_move_toward(arg)
        
    def do_EOF(self, line):
        return True


    '''COMMAND INVOCATION'''
    def invoke_connect(self, arg):
        if (len(arg) > 1): #very weak param validation
            ip = arg[0]
            port = arg[1]
        else:
            ip = defaults.DEFAULT_IP
            port = defaults.DEFAULT_PORT
                    
        self.stdout.write('Connecting to robot on {0}:{1}...\n'.format(ip, port))
        self.robot_proxies = {}
        for lib in self.PROXY_LIBS:
            try:
                self.robot_proxies[lib] = ALProxy(lib, ip, port)
            except Exception, e:
                self.stdout.write('\nCould not create proxy to {0}\n'.format(lib))
                self.stdout.write('\nError was: {0}\n'.format(e))
                self.is_connected = False
                return
        self.is_connected = True
        self.set_autonomous_life(False)

    def invoke_say(self, animation, speech):
        cleaned_animation = self.clean_animation(animation)
        cleaned_speech = self.clean_speech(speech)
        animatedSpeech = self.format_say_inputs(cleaned_animation, cleaned_speech)
        self.robot_proxies[self.ANIM_SPEECH_LIB].say(animatedSpeech)

    #MM:do we need to strip any unsupported characters from animation and speech?
    def clean_speech(self, speech):
        return speech

    def clean_animation(self, animation):
        return animation

    def format_say_inputs(self, animation, speech):
        animatedSpeech = '^startTag({0}) "\\rspd={2}\\{1}" ^waitTag({0})'.format(animation.lower(), speech, defaults.SPEECH_SPEED)
        return animatedSpeech

    def get_say_inputs(self):
        self.stdout.write('What would you like the robot to say?\n')
        speech = self.stdin.readline()
        self.stdout.write('What animation would you like the robot to perform?\n')
        animation = self.stdin.readline()
        return animation, speech

    def invoke_stand(self):
        self.stdout.write('Standing...')
        self.set_body_stiffness(1.0)
        self.set_pose('Stand')
        self.set_breathing(True)
        
    def invoke_sit(self):
        self.stdout.write('Sitting...')
        self.set_breathing(False)
        self.set_pose('Sit')
        self.set_body_stiffness(0.0)  

    def set_body_stiffness(self, stiffness):
        self.stdout.write('Setting stiffness to {0}...'.format(stiffness))
        self.robot_proxies[self.MOTION_LIB].stiffnessInterpolation("Body", stiffness, 1.0) 

    def set_pose(self, pose):
        self.robot_proxies[self.POSTURE_LIB].goToPosture(pose, 0.5)

    def invoke_move_to(self, arg):
        processed_args = list(*self_process_move_arg(arg))
        if (processed_args[0] == False):
            self.stdout.write("Invalid arguments passed to move_to command.")
            return
        motion = self.robot_proxies[self.MOTION_LIB]
        motion.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", False]])
        motion.setMoveArmsEnabled(True, True)
        motion.moveTo(processed_args[1], processed_y[2], processed_theta[3])
        #MM: enable collision detection

    def process_move_arg(self, arg):
        ##MM: if not 3 args 
        ##MM: if non-number args
        ##MM: if degress less than 0 and bigger than 360 clamp
        ##MM: unit test process and validation
        x = arg[0]
        y = arg[1]
        theta = math.radians(arg[2])
        return True, x, y, theta

    def invoke_toggle_autolife(self):
        current_state = (self.robot_proxies[self.AUTONOMOUS_LIFE_LIB].getState() == 'solitary')
        if (current_state == 'interactive'):
            self.stdout.write('Cannot change autolife state when in interactive mode.')
        else:
            self.set_autonomous_life(not current_state)

    def set_autonomous_life(self, set_on):
        self.print_sub_system_update(set_on, 'Autonomous Life')
        target_state = 'solitary' if set_on else 'disabled' #todo: this causes exception if the robot is in interactive state
        self.robot_proxies[self.AUTONOMOUS_LIFE_LIB].setState(target_state)
        
    def get_autonomous_life(self):
        return (self.robot_proxies[self.AUTONOMOUS_LIFE_LIB].getState() != 'disabled')
  
    def set_autonomous_moves(self, set_on):
        self.print_sub_system_update(set_on, 'Autonomous Moves')
        target_state = 'backToNeutral' if set_on else 'none'
        self.robot_proxies[self.AUTONOMOUS_MOVES_LIB].setBackgroundStrategy(target_state)
        
    def set_awareness(self, set_on):
        self.print_sub_system_update(set_on, 'Basic Awareness')
        proxy = self.robot_proxies[self.BASIC_AWARE_LIB]
        proxy.startAwareness() if set_on else proxy.stopAwareness()

    def set_breathing(self, set_on):
        NaoController.print_sub_system_update(set_on, 'body breathing')
        self.robot_proxies[self.MOTION_LIB].setBreathEnabled('Body', set_on)
        NaoController.print_sub_system_update(set_on, 'arm breathing')
        self.robot_proxies[self.MOTION_LIB].setBreathEnabled('Arms', set_on)

    def print_not_connected_error(self):
        self.stdout.write('You cannot run this command until you connect to robot with the CONNECT command\n')

    def print_sub_system_update(self, set_on, sub_process):
        on_off = ['off', 'on']
        self.stdout.write('Turning {0} {1}...'.format(on_off[set_on], sub_process))
  
    #def main(self):

    def __init__(self, script):
        if (script is not None):
            cmd.Cmd.__init__(self, stdin=script)
            self.use_rawinput = False
        else:
            cmd.Cmd.__init__(self)

if __name__ == "__main__":
    if (len(sys.argv) > 1):
        script = open(sys.argv[1], 'rt')
        try:
            NaoController(script).cmdloop()
        finally:
            script.close()
    else:
        NaoController(None).cmdloop()


    
