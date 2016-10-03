"""controller.py: 'Business layer' between client and robot"""

# pylint: disable=line-too-long,missing-docstring

class VideoController(object):
     
    def __init__(self, videorobot):
        self.robot = videorobot

    def get_picture(self, use_bottom_camera=False):
        self.robot.get_remote_image(use_bottom_camera)

   
