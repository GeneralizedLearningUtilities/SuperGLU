"""
Requires:
- MongoDB
- Packages: pymongo, kitchen, 
"""
import os
import sys
import time
import traceback
import json
import random
from functools import wraps

from threading import Thread

from Util.ErrorHandling import logError, logWarning
from Util.Serialization import serializeObject
from Util.SerializationDB import SerializableDBWrapper, SerializableMongoWrapper
from Core.MessagingGateway import HTTPMessagingGateway
from Core.Messaging import Message
from Services.LoggingService.LoggingService import CSVLoggingService, BadDialogCSVLogger

DEBUG_MODE = False
DEBUG_ON_VM = False

# Server Initialization
#------------------------------
def SetupServer(app=None, socketio=None, host='localhost', port=5000, debug=True):
    # Initial Setup
    global FLASK_CORE_APP, SOCKET_IO_CORE, DB_CONNECTION, MESSAGING_GATEWAY
    if app is None: app = FLASK_CORE_APP
    if socketio is None: socketio = SOCKET_IO_CORE
    aPort = int(os.getenv('PORT', port))
    if (aPort != port or host != 'localhost') and debug:
        host = '0.0.0.0'
        debug = False
        logWarning("Going to host 0")
    app.debug = bool(debug)

    #Allow some env specification of helpful test services
    services = [
        CSVLoggingService("logfile.csv"),
    ]
    if os.getenv('TESTSERVICE', ''):
        logWarning('SKO_Architecture.MessagingGateway.TestService will be run')
        from SKO_Architecture.MessagingGateway import TestService
        services.append(TestService())

    MESSAGING_GATEWAY = HTTPMessagingGateway(
        None,
        SOCKET_IO_CORE,
        flask.ext.socketio,
        services
    )

    return socketio

def StartServer(app=None, socketio=None, host='localhost', port=5000, debug=True):
    socketio = SetupServer(app, socketio, host, port, debug)
    Thread(target=background_thread).start()
    logWarning("Starting Socket App")
    try:
        socketio.run(app, host=host, port=port)
    except Exception as err:
        DB_CONNECTION.close()

def StartDebugServer(app=None, socketio=None):
    """ Use this for basic online debugging """
    StartServer(app, socketio, 'localhost', 5000, True)

def StartVMDebugServer(app=None, socketio=None):
    """ Use this when you want to run in a local VM using
    port forwarding on your host OS """
    StartServer(app, socketio, '0.0.0.0', 8081, True)

def StartDirectServer(app=None, socketio=None):
    """
    Use this for direct production debugging
    Warning: This is a little unsafe to use for longer
    periods, as you're giving admin rights to the app.
    """
    StartServer(app, socketio, '0.0.0.0', 80, False)

def StartProductionServer(app=None, socketio=None):
    """
    Use this for local production, with NGINX forwarding
    from 0.0.0.0:80 to 127.0.0.1:8000
    """
    StartServer(app, socketio, '127.0.0.1', 8081, False)

# Declarations occur here to prevent triggering during an import
if __name__ == '__main__' or __name__ == 'MinimalServer':
    # NOTE: For no good reason, these cause IDLE to reboot when importing sometimes
    from flask import Flask, render_template, session, request, abort, redirect, url_for, make_response
    import flask.ext.socketio
    #SocketIO, emit, join_room, leave_room

    # Basic Standup
    FLASK_CORE_APP = Flask(__name__, static_folder='../')
    FLASK_CORE_APP.debug = DEBUG_MODE
    FLASK_CORE_APP.config['SECRET_KEY'] = 'Please enter your own secret key. Not this default.'
    SOCKET_IO_CORE = flask.ext.socketio.SocketIO(FLASK_CORE_APP)
    WSGI_APP = FLASK_CORE_APP.wsgi_app

    # Service Setup
    MESSAGING_GATEWAY = None

    # Basic File Delivery
    #-----------------------------
    @FLASK_CORE_APP.route('/')
    def index():
        return render_template('index.html')

    @FLASK_CORE_APP.route('/templates/<path:path>')
    def template_imports(path):
        if path[-5:] in ('.html',):
            try:
                path = path.split('//')[-1]
                logWarning(path)
                return render_template(path)
            except Exception:
                abort(404)
        else:
            return abort(404)

    @FLASK_CORE_APP.route('/log/<path:path>')
    def logfile_imports(path):
        if path[-4:] in ('.log', '.csv'):
            try:
                path = path.split('//')
                path.insert(0, 'Services')
                path = '//'.join(path)
                logWarning(path)
                return FLASK_CORE_APP.send_static_file(path)
            except Exception:
                abort(404)
        else:
            return abort(404)

    # Message Handling
    #-----------------------------
    @SOCKET_IO_CORE.on('message', namespace='/messaging')
    def receive_message(message):
        try:
            MESSAGING_GATEWAY.onReceiveAJAXMessage(message)
        except Exception as err:
            if DEBUG_MODE:
                raise
            else:
                logError(err, stack=traceback.format_exc())

    def background_thread():
        #@TODO: TEST AND MAKE SURE THIS workS WITH GUNICORN (if we use that)
        try:
            MESSAGING_GATEWAY.processQueuedMessages()
        except Exception as err:
            if DEBUG_MODE:
                raise
            else:
                logError(err, stack=traceback.format_exc())
                MESSAGING_GATEWAY.processQueuedMessages()

    # Connection Monitoring
    #------------------------------
    @SOCKET_IO_CORE.on('connect', namespace='/messaging')
    def onConnect():
        logWarning("Connected")
        #flask.ext.socketio.emit('my response', {'data': 'Connected', 'count': 0})

    @SOCKET_IO_CORE.on('disconnect', namespace='/messaging')
    def onDisconnect():
        logWarning('Client disconnected')


    #First check to see if HOST and PORT were specified in the
    #environment - if so, we use those values directly and skip
    #the "usual" logic below
    envHost, envPort = None, None
    try:
        envHost = os.getenv('HOST', None)
        envPort = int(os.getenv('PORT', 0))
    except:
        pass

    if envHost and envPort:
        logWarning("Using Host/Port from environment: %s:%d" % (envHost, envPort))
        StartServer(FLASK_CORE_APP, SOCKET_IO_CORE, envHost, envPort, DEBUG_MODE)
    elif DEBUG_MODE:
        StartDebugServer(FLASK_CORE_APP, SOCKET_IO_CORE)
    elif DEBUG_ON_VM:
        StartVMDebugServer(FLASK_CORE_APP, SOCKET_IO_CORE)
    elif False:
        StartDirectServer(FLASK_CORE_APP, SOCKET_IO_CORE)
    else:
        StartProductionServer(FLASK_CORE_APP, SOCKET_IO_CORE)
