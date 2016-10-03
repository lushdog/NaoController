'''core_tests.py tests'''
import unittest
from mock import patch
import mock
import core_controller as controller
import core_robot as robot
import defaults

# pylint: disable=line-too-long,missing-docstring,invalid-name

class CoreTests(unittest.TestCase):

    def test_robot_connect_with_invalid_ip_raises_value_error(self):
        self.assertRaises(ValueError, robot.CoreRobot().connect, '255.255.255.255', 9559)

    def test_robot_connect_with_bad_port_sets_is_connected_false(self):
        self.assertRaises(ValueError, robot.CoreRobot().connect, '1.1.1.1', 0000)

    def test_controller_invoke_toggle_autolife_sets_correct_state_based_on_all_possible_current_states(self):
        corebot = robot.CoreRobot()
        corebot.get_autonomous_life_state = mock.Mock()
        corebot.get_autonomous_life_state.side_effect = [
            'interactive', 'solitary', 'disabled']

        corebot.set_autonomous_life = mock.Mock()

        coretroller = controller.CoreController(corebot)
        coretroller.toggle_autolife()
        self.assertEqual(corebot.set_autonomous_life.call_count, 0)

        corebot.set_autonomous_life.reset_mock()
        coretroller.toggle_autolife()
        coretroller.robot.set_autonomous_life.assert_called_once_with(False)

        corebot.set_autonomous_life.reset_mock()
        coretroller.toggle_autolife()
        corebot.set_autonomous_life.assert_called_once_with(True)

    @staticmethod
    def test_controller_say_with_valid_args_invokes_robot_say():
        with patch('core_robot.CoreRobot') as mock_robot:
            controller.CoreController(mock_robot).say('foo', 'bar')
            mock_robot.say.assert_called_once_with(
                '^startTag(foo) "\\rspd={0}\\bar" ^waitTag(foo)'.format(defaults.SPEECH_SPEED))

    @staticmethod
    def test_controller_say_with_special_characters_invokes_robot_say_with_clean_inputs():
        with patch('core_robot.CoreRobot') as mock_robot:
            controller.CoreController(mock_robot).say('fo\'o', 'b\"ar')
            mock_robot.say.assert_called_once_with(
                '^startTag(foo) "\\rspd={0}\\bar" ^waitTag(foo)'.format(defaults.SPEECH_SPEED))

    def test_clean_speech_removes_non_alpha(self):
        self.assertEqual('test', controller.CoreController.clean_animated_speech('test'))
        self.assertEqual('tet', controller.CoreController.clean_animated_speech('te$t'))
        self.assertEqual('tet', controller.CoreController.clean_animated_speech('te^t'))
        self.assertEqual('tet', controller.CoreController.clean_animated_speech('te\'t'))
        self.assertEqual('tet', controller.CoreController.clean_animated_speech('te\"t'))

    def test_clean_speech_converts_basic_punctuation(self):
        self.assertEqual('te\\pau=800\\t', controller.CoreController.clean_animated_speech('te.t'))
        self.assertEqual('te\\pau=400\\t', controller.CoreController.clean_animated_speech('te,t'))
        self.assertEqual('te t', controller.CoreController.clean_animated_speech('te t'))
 
if __name__ == '__main__':
    unittest.main()
