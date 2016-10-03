"""core_robot.py: Thin class that handles creating proxies and making calls to NaoQi API"""
import math
from naoqi import ALProxy

# pylint: disable=line-too-long,missing-docstring

class CoreRobot(object):

    def __init__(self):
        self.animated_speech_proxy = None
        self.motion_proxy = None
        self.posture_proxy = None
        self.awareness_proxy = None
        self.autonomous_move_proxy = None
        self.autonomous_life_proxy = None

    def connect(self, host, port):
        """Takes connection params and builds list of ALProxies"""
        print 'Core - Connecting to robot on {0}:{1}...'.format(host, port)
        try:
            self.animated_speech_proxy = ALProxy("ALAnimatedSpeech", host, port)
            self.motion_proxy = ALProxy("ALMotion", host, port)
            self.posture_proxy = ALProxy("ALRobotPosture", host, port)
            self.awareness_proxy = ALProxy("ALBasicAwareness", host, port)
            self.autonomous_move_proxy = ALProxy("ALAutonomousMoves", host, port)
            self.autonomous_life_proxy = ALProxy("ALAutonomousLife", host, port)
        except Exception as exception: # pylint: disable=broad-except
            raise ValueError('Could not create proxy:{0}', format(exception))
        self.set_autonomous_life(False)

    def say(self, animated_speech):
        self.animated_speech_proxy.say(animated_speech) 

    def move(self, rotation, distance):
        motion = self.motion_proxy
        motion.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])
        motion.setMotionConfig([["ENABLE_STIFFNESS_PROTECTION", True]])
        motion.setCollisionProtectionEnabled('Arms', True)
        motion.setExternalCollisionProtectionEnabled('All', True)
        motion.moveTo(0, 0, rotation)
        motion.moveTo(distance, 0, 0)

    def open_hand(self, hand):
        self.motion_proxy.openHand(hand)
 
    def close_hand(self, hand):
        self.motion_proxy.closeHand(hand)

    def set_stiffness(self, joint, stiffness):
        print 'Setting {0} to stiffness {1}...'.format(joint, stiffness)
        try:
            self.motion_proxy.stiffnessInterpolation(joint, stiffness, 1.0) 
        except Exception as exception: # pylint: disable=broad-except
            print 'Error setting {0} stiffness to {1}:{2}'.format(joint, stiffness, exception)

    def set_joint_angle(self, joint, angle_degrees, speed=0.1):
        print 'Setting {0} to {1} angle in degrees...'.format(joint, angle_degrees)
        try:
            self.motion_proxy.setAngles(joint, math.radians(angle_degrees), speed)
        except Exception as exception: # pylint: disable=broad-except
            print 'Error setting {0} angle to {1}:{2}'.format(joint, angle_degrees, exception)

    def set_pose(self, pose):
        self.posture_proxy.goToPosture(pose, 0.5) 
      
    def set_autonomous_life(self, set_on):
        self.print_sub_system_update(set_on, 'Autonomous Life')
        target_state = 'solitary' if set_on else 'disabled'
        self.autonomous_life_proxy.setState(target_state)
        
    def get_autonomous_life_state(self):
        return self.autonomous_life_proxy.getState()
  
    def set_autonomous_moves(self, set_on):
        self.print_sub_system_update(set_on, 'Autonomous Moves')
        target_state = 'backToNeutral' if set_on else 'none'
        self.autonomous_move_proxy.setBackgroundStrategy(target_state)
        
    def set_awareness(self, set_on):
        self.print_sub_system_update(set_on, 'Basic Awareness')
        if set_on:
            self.awareness_proxy.startAwareness() 
        else:
            self.awareness_proxy.stopAwareness()

    def set_breathing(self, set_on):
        self.print_sub_system_update(set_on, 'body breathing')
        self.motion_proxy.setBreathEnabled('Body', set_on)
        self.print_sub_system_update(set_on, 'arm breathing')
        self.motion_proxy.setBreathEnabled('Arms', set_on)

    def set_move_arms_enabled(self, left_arm, right_arm):
        self.motion_proxy.setMoveArmsEnabled(left_arm, right_arm)

    @staticmethod
    def print_sub_system_update(set_on, sub_process):
        on_off = ['off', 'on']
        print 'Turning {0} {1}...'.format(on_off[set_on], sub_process)
