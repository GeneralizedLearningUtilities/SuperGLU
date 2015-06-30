# -*- coding: utf-8 -*-
"""
A simple JavaScript Interpreter that wraps the Rhino JS.jar file
Requires: Java installation, Rhino package
"""
import io
import os
import subprocess
from SuperGLU.Util.ErrorHandling import tryRaiseError

def _find_js_cmd():
    #Easiest - they just told us the command to use
    js_cmd = os.environ.get("JS_INTERPRETER", None)
    if js_cmd:
        return js_cmd
    
    #Going to need to search the hard way
    
    locs = [
        ("lib", "rhino", "js.jar"),
        ("lib", "rhino.jar"),
        ("lib", "js.jar"),
    ]
    
    java_homes = [
        os.environ.get('JAVA_HOME', None),
        os.path.join(os.path.sep, "usr", "share", "java")
    ]

    js_path = None
    for java_home in java_homes:
        if not java_home:
            continue
        for loc in locs:
            js_path = os.path.join(java_home, *loc)
            if os.path.isfile(js_path):
                return 'java -jar "%s"' % (js_path,)
    
    #Nothing could be found
    return None

RUN_JS_COMMAND = _find_js_cmd()
HAS_JS_INTERPRETER = True if RUN_JS_COMMAND else False

# Exception Classes
class MissingJSInterpreterError(NotImplementedError): pass
class JSRuntimeError(RuntimeError): pass

if HAS_JS_INTERPRETER:
    def executeJS(jsFile, dirName='', *params):
        fullFile = os.path.join(dirName, jsFile)
        
        allParams = [fullFile]
        if params:
            allParams.extend(list(params))
        
        command = RUN_JS_COMMAND + ' ' + ' '.join(allParams)
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err =  p.communicate()
        if len(err) == 0:
            return out
        else:
            raise JSRuntimeError("\n" + err)
else:
    def executeJS(jsFile, dirName='', *params):
        errMsg = "Rhino JS Interpreter not found!"
        tryRaiseError(MissingJSInterpreterError(errMsg))
