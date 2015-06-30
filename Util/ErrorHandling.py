# -*- coding: utf-8 -*-
import copy
import logging
import traceback
import sys

# Optional: For catching UTF better
#from kitchen.text.converters import getwriter
#sys.stdout = getwriter('utf8')(sys.stdout)
#sys.stderr = getwriter('utf8')(sys.stderr)

IGNORE_ERRORS_MODE = 0
LOG_ERRORS_MODE = 1
RAISE_ERRORS_MODE = 2
VALID_ERROR_HANDLER_MODES = frozenset([IGNORE_ERRORS_MODE,
                                      LOG_ERRORS_MODE,
                                      RAISE_ERRORS_MODE])

# Default Error Mode
ERROR_MODE = RAISE_ERRORS_MODE

# Errors About Error Handling
class ErrorHandlerException(Exception): pass
class LoggedWarning(Exception): pass
class InvalidErrorHandlingMode(ErrorHandlerException): pass

ERROR_LOGGER = logging.getLogger("Application Log")
ERROR_LOGGER.addHandler(logging.StreamHandler())

#def attachLogFile(fileName):
#    pass
                
def errorHandler(errInfo, mode=None, warning=False):
    if errInfo is not None:
        errInfo = tuple(makeStandardEncoding(x) for x in errInfo)
    if mode is None:
        mode = _getErrorMode()
    if mode in (LOG_ERRORS_MODE, RAISE_ERRORS_MODE):
        if warning:
            ERROR_LOGGER.warning(u"INFO: %s", errInfo[1])
        else:
            ERROR_LOGGER.error(u"ERROR: \n%s", errInfo[2])
    if mode in (RAISE_ERRORS_MODE,):
        raise

def tryRaiseError(error, mode=None, stack=None):
    try:
        raise error
    except Exception:
        if stack is None:
            stack = full_stack()
        errorHandler(sys.exc_info()[:2] + (stack,), mode)

def logError(error, stack=None):
    tryRaiseError(error, LOG_ERRORS_MODE, stack)

def logWarning(*args, **kwds):
    try:
        raise LoggedWarning(' '.join([makeStandardEncoding(x) for x in args]))
    except LoggedWarning, err:
        if kwds.get('stack') is None:
            stack = full_stack()
        else:
            stack = kwds.get('stack')
        errorHandler(sys.exc_info()[:2] + (stack,),
                     LOG_ERRORS_MODE, True)
    
def _getErrorMode():
    return ERROR_MODE

def _setErrorMode(mode):
    global ERROR_MODE
    if mode in VALID_ERROR_HANDLER_MODES:
        ERROR_MODE = mode
    else:
        error = InvalidErrorHandlingMode("Attempted to set error mode to: %s"%(mode,))
        errorHandler(error)

def full_stack():
    """
    Cludgy workaround from StackOverflow User Tobias Kienzler
    Source: stackoverflow.com/questions/6086976/how-to-get-a-complete-exception-stack-trace-in-python/16589622#16589622
    """
    exc = sys.exc_info()[0]
    stack = traceback.extract_stack()[:-1]  # last one would be full_stack()
    if not exc is None:  # i.e. if an exception is present
        del stack[-1]       # remove call of full_stack, the printed exception
                            # will contain the caught exception caller instead
    trc = 'Traceback (most recent call last):\n'
    stackstr = trc + ''.join(traceback.format_list(stack))
    if not exc is None:
         stackstr += '  ' + traceback.format_exc().lstrip(trc)
    return stackstr

def makeStandardEncoding(x, encoding='UTF-8'):
    if isinstance(x, unicode):
        return x
    elif isinstance(x, str):
        return unicode(str(x), 'UTF-8', 'ignore')
    else:
        try:
            return unicode(x)
        except Exception:
            pass
        try:
            return unicode(str(x), 'UTF-8', 'ignore')
        except Exception:
            return u'(ERROR: COULD NOT DECODE!)'

if __name__ == '__main__':
    def aFunct(x):
        print x
        #raise Exception("AAA")
        logWarning("Warning, said it!")
        logError(Exception("Generic Exception!"))
        tryRaiseError(Exception("Generic Exception!"), IGNORE_ERRORS_MODE)
        print "Keep on trucking: ", x
        #tryRaiseError(Exception("Generic Exception!"), RAISE_ERRORS_MODE)

    def bFunct(x):
        aFunct(x)

    aFunct(1)
    bFunct(2)
    logWarning('AA')
    logWarning(u'ÂÂ')
    logWarning("ERROR FROM ATWS: ", 10, u'ÂÂ')
    logError(Exception('AA'))
    print "X", unicode(Exception(u'ÂÂ')), "X"
    logError(Exception(u'ÂÂ'))
    logError(Exception(u"ERROR FROM ATWS: 10 " + u'ÂÂ'))
