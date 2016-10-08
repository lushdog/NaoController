import bottle
from bottle import request, route, hook
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

@route('/')
@route('/connect')
def connect():
    command_line = commandline.NaoCommandLine(None)
    command_line.do_connect('')
    request.session['commandline'] = command_line
    request.session['foo'] = 'bar'

@route('/something')
def something():
    return request.session['foo']

bottle.run(app=APP, host='localhost', port=8080, debug=True)
