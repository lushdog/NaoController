"""core_controller.py: 'Business layer' between client and robot"""
import math
import re
import time
import defaults

#pylint: disable=line-too-long,missing-docstring

class CoreController(object):

    def __init__(self, core_robot):
        self.robot = core_robot
     
    def say(self, animation, speech):
        cleaned_animation = self.clean_animated_speech(animation)
        cleaned_speech = self.clean_animated_speech(speech)
        animated_speech = self.format_animated_speech(cleaned_animation, cleaned_speech)
        self.robot.say(animated_speech)

    def move(self, rotation_in_hours, distance):
        try:
            rotation_in_rads = self.convert_hour_to_radians(self.clamp(1, int(rotation_in_hours), 12))
            distance_clamped = self.clamp(-10, int(distance), 10)
            self.robot.move(rotation_in_rads, distance_clamped)
        except TypeError as error:
            raise  TypeError('\nRotation and distance should both be numbers: {0}'.format(error))
               

    def rotate_head(self, rotation_in_hours):
        try: 
            rotation_in_rads = self.convert_hour_to_radians(self.clamp(1, int(rotation_in_hours), 12))
            roatation_in_degrees = math.degrees(rotation_in_rads)
            self.robot.set_stiffness('HeadYaw', 1)
            self.robot.set_joint_angle('HeadYaw', roatation_in_degrees)
            self.robot.set_stiffness('HeadYaw', 0)
        except TypeError as error:
            raise TypeError('\nRotation and distance should both be numbers: {0}'.format(error))

    def stand(self):
        print 'Standing...'
        self.robot.set_stiffness('Body', 1.0)
        self.robot.set_pose('Stand')
        self.robot.set_breathing(True)
        
    def sit(self):
        print 'Sitting...'
        self.robot.set_breathing(False)
        self.robot.set_pose('Sit')
        self.robot.set_stiffness('Body', 0.0)  

    def hold(self):
        self.robot.set_breathing(False)
        self.robot.set_stiffness('RArm', 1.0)
        self.robot.set_joint_angle('RShoulderPitch', 20)
        hand = 'RHand'
        self.robot.open_hand(hand)
        time.sleep(2.0)
        self.robot.close_hand(hand)
        self.robot.set_move_arms_enabled(True, False)
    
    def drop(self):   
        self.robot.set_stiffness('RArm', 1.0)
        hand = 'RHand'
        self.robot.open_hand(hand)
        time.sleep(2.0)
        self.robot.close_hand(hand)
        self.robot.set_joint_angle('RShoulderPitch', 80)
        self.robot.set_move_arms_enabled(True, True)

    def toggle_autolife(self):
        current_state = self.robot.get_autonomous_life_state()
        if current_state == 'interactive':
            #changing state while in interactive mode throws exception
            raise ValueError('Cannot change autolife state when in interactive mode.')
        elif current_state == 'solitary':
            self.robot.set_autonomous_life(False)
        else:
            self.robot.set_autonomous_life(True)

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
       