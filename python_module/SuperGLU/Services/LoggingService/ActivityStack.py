from SuperGLU.Util.Serialization import SuperGlu_Serializable, tokenizeObject, untokenizeObject


class ActivityStack(SuperGlu_Serializable):
    '''
    This class tracks the entering and exiting of xAPI Activities with the assumption that
    each new activity is always a part of the last entered activity, or the sole activity being
    pursued.

    '''

    ACTIVITY_STACK_KEY = "activityStack"

    def __init__(self):
        '''
        Constructor
        '''
        super(ActivityStack, self).__init__()
        self._activityStack = []

    def saveToToken(self):
        token = super(ActivityStack, self).saveToToken()
        token[ActivityStack.ACTIVITY_STACK_KEY] = tokenizeObject(self._activityStack)
        return token
    
    def initializeFromToken(self, token, context=None):
        super(ActivityStack, self).initializeFromToken(token, context)
        self._activityStack = untokenizeObject(token.get(ActivityStack.ACTIVITY_STACK_KEY, None))

    def accessTopElement(self):
        if len(self._activityStack) > 0:
            return self._activityStack[-1]
        else:
            return None

    def enterActivity(self, myobject):
        self._activityStack.append(myobject)

    def exitActivity(self):
        if len(self._activityStack) > 0:
            self._activityStack.pop()

    def __str__(self):
        return str(self._activityStack)
