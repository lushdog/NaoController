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
    _set_command_line(command_line)
    return _invoke_command('connect ')

@post('/send')
def send():
    return _invoke_command(request.json)

def _set_command_line(command_line):
    bottle.request.environ.get('beaker.session')['commandline'] = command_line

def _get_command_line():
    return bottle.request.environ.get('beaker.session')['commandline']

def _invoke_command(command):
    old_stdout = sys.stdout
    sys.stdout = new_stdout = StringIO()
    _get_command_line().onecmd(command)
    sys.stdout = old_stdout
    return new_stdout.getvalue()

bottle.run(app=APP, host='localhost', port=8080, debug=True)
