import argparse
import sys
import string
import re

import defaults
from naoqi import ALProxy

class NaoController:

    def connect_to_robot(self):
        proxy = None
        try:
            proxy = ALProxy("ALAnimatedSpeech", self.ip, self.port)
            print "Connected to robot..."
        except RuntimeError as e:
            print "Error connecting to robot({0})".format(e)
        return proxy

    def print_usage(self):
        print 'Command format:"Text to say" "Animation tag while text is playing"'
        print 'Example: "Hello, how are you" "Bow"'
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
        match_pattern = '^"([^"]*)"\s+"([A-Za-z]*)"$'
        match = re.match(match_pattern, command)
        if(match):
            speech = match.group(1)
            animation = match.group(2)
            return(speech, animation)
        return None

    def invoke_command(self, proxy, speech, animation,):
        animatedSpeech = '^startTag({0}) "{1}" ^waitTag({0})'.format(animation, speech)
        proxy.say(animatedSpeech)

    def main(self):
        proxy = self.connect_to_robot()
        if (proxy):
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


    
