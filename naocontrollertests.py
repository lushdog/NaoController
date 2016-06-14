import unittest
import mock
import string
import random

import naocontroller as nc

class NaoControllerTests(unittest.TestCase):

    def test_connection_bad_ip_returns_all_proxies_none(self):
        robot = nc.NaoController()
        robot.ip = '$$$'
        robot.port = 9559
        robot.connect_to_robot()
        self.assertIsNone(robot.tts_proxy)
        self.assertIsNone(robot.motion_proxy)
        self.assertIsNone(robot.posture_proxy)

    def test_connection_bad_port_returns_none(self):
        robot = nc.NaoController()
        robot.ip = '192.168.1.1'
        robot.port = '@@@'
        robot.connect_to_robot()
        self.assertIsNone(robot.tts_proxy)
        self.assertIsNone(robot.motion_proxy)
        self.assertIsNone(robot.posture_proxy)
    
    def test_command_loop_first_input_is_exit_does_exit(self):
        robot = nc.NaoController()
        robot.get_command = mock.Mock(side_effect=['exit'])
        robot.command_loop(None)
        self.assertEqual(robot.get_command.call_count, 1)

    def test_command_loop_not_first_input_is_exit_loop_then_exit(self):
        robot = nc.NaoController()
        robot.get_command = mock.Mock(side_effect=['foo', 'exit'])
        robot.parse_command = mock.Mock(return_value=[None])
        robot.invoke_command = mock.Mock()
        robot.command_loop(None)
        self.assertEqual(robot.parse_command.call_count, 1)
        self.assertEqual(robot.invoke_command.call_count, 1)

    def test_invoke_command_with_speech_calls_invoke_speech(self):
        robot = nc.NaoController()
        robot.invoke_speech = mock.Mock()
        robot.invoke_posture = mock.Mock()
        robot.invoke_command("Speech", "Animation", None);
        robot.invoke_speech.assert_called_once_with("Speech", "Animation")
        self.assertEqual(robot.invoke_posture.call_count, 0)

    def test_invoke_command_with_posture_calls_invoke_posture(self):
        robot = nc.NaoController()
        robot.invoke_speech = mock.Mock()
        robot.invoke_posture = mock.Mock()
        robot.invoke_command(None, None, "Posture");
        robot.invoke_posture.assert_called_once_with("Posture")
        self.assertEqual(robot.invoke_speech.call_count, 0)

    def test_invoke_posture_with_sit_calls_invoke_sit(self):
        robot = nc.NaoController()
        robot.invoke_stand = mock.Mock()
        robot.invoke_sit = mock.Mock()
        robot.invoke_posture('sit')
        robot.invoke_sit.assert_called_once
        self.assertEqual(robot.invoke_stand.call_count, 0)

    def test_invoke_posture_with_stand_calls_invoke_stand(self):
        robot = nc.NaoController()
        robot.invoke_stand = mock.Mock()
        robot.invoke_sit = mock.Mock()
        robot.invoke_posture('stand')
        robot.invoke_stand.assert_called_once
        self.assertEqual(robot.invoke_sit.call_count, 0)

    def test_invoke_posture_with_unknown_posture_calls_nothing(self):
        robot = nc.NaoController()
        robot.invoke_stand = mock.Mock()
        robot.invoke_sit = mock.Mock()
        robot.invoke_posture('unkownposture')
        self.assertEqual(robot.invoke_stand.call_count, 0)
        self.assertEqual(robot.invoke_sit.call_count, 0)
    
    #test command_loop (non_exit_input with good date invokes command, non_exit_input with bad data does not invoke command)
        
    #regex tests
    def test_parse_command_empty(self):
        self.assertIsNone(nc.NaoController.parse_command(''))
    def test_parse_command_simple_speech_animation_returns_valid(self):
        self.assertEqual(nc.NaoController.parse_command('"Speech" "Animation"'), ("Speech","Animation", None))
    def test_parse_command_stand_posture_returns_valid(self):
        self.assertEqual(nc.NaoController.parse_command('Stand'), (None, None, 'Stand'))
    def test_parse_command_sit_posture_returns_valid(self):
        self.assertEqual(nc.NaoController.parse_command('Sit'), (None, None, 'Sit'))
    def test_parse_command_unsupported_posture_returns_invalid(self):
        self.assertIsNone(nc.NaoController.parse_command('UnsupportedPosture'))
    def test_parse_command_posture_with_spaces_returns_invalid(self):
        self.assertIsNone(nc.NaoController.parse_command('Posture Space'))
    def test_parse_command_too_many_quotes_command_returns_none(self):
        self.assertIsNone(nc.NaoController.parse_command('"Spee"ch" "Animation"'))
    def test_parse_command_missing_animation_command_returns_none(self):
        self.assertIsNone(nc.NaoController.parse_command('"Speech"'))
    def test_parse_command_no_space_command_returns_none(self):
        self.assertIsNone(nc.NaoController.parse_command('"Speech""Animation"'))
    def test_parse_command_trailing_command_returns_none(self):
        self.assertIsNone(nc.NaoController.parse_command('"Speech" "Animation"dfadfasdf'))
    def test_parse_command_invalid_chars_in_animation_returns_none(self):
        self.assertIsNone(nc.NaoController.parse_command('"Speech" "Ani#m@tion"'))
    def test_parse_command_quotes_in_speech_returns_none(self):
        self.assertIsNone(nc.NaoController.parse_command('"Sp"eech" "Animation"'))
    def test_parse_command_no_animation_returns_none(self):
        self.assertIsNone(nc.NaoController.parse_command('"Speech Animation"'))
                         
if __name__ == '__main__':
    unittest.main()
