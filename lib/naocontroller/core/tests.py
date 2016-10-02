'''controller.py tests'''
import unittest
import mock
#from mock import patch
from naocontroller.core import controller
from naocontroller.defaults import defaults

# disable bad method name linting
# pragma pylint: disable=C0103,R0904, C0111

class ControllerTests(unittest.TestCase):

    def test_do_connect_with_invalid_ip_sets_is_connected_false(self):
        c = controller.Controller()
        c.connect('255.255.255.255', 9559)
        self.assertEqual(c.robot.is_connected, False)

    def test_do_connect_with_bad_port_sets_is_connected_false(self):
        c = controller.Controller()
        c.connect('1.1.1.1', 0000)
        self.assertEqual(c.robot.is_connected, False)
    
    @staticmethod
    def test_controller_say_with_valid_args_invokes_robot_say():
        c = controller.Controller()
        c.robot.is_connected = True
        c.robot.say = mock.Mock()
        c.say('foo', 'bar')
        c.robot.say.assert_called_once_with(
            '^startTag(foo) "\\rspd={0}\\bar" ^waitTag(foo)'.format(defaults.SPEECH_SPEED))

    @staticmethod
    def test_controller_say_with_special_characters_invokes_robot_say_with_clean_inputs():
        c = controller.Controller()
        c.robot.is_connected = True
        c.robot.say = mock.Mock()
        c.say('fo\'o', 'b\"ar')
        c.robot.say.assert_called_once_with(
            '^startTag(foo) "\\rspd={0}\\bar" ^waitTag(foo)'.format(defaults.SPEECH_SPEED))

    def test_invoke_toggle_autolife_sets_correct_state_based_on_all_possible_current_states(self):
        c = controller.Controller()
        c.robot.is_connected = True
        c.robot.proxies = {}
        c.robot.get_autonomous_life_state = mock.Mock()
        c.robot.get_autonomous_life_state.side_effect = [
            'interactive', 'solitary', 'disabled']

        c.robot.set_autonomous_life = mock.Mock()
        c.toggle_autolife()
        self.assertEqual(c.robot.set_autonomous_life.call_count, 0)

        c.robot.set_autonomous_life.reset_mock()
        c.toggle_autolife()
        c.robot.set_autonomous_life.assert_called_once_with(False)

        c.robot.set_autonomous_life.reset_mock()
        c.toggle_autolife()
        c.robot.set_autonomous_life.assert_called_once_with(True)

    def test_clean_speech_removes_non_alpha(self):
        c = controller.Controller()
        self.assertEqual('test', c.clean_animated_speech('test'))
        self.assertEqual('tet', c.clean_animated_speech('te$t'))
        self.assertEqual('tet', c.clean_animated_speech('te^t'))
        self.assertEqual('tet', c.clean_animated_speech('te\'t'))
        self.assertEqual('tet', c.clean_animated_speech('te\"t'))

    def test_clean_speech_converts_basic_punctuation(self):
        c = controller.Controller()
        self.assertEqual('te\\pau=800\\t', c.clean_animated_speech('te.t'))
        self.assertEqual('te\\pau=400\\t', c.clean_animated_speech('te,t'))
        self.assertEqual('te t', c.clean_animated_speech('te t'))
 
if __name__ == '__main__':
    unittest.main()
