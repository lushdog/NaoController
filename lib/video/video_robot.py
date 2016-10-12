"""robot.py: Thin class that handles creating proxies and making calls to NaoQi API"""
import datetime
from PIL import Image
from naoqi import ALProxy
import vision_definitions

# pylint: disable=line-too-long,missing-docstring

class VideoRobot(object):

    FPS = 5
    RESOLUTION = vision_definitions.kVGA
    COLOR_SPACE = vision_definitions.kRGBColorSpace

    def __init__(self):
        self.video_proxy = None
        self.cameras = [None, None] #two cameras on Nao, top and bottom

    def connect(self, host, port):
        print 'Video - Connecting to robot on {0}:{1}...'.format(host, port)
        try:
            self.video_proxy = ALProxy("ALVideoDevice", host, port)
        except Exception as exception: # pylint: disable=broad-except
            raise Exception('Could not create proxy: {0}', format(exception))
        self._subscribe_to_cameras()

    def _subscribe_to_cameras(self):
        for camera_index in range(len(self.cameras)):
            camera_name = 'nc_camera_{0}'.format(camera_index)
            camera = self.video_proxy.subscribeCamera(camera_name, camera_index, self.RESOLUTION, self.COLOR_SPACE, self.FPS)
            self.cameras[camera_index] = camera
            if camera is None:
                print 'Failed to subscribe to camera: {0}'.format(camera_index)

    def get_remote_image(self, use_bottom_camera=False):
        camera_index = vision_definitions.kBottomCamera if use_bottom_camera else vision_definitions.kTopCamera
        camera = self.cameras[camera_index]
        capture = self.video_proxy.getImageRemote(camera)
        if capture is None:
            print 'Failed to retrieve image remotely from camera: {0}'.format(camera_index)
        image = None
        if capture is not None:
            width = capture[0]
            height = capture[1]
            data = capture[6]
            try:    
                image = self._convert_capture_to_image(width, height, 'RGB', data)
                #timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
                #image.save(timestamp + '.png', "PNG")
                #image.show()
            except IOError as error: 
                print 'Error saving image: {0}'.format(error)
            finally:
                self.video_proxy.releaseImage(camera)
        return image

    @staticmethod
    def _convert_capture_to_image(width, height, mode, data):
        image = None
        try:
            image = Image.frombytes(mode, (width, height), data)
        except ValueError as error:
            raise ValueError('Invalid parameter passed to image creation: {0}'.format(error))
        except TypeError as error:
            raise TypeError('Invalid type passed to image creation: {0}'.format(error))
        return image

    def set_auto_exposure(self, target_exposure, set_bottom_camera=False):
        if target_exposure < 0 or target_exposure > 3:
            raise ValueError('target_exposure must be between 0 and 3')

        camera_index = vision_definitions.kBottomCamera if set_bottom_camera else vision_definitions.kTopCamera
        success = self.video_proxy.setParameter(camera_index, vision_definitions.kCameraExposureAlgorithmID, target_exposure)

        if success:
            print 'Successfully changed camera {0} exposure to {1}'.format(camera_index, target_exposure)
        else:
            print 'Failed to change camera {0} exposure to {1}'.format(camera_index, target_exposure)
        return success

    def __del__(self):
        print 'Unsubscribing from cameras...'
        for camera_index in range(len(self.cameras)):
            camera = self.cameras[camera_index]
            if not camera is None:
                unsubscribe_success = self.video_proxy.unsubscribe(camera)
                if not unsubscribe_success:
                    print 'Failed to unsubscribe to camera: {0}'.format(camera_index)
