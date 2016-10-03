"""robot.py: Thin class that handles creating proxies and making calls to NaoQi API"""
from PIL import Image
from naoqi import ALProxy
import vision_definitions

# pylint: disable=line-too-long,missing-docstring

class VideoRobot(object):

    def __init__(self):
        self.video_proxy = None

    def connect(self, host, port):
        print 'Video - Connecting to robot on {0}:{1}...'.format(host, port)
        try:
            self.video_proxy = ALProxy("ALVideoDevice", host, port)
        except Exception as exception: # pylint: disable=broad-except
            raise ValueError('Could not create proxy:{0}', format(exception))

    def get_remote_image(self, use_bottom_camera=False):
        camera_index = vision_definitions.kBottomCamera if use_bottom_camera else vision_definitions.kTopCamera
        resolution = vision_definitions.kVGA
        colorspace = vision_definitions.kRGBColorSpace 
        fps = 1
        
        print 'subscribing...'
        subscription = self.video_proxy.subscribeCamera('Vision', camera_index, resolution, colorspace, fps)
        if subscription is None:
            print 'Failed to subscribe to camera.'

        print 'taking picture and transfer...'
        capture = self.video_proxy.getImageRemote(subscription)
        if capture is None:
            print 'Failed to retrieve image remotely.'

        print 'unsubscribing...'
        if not subscription is None:
            unsubscribe_success = self.video_proxy.unsubscribe(subscription)
            if not unsubscribe_success:
                print 'Failed to unsubscribe to camera.'

        image = None
        if capture is not None:
            width = capture[0]
            height = capture[1]
            data = capture[6]
            try:
                print 'converting image...'
                image = Image.frombytes("RGB", (width, height), data)
                image.save("camImage.png", "PNG")
                print 'done'
                #image.show()
            except ValueError as error:
                print 'Invalid parameter passed to image creation: {0}'.format(error)
            finally:
                self.video_proxy.releaseImage(capture)
        return image
