import unittest
import mock
import string

import naocontroller as nc

class NaoControllerTests(unittest.TestCase):

    #NaoController class tests
    def test_print_usage_called_from_main(self):
        robot = nc.NaoController()
        robot.connect_to_robot = mock.Mock() #fake connection
        robot.invoke_command = mock.Mock()   #fake invoking the command
        robot.get_command = mock.Mock(side_effect=['exit']) #exit the command loop
        robot.print_usage = mock.Mock()
        
        robot.main()
        robot.print_usage.assert_called_with()

    #test connect_to_robot (get proper exception and don't enter loop)
    #test command_loop (typing exit does indeed exit, 2 valid then exit, invalid then exit, invalid command prints usage)
    #test invoke_command (
        
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
