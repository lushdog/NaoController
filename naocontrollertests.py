import unittest
import mock
import string
import random
import defaults

from mock import patch

import naocontroller as nc

class NaoControllerTests(unittest.TestCase):

    def test_do_connect_with_bad_ip_sets_is_connected_false(self):
        robot = nc.NaoController(None)
        robot.do_connect(['$$$', 9559])
        self.assertEqual(robot.is_connected, False)

    def test_do_connect_with_bad_port_sets_is_connected_false(self):
        robot = nc.NaoController(None)
        robot.do_connect(['192.168.1',9559])
        self.assertEqual(robot.is_connected, False)

    def mock_speech_proxy(self):
        robot = nc.NaoController(None)
        robot.is_connected = True
        robot.robot_proxies = {};
        robot.robot_proxies[robot.ANIM_SPEECH_LIB] = mock.Mock()
        robot.robot_proxies[robot.ANIM_SPEECH_LIB].say = mock.Mock()
        return robot
        
    def test_do_say_with_valid_args_invokes_say(self):
        robot = self.mock_speech_proxy()
        robot.get_say_inputs = mock.Mock(return_value=('foo', 'bar'))
        robot.do_say(None)
        robot.robot_proxies[robot.ANIM_SPEECH_LIB].say.assert_called_once_with('^startTag(foo) "\\rspd={0}\\bar" ^waitTag(foo)'.format(defaults.SPEECH_SPEED))

    '''
    def test_do_say_with_invalid_args(self):
        robot = self.mock_speech_proxy()
        robot.get_say_inputs = mock.Mock(return_value=('fo\"o', 'bar'))
        robot.do_say(None)
        robot.robot_proxies[robot.ANIM_SPEECH_LIB].say.assert_called_once_with('^startTag(fo\'o) "\\rspd={0}\\bar" ^waitTag(fo\'o)'.format(defaults.SPEECH_SPEED))
    '''

    '''
    def test_invoke_command_with_posture_calls_invoke_posture(self):
        robot = nc.NaoController()
        robot.invoke_speech = mock.Mock()
        robot.invoke_method = mock.Mock()
        robot.invoke_command(None, None, "Posture");
        robot.invoke_method.assert_called_once_with("Posture")
        self.assertEqual(robot.invoke_speech.call_count, 0)

    def test_invoke_method_with_sit_calls_invoke_sit(self):
        robot = nc.NaoController()
        robot.invoke_stand = mock.Mock()
        robot.invoke_sit = mock.Mock()
        robot.invoke_method('sit')
        robot.invoke_sit.assert_called_once
        self.assertEqual(robot.invoke_stand.call_count, 0)

    def test_invoke_method_with_stand_calls_invoke_stand(self):
        robot = nc.NaoController()
        robot.invoke_stand = mock.Mock()
        robot.invoke_sit = mock.Mock()
        robot.invoke_method('stand')
        robot.invoke_stand.assert_called_once
        self.assertEqual(robot.invoke_sit.call_count, 0)

    def test_invoke_method_with_unknown_posture_calls_nothing(self):
        robot = nc.NaoController()
        robot.invoke_stand = mock.Mock()
        robot.invoke_sit = mock.Mock()
        robot.invoke_method('unkownposture')
        self.assertEqual(robot.invoke_stand.call_count, 0)
        self.assertEqual(robot.invoke_sit.call_count, 0)

    def test_invoke_method_with_autolife(self):
        robot = nc.NaoController()
        robot.toggle_auto_life = mock.Mock()
        robot.invoke_method('autolife')
        self.assertEqual(robot.toggle_auto_life.call_count, 1)

    '''    
if __name__ == '__main__':
    unittest.main()
