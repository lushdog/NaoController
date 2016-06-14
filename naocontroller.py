import argparse
import sys
import string
import re

import defaults
from naoqi import ALProxy

class NaoController:

    def connect_to_robot(self):
        self.tts_proxy = None
        self.motion_proxy = None
        self.posture_proxy = None

        print "Connecting to robot..."
        try:
            self.tts_proxy = ALProxy("ALAnimatedSpeech", self.ip, self.port)
        except Exception, e:
            print "Could not create proxy to ALAnimatedSpeech"
            print "Error was: ", e

        if (self.tts_proxy):
            try:
                self.motion_proxy = ALProxy("ALMotion", self.ip, self.port)
            except Exception, e:
                print "Could not create proxy to ALMotion"
                print "Error was: ", e

        if (self.motion_proxy):
            try:
                self.posture_proxy = ALProxy("ALRobotPosture", self.ip, self.port)
            except Exception, e:
                print "Could not create proxy to ALRobotPosture"
                print "Error was: ", e

    def print_usage(self):
        print 'Command format:"Text to say" "Animation tag while text is playing" or PostureToAssume'
        print 'Example: "Hello, how are you" "Bow"'
        print 'Example: Sit'
        print 'Quit by typing "exit" (without quotes)'

    def command_loop(self, proxy):
        command = self.get_command()
        while (string.lower(command) != 'exit'):
            parsed_command = self.parse_command(command)
            if (parsed_command):
                print parsed_command
                self.invoke_command(proxy, *parsed_command)            
            else:
                print 'Command format was invalid'
                self.print_usage()
            command = self.get_command()

    def get_command(self):
        return raw_input("Command:")

    @staticmethod
    def parse_command(command):
        match_pattern = '^"([^"]*)"\s+"([A-Za-z]*)"$|^(?i)(Stand|Sit)$'
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
        animatedSpeech = '^startTag({0}) "{1}" ^waitTag({0})'.format(animation, speech)
        self.tts_proxy.say(animatedSpeech)

    def invoke_posture(self, posture):
        posture = string.lower(posture)
        if (posture == 'sit'):
            self.invoke_sit()
        elif (posture == 'stand'):
            self.invoke_stand()

    def invoke_stand(self):
        self.set_body_stiffness(1.0)
        self.set_pose('StandInit')

    def invoke_sit(self):
        self.set_pose('Sit')
        self.set_body_stiffness(0.0)

    def set_body_stiffness(stiffness):
        self.motion_proxy.stiffnessInterpolation("Body", stiffness, stiffness) 

    def set_pose(pose):
        self.posture_proxy.goToPosture(pose, 0.5)
    
    def main(self):
        self.connect_to_robot()
        if (self.tts_proxy and self.motion_proxy and self.posture_proxy):
            self.print_usage()
            self.command_loop(proxy)

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


    
