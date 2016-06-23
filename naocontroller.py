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
    AUTONOMOUS_LIB = "ALAutonomousMoves"

    def connect_to_robot(self):
        print "Connecting to robot..."
        proxy_libs = [self.ANIM_SPEECH_LIB, self.MOTION_LIB, self.POSTURE_LIB, self.BASIC_AWARE_LIB, self.AUTONOMOUS_LIB]
        self.robot_proxies = {}
        for lib in proxy_libs:
            try:
                self.robot_proxies[lib] = ALProxy(lib, self.ip, self.port)
            except Exception, e:
                print "Could not create proxy to ", lib
                print "Error was: ", e
                return False
        return True

    def print_usage(self):
        print 'Text to speech command:"Text to say" "Animation tag while text is playing"'
        print 'Posture command: Posture'
        print 'Example: "Hello, how are you" "Bow"'
        print 'Example" "That is not correct" "Incorrect"'
        print 'Example: Sit'
        print 'Example: Stand'
        print 'Quit by typing "exit" (without quotes)'

    def command_loop(self):
        command = self.get_command()
        while (string.lower(command) != 'exit'):
            parsed_command = self.parse_command(command)
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
        match_pattern = '^"([^"\\\\]*)"\s+"([A-Za-z]*)"$|^(?i)(Stand|Sit)$'
        match = re.match(match_pattern, command)
        if(match):
            speech = match.group(1)
            animation = match.group(2)
            posture = match.group(3)
            return(speech, animation, posture)
        return None

    def invoke_command(self, speech, animation, posture):
        "Sending command to Nao..."
        if (speech):
            self.invoke_speech(speech, animation)      
        else:
            self.invoke_posture(posture)
            
    def invoke_speech(self, speech, animation):
        animatedSpeech = '^startTag({0}) "\\rspd={2}\\{1}" ^waitTag({0})'.format(animation.lower(), speech, defaults.SPEECH_SPEED)
        self.robot_proxies[self.ANIM_SPEECH_LIB].anim_speech_proxy.say(animatedSpeech)

    def invoke_posture(self, posture):
        posture = posture.lower()
        if (posture == 'sit'):
            self.invoke_sit()
        elif (posture == 'stand'):
            self.invoke_stand()

    def invoke_stand(self):
        print 'Standing...'
        self.set_body_stiffness(1.0)
        self.set_pose('StandInit')

    def invoke_sit(self):
        print 'Sitting...'
        self.set_pose('Sit')
        self.set_body_stiffness(0.0)

    def set_body_stiffness(self, stiffness):
        self.robot_proxies[self.MOTION_LIB].stiffnessInterpolation("Body", stiffness, 1.0) 

    def set_pose(self, pose):
        self.robot_proxies[self.POSTURE_LIB].goToPosture(pose, 0.5)
    
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


    
