"""controller.py: 'Business layer' between inputs and robot.py"""
import math
import re
import time
import naocontroller.core.robot as corerobot
from naocontroller.defaults import defaults

# disable too many public methods and docsctring linting
# pylint: disable=R0904, C0111

class Controller(object):
     
    def connect(self, host, port):
        if self.robot.is_connected:
            print 'Connection to robot already exists.'
            return

        if host is None:
            host = defaults.DEFAULT_IP
        if port is None:
            port = defaults.DEFAULT_PORT
        self.robot.connect(host, port)

    def say(self, animation, speech):
        if not self.robot.is_connected:
            self.print_not_connected_error()
            return
     
        cleaned_animation = self.clean_animated_speech(animation)
        cleaned_speech = self.clean_animated_speech(speech)
        animated_speech = self.format_animated_speech(cleaned_animation, cleaned_speech)
        self.robot.say(animated_speech)

    def move(self, rotation_in_hours, distance):
        if not self.robot.is_connected:
            self.print_not_connected_error()
            return
        try:
            rotation_in_rads = self.convert_hour_to_radians(self.clamp(1, rotation_in_hours, 12))
            distance_clamped = self.clamp(-10, distance, 10)
        except ValueError as error:
            print '\nError:{0}'.format(error)
            return   
        self.robot.move(rotation_in_rads, distance_clamped)

    def stand(self):
        if not self.robot.is_connected:
            self.print_not_connected_error()
            return
       
        print 'Standing...'
        self.robot.set_stiffness('Body', 1.0)
        self.robot.set_pose('Stand')
        self.robot.set_breathing(True)
        
    def sit(self):
        if not self.robot.is_connected:
            self.print_not_connected_error()
            return
       
        print 'Sitting...'
        self.robot.set_breathing(False)
        self.robot.set_pose('Sit')
        self.robot.set_stiffness('Body', 0.0)  

    def hold(self):
        if not self.robot.is_connected:
            self.print_not_connected_error()
            return

        self.robot.set_breathing(False)
        self.robot.set_stiffness('RArm', 1.0)
        self.robot.set_joint_angle('RShoulderPitch', 20)
        hand = 'RHand'
        self.robot.open_hand(hand)
        time.sleep(2.0)
        self.robot.close_hand(hand)
        self.robot.set_move_arms_enabled(True, False)
        

    def drop(self):
        if not self.robot.is_connected:
            self.print_not_connected_error()
            return
       
        self.robot.set_stiffness('RArm', 1.0)
        hand = 'RHand'
        self.robot.open_hand(hand)
        time.sleep(2.0)
        self.robot.close_hand(hand)
        self.robot.set_joint_angle('RShoulderPitch', 80)
        self.robot.set_move_arms_enabled(True, True)

    def toggle_autolife(self):
        if not self.robot.is_connected:
            self.print_not_connected_error()
            return
        
        current_state = self.robot.get_autonomous_life_state()
        if current_state == 'interactive':
            #changing state while in interactive mode throws exception
            print 'Cannot change autolife state when in interactive mode.'
            return
        elif current_state == 'solitary':
            self.robot.set_autonomous_life(False)
        else:
            self.robot.set_autonomous_life(True)

    @staticmethod
    def print_not_connected_error():
        print 'You cannot run this command until you connect to robot with the CONNECT command'

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
    def clean_animated_speech(speech):
        regex = re.compile('[^a-zA-Z., ]')
        cleaned = regex.sub('', speech).replace('.', '\\pau=800\\').replace(',', '\\pau=400\\')
        return cleaned

    @staticmethod
    def format_animated_speech(animation, speech):
        animated_speech = '^startTag({0}) "\\rspd={2}\\{1}" ^waitTag({0})'.format(
            animation.lower(), speech, defaults.SPEECH_SPEED)
        return animated_speech

    def __init__(self):
        self.robot_is_connected = False
        self.robot = corerobot.Robot()
       