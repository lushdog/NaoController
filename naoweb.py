from cStringIO import StringIO
import bottle
from beaker.middleware import SessionMiddleware

import naocommandline as commandline

# pylint: disable=missing-docstring

SESSION_OPTS = {
    'session.type' : 'memory',
    'session.auto' : 'true',
    'session.timeout' : '600'
}

APP = SessionMiddleware(bottle.app(), SESSION_OPTS)

'''
@hook('before_request')
def setup_request():
    request.session = bottle.request.environ.get('beaker.session')
'''

@bottle.route('/static/<filename:path>')
def send_static(filename):
    return bottle.static_file(filename, root='static')

@bottle.route('/')
@bottle.view('naoweb')
def main():
    command_line = commandline.NaoCommandLine(None)
    command_line.use_rawinput = False
    _set_command_line(command_line)
    return None

@bottle.post('/command')
def run_command():
    """Runs naocommandline command, returns console output and sets connected cookie"""
    output = _invoke_command(bottle.request.json['command']) #pylint: disable=unsubscriptable-object
    bottle.response.set_cookie("naoconnected", '1' if _get_command_line().is_connected else '0')
    return output

@bottle.route('/camera')
def get_camera_image_top():
    return get_camera_image()

@bottle.route('/camera/<camera_name>')
def get_camera_image(camera_name='top'):
    """Takes a picture with top or bottom camera and returns the image contents in png format
        encoded in base64. 
    """
    use_bottom_camera = (camera_name == 'bottom')
    image = None
    try:
        video_controller = _get_command_line().video_controller
        image = video_controller.get_picture(use_bottom_camera)
    except (KeyError, AttributeError):
        bottle.abort(400, "Must /connect first.")
    except (ValueError, TypeError):
        bottle.abort(400, "Invalid value sent to server.")
    except Exception: # pylint: disable=broad-except
        bottle.abort(500, "Error on server.")

    if image is not None:
        output = StringIO()
        image.save(output, "JPEG", quality=90, progressive=True)
        contents = output.getvalue().encode("base64")
        output.close()
        #contents = contents.split('\n')[0] #uncommenting this may help
        return contents
    else:
        return None 
    
def _set_command_line(command_line):
    session = bottle.request.environ.get('beaker.session')
    session['commandline'] = command_line

def _get_command_line():
    return bottle.request.environ.get('beaker.session')['commandline']

def _invoke_command(command):
    """Redirects 'console' output, invokes commandline-style command and returns console output
        Note: NaoCommandLine catches most every exception and ouputs error messages to console
        which is what naoweb does as well therefore no all invoked commands will return 200 OK.
    """
    command_line = _get_command_line()
    old_stdout = _get_command_line().stdout
    command_line.stdout = new_stdout = StringIO()
    command = command_line.precmd(command) 
    command_line.onecmd(command)
    command_line.stdout = old_stdout
    return new_stdout.getvalue()

bottle.run(app=APP, host='localhost', port=8080, debug=True)
