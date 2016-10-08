"""controller.py: 'Business layer' between client and robot"""

# pylint: disable=line-too-long,missing-docstring

class VideoController(object):
     
    def __init__(self, videorobot):
        self.robot = videorobot

    def get_picture(self, use_bottom_camera=False):
        return self.robot.get_remote_image(use_bottom_camera)

    def set_auto_exposure(self, auto_exposure, set_bottom_camera=False):
        try:
            clamped = self.clamp(0, int(auto_exposure), 3)
        except TypeError:
            print 'Exposure value must be an integer between 0 and 3.'
        return self.robot.set_auto_exposure(clamped, set_bottom_camera)

    @staticmethod
    def clamp(minvalue, value, maxvalue):
        return max(minvalue, min(value, maxvalue))
   
