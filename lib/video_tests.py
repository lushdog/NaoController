'''core_tests.py tests'''
import unittest
from mock import patch
import mock
import video_controller as controller
import video_robot as robot
import defaults

# pylint: disable=line-too-long,missing-docstring,invalid-name

class VideoTests(unittest.TestCase):

    def test_robot_connect_with_invalid_ip_raises_value_error(self):
        self.assertRaises(ValueError, robot.VideoRobot().connect, '255.255.255.255', 9559)

    def test_robot_connect_with_bad_port_sets_is_connected_false(self):
        self.assertRaises(ValueError, robot.VideoRobot().connect, '1.1.1.1', 0000)

if __name__ == '__main__':
    unittest.main()
