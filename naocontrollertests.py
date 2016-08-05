import unittest
import defaults
import mock
#from mock import patch

import naocontroller as nc

# disable bad method name linting
# pragma pylint: disable=C0103
class NaoControllerTests(unittest.TestCase):

    def test_do_connect_with_bad_ip_sets_is_connected_false(self):
        robot = nc.NaoController(None)
        robot.do_connect('255.255.255.255 9559')
        self.assertEqual(robot.is_connected, False)

    def test_do_connect_with_bad_port_sets_is_connected_false(self):
        robot = nc.NaoController(None)
        robot.do_connect('1.1.1.1 0000')
        self.assertEqual(robot.is_connected, False)

    @staticmethod
    def mock_speech_proxy():
        robot = nc.NaoController(None)
        robot.is_connected = True
        robot.robot_proxies = {}
        robot.robot_proxies[robot.ANIM_SPEECH_LIB] = mock.Mock()
        robot.robot_proxies[robot.ANIM_SPEECH_LIB].say = mock.Mock()
        return robot
        
    def test_do_say_with_valid_args_invokes_say(self):
        robot = self.mock_speech_proxy()
        robot.get_say_inputs = mock.Mock(return_value=('foo', 'bar'))
        robot.do_say(None)
        robot.robot_proxies[robot.ANIM_SPEECH_LIB].say.assert_called_once_with(
            '^startTag(foo) "\\rspd={0}\\bar" ^waitTag(foo)'.format(defaults.SPEECH_SPEED))

    def test_do_say_with_special_characters_invokes_say_with_clean_inputs(self):
        robot = self.mock_speech_proxy()
        robot.get_say_inputs = mock.Mock(return_value=('fo\'o', 'b\"ar'))
        robot.do_say(None)
        robot.robot_proxies[robot.ANIM_SPEECH_LIB].say.assert_called_once_with(
            '^startTag(foo) "\\rspd={0}\\bar" ^waitTag(foo)'.format(defaults.SPEECH_SPEED))

    def test_invoke_toggle_autolife(self):
        robot = nc.NaoController(None)
        robot.robot_proxies = {}
        robot.robot_proxies[robot.AUTONOMOUS_LIFE_LIB] = mock.Mock()
        robot.robot_proxies[robot.AUTONOMOUS_LIFE_LIB].getState = mock.Mock()
        robot.robot_proxies[robot.AUTONOMOUS_LIFE_LIB].getState.side_effect = [
            'interactive', 'solitary', 'disabled']

        robot.set_autonomous_life = mock.Mock()
        robot.invoke_toggle_autolife()
        self.assertEqual(robot.set_autonomous_life.call_count, 0)

        robot.set_autonomous_life.reset_mock()
        robot.invoke_toggle_autolife()
        robot.set_autonomous_life.assert_called_once_with(False)

        robot.set_autonomous_life.reset_mock()
        robot.invoke_toggle_autolife()
        robot.set_autonomous_life.assert_called_once_with(True)

    def test_clean_speech_removes_non_alpha(self):
        robot = nc.NaoController(None)
        self.assertEqual('test', robot.clean_speech('test'))
        self.assertEqual('tet', robot.clean_speech('te$t'))
        self.assertEqual('tet', robot.clean_speech('te^t'))
        self.assertEqual('tet', robot.clean_speech('te\'t'))
        self.assertEqual('tet', robot.clean_speech('te\"t'))

    def test_clean_speech_keeps_basic_punctuation(self):
        robot = nc.NaoController(None)
        self.assertEqual('te.t', robot.clean_speech('te.t'))
        self.assertEqual('te,t', robot.clean_speech('te,t'))
        self.assertEqual('te t', robot.clean_speech('te t'))
 
if __name__ == '__main__':
    unittest.main()
