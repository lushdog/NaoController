import sys
from cStringIO import StringIO 
import bottle
from bottle import request, route, SimpleTemplate, view, static_file, post
from beaker.middleware import SessionMiddleware

import naocontroller.examples.commandline.naocommandline as commandline

#pylint: disable=missing-docstring

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

@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='static')

@route('/')
@view('naoweb')
def main():
    return None

@route('/connect')
def connect():
    command_line = commandline.NaoCommandLine(None)
    command_line.use_rawinput = False
    command_line.onecmd('connect ')
    beaker_session = bottle.request.environ.get('beaker.session')
    beaker_session['commandline'] = command_line
    return None

@post('/send')
def send():
    beaker_session = bottle.request.environ.get('beaker.session')
    command_line = beaker_session['commandline']
    command = request.json

    old_stdout = sys.stdout
    sys.stdout = new_stdout = StringIO()
    command_line.onecomd(command)
    sys.stdout = old_stdout
    return new_stdout.getValue()

'''
@bottle.route('/test')
def test():
  s = bottle.request.environ.get('beaker.session')
  s['test'] = s.get('test',0) + 1
  s.save()
  return 'Test counter: %d' % s['test']
'''

bottle.run(app=APP, host='localhost', port=8080, debug=True)
