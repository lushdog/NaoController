'''video_tests.py:  video_controller.py and video_test.py tests'''
import unittest
import mock
import video_controller as controller
import video_robot as robot

# pylint: disable=line-too-long,missing-docstring,invalid-name,protected-access

class VideoTests(unittest.TestCase):

    def test_robot_connect_with_invalid_ip_raises_value_error(self):
        self.assertRaises(Exception, robot.VideoRobot().connect, '255.255.255.255', 9559)

    def test_robot_connect_with_bad_port_sets_is_connected_false(self):
        self.assertRaises(Exception, robot.VideoRobot().connect, '1.1.1.1', 0000)

    def test_robot_camera_subscription_failed_cameras_are_none(self):
        bot = robot.VideoRobot()
        bot.video_proxy = mock.Mock()
        bot.video_proxy.subscribeCamera.return_value = None
        bot._subscribe_to_cameras()
        for x in range(len(bot.cameras)):
            self.assertIsNone(bot.cameras[x])

    def test_robot_get_remote_image_null_returned_from_robot_returns_none_image(self):
        bot = robot.VideoRobot()
        bot.video_proxy = mock.Mock()
        bot.video_proxy.getImageRemote.return_value = None
        self.assertIsNone(bot.get_remote_image())

    def test_robot_convert_capture_to_image_throws_when_passed_invalid_param_types(self):
        self.assertRaises(TypeError, robot.VideoRobot._convert_capture_to_image, 'a', 'a', 'a', 'a')

    def test_robot_convert_capture_to_image_throws_when_passed_invalid_param_value(self):
        self.assertRaises(ValueError, robot.VideoRobot._convert_capture_to_image, 1, 1, 'A', 1)

    def test_clamp_below_min_clamps_to_min(self):
        self.assertEquals(controller.VideoController.clamp(0, -5, 10), 0)
        self.assertEquals(controller.VideoController.clamp(0, 0, 10), 0)

    def test_clamp_above_max_clamps_to_max(self):
        self.assertEquals(controller.VideoController.clamp(0, 15, 10), 10)
        self.assertEquals(controller.VideoController.clamp(0, 10, 10), 10)

    def test_clam_mid_no_clamp(self):
        self.assertEquals(controller.VideoController.clamp(0, 2, 3), 2)

if __name__ == '__main__':
    unittest.main()
