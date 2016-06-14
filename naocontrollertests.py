import unittest
import mock
import string
import random

import naocontroller as nc

class NaoControllerTests(unittest.TestCase):

    def test_connection_bad_ip_returns_none(self):
        robot = nc.NaoController()
        robot.ip = '$$$'
        robot.port = 9559
        self.assertIsNone(robot.connect_to_robot())

    def test_connection_bad_port_returns_none(self):
        robot = nc.NaoController()
        robot.ip = '192.168.1.1'
        robot.port = '@@@'
        self.assertIsNone(robot.connect_to_robot())
    
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

    
    #test command_loop (non_exit_input with good date invokes command, non_exit_input with bad data does not invoke command)
        
    #regex tests
    def test_parse_command_empty(self):
        self.assertIsNone(nc.NaoController.parse_command(''))
    def test_parse_command_simple_valid_command_returns_valid(self):
        self.assertEqual(nc.NaoController.parse_command('"Speech" "Animation"'), ("Speech","Animation"))
    def test_parse_command_simple_invalid_command_returns_none(self):
        self.assertIsNone(nc.NaoController.parse_command('dfasdfasdfasdf'))
    def test_parse_command_too_many_quotes_command_returns_none(self):
        self.assertIsNone(nc.NaoController.parse_command('"Spee"ch" "Animation"'))
    def test_parse_command_missing_animation_command_returns_none(self):
        self.assertIsNone(nc.NaoController.parse_command('"Speech"'))
    def test_parse_command_no_space_command_returns_valid(self):
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
