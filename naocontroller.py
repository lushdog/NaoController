import argparse
import sys
import string
import re

import defaults
from naoqi import ALProxy

class NaoController:

    ANIM_SPEECH_LIB = "ALAnimatedSpeech"
    MOTION_LIB = "ALMotion"
    POSTURE_LIB = "ALRobotPosture"
    BASIC_AWARE_LIB = "ALBasicAwareness"
    AUTONOMOUS_MOVES_LIB = "ALAutonomousMoves"
    AUTONOMOUS_LIFE_LIB = "ALAutonomousLife"
    PROXY_LIBS = [ANIM_SPEECH_LIB, MOTION_LIB, POSTURE_LIB,
                BASIC_AWARE_LIB, AUTONOMOUS_MOVES_LIB, AUTONOMOUS_LIFE_LIB]

    def connect_to_robot(self):
        print "Connecting to robot..."
        self.robot_proxies = {}
        for lib in self.PROXY_LIBS:
            try:
                self.robot_proxies[lib] = ALProxy(lib, self.ip, self.port)
            except Exception, e:
                print "Could not create proxy to ", lib
                print "Error was: ", e
                return False
        self.set_autonomous_life(False)
        return True

    def print_usage(self):
        print 'Text to speech command:"Text to say" "Animation tag while text is playing"'
        print 'Posture command: Posture'
        print 'Subsytem command: SubsystemToToggle'
        print 'Example: "Hello, how are you" "Bow"'
        print 'Example" "That is not correct" "Incorrect"'
        print 'Example: Sit'
        print 'Example: Autolife'
        print 'Quit by typing "exit" (without quotes)'

    def command_loop(self):
        command = self.get_command()
        while (string.lower(command) != 'exit'):
            parsed_command = NaoController.parse_command(command)
            if (parsed_command):
                #print parsed_command
                self.invoke_command(*parsed_command)            
            else:
                print 'Command format was invalid'
                self.print_usage()
            command = self.get_command()

    def get_command(self):
        return raw_input("Command:")

    @staticmethod
    def parse_command(command):
        match_pattern = '^\s*"([^"\\\\]*)"\s+"([A-Za-z]*)"\s*$|^\s*(?i)(Stand|Sit|Autolife)\s*$'
        match = re.match(match_pattern, command)
        if(match):
            speech = match.group(1)
            animation = match.group(2)
            method = match.group(3)
            return(speech, animation, method)
        return None

    @staticmethod
    def print_sub_system_update(set_on, sub_process):
         print "Turning {on_off} {sub_process}...".format(on_off = 'on' if set_on == True else 'off', sub_process = sub_process)
  
    def invoke_command(self, speech, animation, method):
        "Sending command to Nao..."
        if (speech):
            self.invoke_speech(speech, animation)      
        else:
            self.invoke_method(method)
            
    def invoke_speech(self, speech, animation):
        animatedSpeech = '^startTag({0}) "\\rspd={2}\\{1}" ^waitTag({0})'.format(animation.lower(), speech, defaults.SPEECH_SPEED)
        self.robot_proxies[self.ANIM_SPEECH_LIB].say(animatedSpeech)

    def invoke_method(self, method):
        if (method.lower() == 'sit'):
            self.invoke_sit()
        elif(method.lower() == 'stand'):
            self.invoke_stand()
        elif(method.lower() == 'autolife'):
            self.toggle_auto_life()

    def invoke_stand(self):
        print 'Standing...'
        self.set_body_stiffness(1.0)
        self.set_pose('Stand')
        self.set_breathing(True)
        is_alive = self.get_autonomous_life()
        
    def invoke_sit(self):
        print 'Sitting...'
        self.set_breathing(False)
        self.set_pose('Sit')
        self.set_body_stiffness(0.0)
        
    def set_body_stiffness(self, stiffness):
        print 'Setting stiffness to {stiffness}...'.format(stiffness = stiffness)
        self.robot_proxies[self.MOTION_LIB].stiffnessInterpolation("Body", stiffness, 1.0) 

    def set_pose(self, pose):
        self.robot_proxies[self.POSTURE_LIB].goToPosture(pose, 0.5)
        
    def toggle_auto_life(self):
        current_state = (self.robot_proxies[self.AUTONOMOUS_LIFE_LIB].getState() == 'solitary')
        self.set_autonomous_life(not current_state)
        
    def set_autonomous_life(self, set_on):
        NaoController.print_sub_system_update(set_on, 'Autonomous Life')
        target_state = 'solitary' if set_on else 'disabled' #todo: this causes exception if the robot is in interactive state
        self.robot_proxies[self.AUTONOMOUS_LIFE_LIB].setState(target_state)
        
    def get_autonomous_life(self):
        return (self.robot_proxies[self.AUTONOMOUS_LIFE_LIB].getState() != 'disabled')
            
    def set_autonomous_moves(self, set_on):
        NaoController.print_sub_system_update(set_on, 'Autonomous Moves')
        target_state = 'backToNeutral' if set_on else 'none'
        self.robot_proxies[self.AUTONOMOUS_MOVES_LIB].setBackgroundStrategy(target_state)
        
    def set_awareness(self, set_on):
        NaoController.print_sub_system_update(set_on, 'Basic Awareness')
        proxy = self.robot_proxies[self.BASIC_AWARE_LIB]
        proxy.startAwareness() if set_on else proxy.stopAwareness()

    def set_breathing(self, set_on):
        NaoController.print_sub_system_update(set_on, 'body breathing')
        self.robot_proxies[self.MOTION_LIB].setBreathEnabled('Body', set_on)
        NaoController.print_sub_system_update(set_on, 'arm breathing')
        self.robot_proxies[self.MOTION_LIB].setBreathEnabled('Arms', set_on)
  
    def main(self):
        if (self.connect_to_robot()):
            self.print_usage()
            self.command_loop()

    def __init__(self):
        self.ip = None
        self.port = None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Connect to and start interactive session to send talk and animation commands to Nao')
    parser.add_argument('-ip', default=defaults.DEFAULT_IP, dest='ip', help='IP (or hostname) of your Nao robot.')
    parser.add_argument('-port', default=defaults.DEFAULT_PORT, dest='port', help='Port of your Nao robot.')
    args = parser.parse_args()
    nc = NaoController()
    nc.ip = args.ip
    nc.port = args.port
    nc.main()


    
