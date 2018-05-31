import time
from SuperGLU.Core.Messaging import Message
from SuperGLU.Core.MessagingGateway import BaseService
from SuperGLU.Services.LoggingService.Constants import *
from SuperGLU.Services.LoggingService.Base_Learn_Logger import BaseLearnLogger

class SuperGLULearnLogger(BaseLearnLogger):

    '''
    Initialize the standard ITS logger service
        @param gateway: The parent gateway for this service
        @type gateway: Messaging_Gateway.MessagingGateway
        @param userId: Unique ID for the user
        @type userId: uuid string
        @param classroomId: Unique ID for the classroom cohort (optional). Leave as None if unknown.
        @type classroomId: uuid string
        @param taskId: Unique ID for the task being performed.
        @type taskId: uuid string
        @param url: The current base URL for the task that is being performed. This should not include situational parameters like the user id.
        @type url: url string
        @param activityType: The type of activity. This should be a unique system UUID (e.g., "AutoTutor_asdf2332gsa" or "www.autotutor.com/asdf2332gsa"). This ID should be the same for all activities presented by this system, since it will be used to query their results.
        @type activityType: uuid string
        @param id: The UUID for this service. If left blank, this will use a random UUID (recommended).
        @type id: string
    '''

    def __init__(self, gateway=None, userId=None, classroomId=None, taskId=None, url=None, activityType=None, context=None, anId=None):
        super(SuperGLULearnLogger, self).__init__(gateway, userId, classroomId, taskId, url, activityType, context, anId)

    '''Send the loaded message, for when the task is ready to start.
        Message Data: <frameName> | Loaded | <url> | true
        @param frameName: The name for the current window
        @type frameName: string
    '''

    def sendLoadedTask(self, frameName):
        msg = Message(frameName, LOADED_VERB, self._url, True)
        self.sendLoggingMessage(msg)

    '''
    Send the task completed message
        Message Data: <userId> | Completed | <taskId> | <score>
        @param score: A score between 0 and 1. Scores outside this range will be clipped to fit. If score None, task presumed incomplete/invalid.
        @type score: float
    '''
    def sendCompletedTask(self, score):
        score = self.clampToUnitV87alue(score)
        msg = Message(self._userId, COMPLETED_VERB, self._taskId, score)
        self.sendLoggingMessage(msg)

    '''
    Send if all steps completed message (or % complete, if unfinished)
        Message Data: <userId> | CompletedAllSteps | <taskId> | <percentComplete>
        @param percentComplete: The percentage of steps that were completed. In [0,1]. If None, assumed 100%.
        @param percentComplete: float
    '''
    def sendCompletedAllSteps(self, percentComplete):
        if percentComplete == None:
            percentComplete = 1.0
        percentComplete = self.clampToUnitValue(percentComplete)
        msg = Message(self._userId, COMPLETED_ALL_STEPS_VERB, self._taskId, percentComplete*1.0)
        self.sendLoggingMessage(msg)

    '''
    Send a message that a step was completed (or marked incomplete, alternatively).
        Message Data: <userId> | CompletedStep | <stepId> | <percentComplete>
        @param stepId: An id that represents the task situation (e.g., decision point) that the user completed or failed to complete. Uniquely represents some decision point in the current task.
        @type stepId: string
        @param isComplete: The amount of the step that was completed, from 0 (nothing completed) to 1 (fully complete).
        @type isComplete: float
    '''
    def sendCompletedStep(self, stepId, isComplete):
        if isComplete == None:
            isComplete = 1.0
        isComplete = self.clampToUnitValue(isComplete)
        msg = Message(self._userId, COMPLETED_STEP_VERB, stepId, 1.0*isComplete)
        self.sendLoggingMessage(msg)

    '''
    Send a KC Score about performance on a specific skill during the activity.
        KC scores override any default KC scores inferred from a task's Completed message
        (e.g., which might be assumed that KC's used to recommend the task are also those that
        are assessed by that same task).  Relevance is intended to be used to determine the level
        of confidence for each assessment, and can be left undefined if all scores have high confidence
        and all KC's used to select a task have been assessed by that task.
        Message Data: <userId> | KCScore | <kcName> | <score>
        @param kcName: The name of the knowledge component that was assessed during this task.
        @type kcName: string
        @param score: The score the system gave for this KC, from 0 to 1.
        @type score: float
        @param relevance: The credit or confidence of your assessment of that KC, from 0 (irrelevant) to 1 (strong confidence in this assessment).  Relevance of 0 should be used if a KC that is associated with choosing this task was not encountered during the task. Typically, relevance can be left undefined, which will default to 1.
        @type relevance: float
    '''

    def sendKCScore(self, kcName, score, relevance):
        if relevance == None:
            relevance = 1.0
        relevance = self.clampToUnitValue(relevance)
        score = self.clampToUnitValue(score)
        msg = Message(self._userId, KC_SCORE_VERB, kcName, score)
        msg.setContextValue(KC_RELEVANCE_KEY, relevance)
        self.sendLoggingMessage(msg)

    '''
    Send a Mastery score, which is a claim by a system about a user's overall knowledge
        about a knowledge component. This score is expected to be based on all evidence available
        to the system at the time when the KC mastery was calculated.
        Message Data: <userId> | Mastery | <kcName> | <score>
        @param kcName: The name of the knowledge component whose mastery level was estimated.
        @type kcName: string
        @param score: The score the system gave for this KC, from 0 to 1.
        @type score: float
        @param numObservations: A weighted sum for the number of observations that supports this estimate. Some observations might be worth less than one (e.g., because the context was only partly relevant), while other observations might be worth more than one (e.g., because they were received from systems which reported a large number of observations).
        @type numObservations: float
    '''
    def sendMastery(self, kcName, score, numObservations):
        score = self.clampToUnitValue(score)
        msg = Message(self._userId, MASTERY_VERB, kcName, score)
        if numObservations != None and numObservations > 0:
            msg.setContextValue(NUM_OBSERVATIONS_KEY, numObservations)
        self.sendLoggingMessage(msg)

    '''
    Notify that a hint was presented
        Message Data: <taskId> | TaskHint | <stepId> | <content>
        @param content: The content of the help given, such as text, raw HTML, a URL, an image link, or other data.
        @type: string
        @param stepId: An id that represents the task situation (e.g., decision point) where the learner received the hint.
        @type stepId: string
        @param helpType: The pedagogical intent of help that was given, such as positive feedback, negative feedback, etc.
        @type helpType: string
        @param contentType: The type of content that was presented (e.g., text, image, video, HTML).
        @type contentType: string
    '''
    def sendHint(self, content, stepId, helpType, contentType):
        self._sendHelpMessage(TASK_HINT_VERB, content, stepId, helpType, contentType)

    '''
    Notify that feedback was presented
        Message Data: <taskId> | TaskFeedback | <stepId> | <content>
        @param content: The content of the help given, such as text, raw HTML, a URL, an image link, or other data.
        @type: string
        @param stepId: An id that represents the task situation (e.g., decision point) where the learner received the feedback.
        @type stepId: string
        @param helpType: The pedagogical intent of help that was given, such as positive feedback, negative feedback, etc.
        @type helpType: string
        @param contentType: The type of content that was presented (e.g., text, image, video, HTML).
        @type contentType: string
    '''

    def sendFeedback(self, content, stepId, helpType, contentType):
        self._sendHelpMessage(TASK_FEEDBACK_VERB, content, stepId, helpType, contentType)

    #Notify that positive feedback was presented
    def sendPositiveFeedback(self, content, stepId, contentType):
        self.sendFeedback(content, stepId, POSITIVE_HELP_TYPE, contentType)

    #Notify that neutral feedback was presented
    def sendNeutralFeedback(self, content, stepId, contentType):
        self.sendFeedback(content, stepId, NEUTRAL_HELP_TYPE, contentType)

    #Notify that negative feedback was presented
    def sendNegativeFeedback(self, content, stepId, contentType):
        self.sendFeedback(content, stepId, NEGATIVE_HELP_TYPE, contentType)

    '''
    Notify that task was decomposed
        Message Data: <taskId> | TaskDecomposition | <stepId> | <content>
        @param content: The content of the help given, such as text, raw HTML, a URL, an image link, or other data.
        @type: string
        @param stepId: An id that represents the task situation (e.g., decision point) where the learner decomposed the task.
        @type stepId: string
        @param helpType: The pedagogical intent of help that was given, such as positive feedback, negative feedback, etc.
        @type helpType: string
        @param contentType: The type of content that was presented (e.g., text, image, video, HTML).
        @type contentType: string
    '''

    def sendTaskDecomposed(self, content, stepId, helpType, contentType):
        self._sendHelpMessage(TASK_DECOMPOSITION_VERB, content, stepId, helpType, contentType)

    '''
    Notify that some other help was presented. In general, this should be used
        only when more specific verbs such as Feedback or Hint are not appropriate.
        Message Data: <userId> | TaskHelp | <stepId> | <score>
        @param content: The content of the help given, such as text, raw HTML, a URL, an image link, or other data.
        @type: string
        @param stepId: An id that represents the task situation (e.g., decision point) where the learner received the help.
        @type stepId: string
        @param helpType: The pedagogical intent of help that was given, such as positive feedback, negative feedback, etc.
        @type helpType: string
        @param contentType: The type of content that was presented (e.g., text, image, video, HTML).
        @type contentType: string
    '''
    def sendHelp(self, content, stepId, helpType, contentType):
        self._sendHelpMessage(TASK_HELP_VERB, content, stepId, helpType, contentType)


    '''
    Notify that task presented some content. This can be at any time that
        new content was presented (e.g., moving to a new panel, etc.).
        Message Data: <taskId> | Presented | <elementId> | <content>
        @param elementId: The HTML element where the content was displayed (if relevant)
        @type elementId: string
        @param content: The content of the help given, such as text, raw HTML, a URL, an image link, or other data.
        @type: string
        @param stepId: An id that represents the task situation (e.g., decision point) where the learner received the help.
        @type stepId: string
        @param contentType: The type of content that was presented (e.g., text, image, video, HTML).
        @type contentType: string
    '''
    def sendPresented(self, elementId, content, stepId, contentType):
        if contentType == None and content != None:
            contentType = 'text'
            content = str(content)
        msg = Message(self._taskId, PRESENTED_VERB, elementId, content)
        msg.setContextValue(STEP_ID_KEY, stepId)
        msg.setContextValue(RESULT_CONTENT_TYPE_KEY, contentType)
        self.sendLoggingMessage(msg)

    '''
    Notify that user selected some element (e.g., in terms of HTML: making active)
        This should be used when the user has selected a choice or option, but has not
        necessarily submitted it (e.g., picking a dropdown but before hitting "Submit",
        or writing a text answer before submitting it or clearing it).
        Message Data: <userId> | SelectedOption | <elementId> | <content>
        @param elementId: The HTML element where the option was selected or provided.
        @type elementId: string
        @param content: The content of the selection chosen (e.g., the option or value)
        @type: string
        @param stepId: An id that represents the task situation (e.g., decision point) where the learner selected the option.
        @type stepId: string
        @param contentType: The type of content that was presented (e.g., text, image, video, HTML).
        @type contentType: string
    '''
    def sendSelectedOption(self, elementId, content, stepId, contentType):
        self._sendInputMessage(SELECTED_OPTION_VERB, elementId, content, stepId, contentType)

    '''
    Notify that user submitted an answer or choice.
        Message Data: <userId> | SubmittedAnswer | <elementId> | <content>
        @param elementId: The HTML element where the option was selected or provided.
        @type elementId: string
        @param content: The content of the submission or choice locked in (e.g., the option or value)
        @type: string
        @param stepId: An id that represents the task situation (e.g., decision point) where the learner submitted the value.
        @type stepId: string
        @param contentType: The type of content that was presented (e.g., text, image, video, HTML).
        @type contentType: string
    '''
    def sendSubmittedAnswer(self, elementId, content, stepId, contentType):
        self._sendInputMessage(SUBMITTED_ANSWER_VERB, elementId, content, stepId, contentType)

    '''
    Notify that user demonstrated a misconception.
        This requires the misconception ID, rather than the element.
        Message Data: <userId> | SubmittedAnswer | <misconceptionId> | <content>
        @param misconceptionId: An id that uniquely identifies this misconception across a variety of problems.
        @type misconceptionId: string
        @param content: The content of the submission or choice locked in (e.g., the option or value)
        @type: string
        @param stepId: An id that represents the task situation (e.g., decision point) where the learner's misconception was shown. Optional.
        @type stepId: string
        @param contentType: The type of content that was presented (e.g., text, image, video, HTML).
        @type contentType: string
    '''
    def sendMisconception(self, misconceptionId, content, stepId, contentType):
        self._sendInputMessage(MISCONCEPTION_VERB, misconceptionId, content, stepId, contentType)

    '''Send the overall level of system support given to the user for this task.
        This is the system's assessment of the level of support that was provided.
        Message Data: <userId> | TaskSupport | <taskId> | <supportLevel>
        @param supportLevel: Fraction of the total support given to the user during the task, in [0,1].
        @type supportLevel: float
    '''
    def sendTaskSupport(self, supportLevel):
        supportLevel = self.clampToUnitValue(supportLevel)
        msg = Message(self._userId, TASK_SUPPORT_VERB, self._taskId, supportLevel)
        self.sendLoggingMessage(msg)

    '''
    Send the overall number of help acts given. To be used when individual hints cannot be logged, but the aggregate can be.
        No need to use this if help actions can be logged individually.
        Message Data: <userId> | TaskHelpCount | <taskId> | <numHelpActs>
        @param numHelpActs: The total number of help acts provided during the task.
        @type numHelpActs: int
    '''
    def sendTaskHelpCount(self, numHelpActs):
        if numHelpActs < 0:
            numHelpActs = 0
        msg = Message(self._userId, TASK_HELP_COUNT_VERB, self._taskId, numHelpActs)
        self.sendLoggingMessage(msg)

    '''
    Send the words per second when user was expected to enter content
        Message Data: <userId>, WordsPerSecond, <evidence>, <value>
        @param value: The number of words per second, during times when input was expected.
        @type value: float
        @param evidence: Raw data used to infer this value, such as a list of [{'text' : '...', 'duration' : '5.4'}, ...]. Stored archivally, to allow recalculating differently, if needed.
        @type evidence: any JSON-serializable or Serialization.Serializable object
        @param stepId: An id that represents the task situation (e.g., decision point) where this evidence was collected. Optional.  If not given, this message should represent all the text input given to this task.
        @type stepId: string
    '''
    def sendWordsPerSecond(self, value, evidence, stepId):
            if value < 0:
                value = 0
            self._sendMetricMessage(WORDS_PER_SECOND_VERB, value, evidence, stepId, False)

    '''
    Send the actions per second when user was expected to interact with the system
        Message Data: <userId>, ActionsPerSecond, <evidence>, <value>
        @param value: The number of actions per second, during times when input was expected.
        @type value: float
        @param evidence: Raw data used to infer this value, such as a list of [{'actions' : ['a1', 'a2'], 'duration' : '5.4'}, ...]. Stored archivally, to allow recalculating differently, if needed.
        @type evidence: any JSON-serializable or Serialization.Serializable object
        @param stepId: An id that represents the task situation (e.g., decision point) where this evidence was collected. Optional.  If not given, this message should represent all the actions given to this task.
        @type stepId: string
    '''
    def sendActionsPerSecond(self, value, evidence, stepId):
            if value < 0:
                value = 0
            self._sendMetricMessage(ACTIONS_PER_SECOND_VERB, value, evidence, stepId, False)

    '''
    Send the semantic match for content submitted. Can be either for a single step (if stepId given)
        or for the whole task (if no stepId given).
        Message Data: <userId>, AnswerSemanticMatch, <evidence>, <value>
        @param value: The semantic match score, in [0,1]
        @type value: float
        @param evidence: Raw data used to infer this value, such as a list of [{'match' : 0.6, 'ideal' : 'pen', 'answer' : 'pencil'}, ...]. Stored archivally, to allow recalculating differently, if needed.
        @type evidence: any JSON-serializable or Serialization.Serializable object
        @param stepId: An id that represents the task situation (e.g., decision point) where this evidence was collected. Optional.  If not given, this message should represent all the actions given to this task.
        @type stepId: string
    '''
    def sendAnswerSemanticMatch(self, value, evidence, stepId):
        self._sendMetricMessage(ANSWER_SEMANTIC_MATCH_VERB, value, evidence, stepId, True)

    def sendPersistence(self, value, evidence, stepId):
        self._sendMetricMessage(PERSISTENCE_VERB, value, evidence, stepId, True)

    def sendImpetuousness(self, value, evidence, stepId):
        self._sendMetricMessage(IMPETUOUSNESS_VERB, value, evidence, stepId, True)

    def sendGamingTheSystem(self, value, evidence, stepId):
        self._sendMetricMessage(GAMING_SYSTEM_VERB, value, evidence, stepId, True)

    def sendConfusion(self, value, evidence, stepId):
        self._sendMetricMessage(CONFUSION_VERB, value, evidence, stepId, True)

    def sendDisengagement(self, value, evidence, stepId):
        self._sendMetricMessage(DISENGAGEMENT_VERB, value, evidence, stepId, True)

    def sendWheelspinning(self, value, evidence, stepId):
        self._sendMetricMessage(WHEELSPINNING_VERB, value, evidence, stepId, True)

    def sendRequestRecommendedTasks(self, userName, numberOfRecommendations):
        msg = Message(userName, RECOMMENDED_TASKS_VERB, numberOfRecommendations, "", "Request")
        self.sendLoggingMessage(msg)

    '''
    Internal Function to notify server that some help message was presented
        @param verb: The verb to use for the help log message
        @type verb: string
        @param content: The content of the help given, such as text, raw HTML, a URL, an image link, or other data.
        @type: string
        @param stepId: An id that represents the task situation (e.g., decision point) where the learner received the hint. Optional.
        @type stepId: string
        @param helpType: The pedagogical intent of help that was given, such as positive feedback, a prompt, etc. Optional.
        @type helpType: string
        @param contentType: The type of content that was presented (e.g., text, image, video, HTML). Defaults to text.
        @type contentType: string
    '''
    def _sendHelpMessage(self, verb, content, stepId, helpType, contentType):
        if (contentType == None) and content != None:
            contentType = 'text'
            content = str(content)
        if helpType == None:
            helpType = NEUTRAL_HELP_TYPE
        msg = Message(self._taskId, verb, stepId, content)
        msg.setContextValue(STEP_ID_KEY, stepId)
        msg.setContextValue(HELP_TYPE_KEY, helpType)
        msg.setContextValue(RESULT_CONTENT_TYPE_KEY, contentType)
        self.sendLoggingMessage(msg)

    '''
    Internal function to notify server that user submitted input
        @param verb: The verb to use for the user input message
        @type verb: string
        @param elementId: The HTML element where the user performed the interaction.
        @type elementId: string
        @param content: The content of the selection chosen (e.g., the option or value)
        @type: string
        @param stepId: An id that represents the task situation (e.g., decision point) where the learner selected the option. Optional.
        @type stepId: string
        @param contentType: The type of content that was presented (e.g., text, image, video, HTML).
        @type contentType: string
    '''
    def _sendInputMessage(self, verb, elementId, content, stepId, contentType):
        if ((contentType == None) and content != None):
            contentType = 'text'
            content = content.toString()
        msg = Message(self._userId, verb, elementId, content)
        msg.setContextValue(STEP_ID_KEY, stepId)
        msg.setContextValue(RESULT_CONTENT_TYPE_KEY, contentType)
        self.sendLoggingMessage(msg)

    '''
    Internal function for sending metric values
        @param verb: The verb to use for the metric message
        @type verb: string
        @param value: Value of the metric to send.
        @type value: numeric
        @param stepId: The stepId that the metric applies to. If None, applies to the task overall.
        @type stepId: string
        @param clampToUnit: If true, adjust value to fit between 0 and 1. Null values are not changed.
        @type clampToUnit: bool
    '''
    def _sendMetricMessage(self, verb, value, evidence,  stepId, clampToUnit):
        if evidence == None:
            evidence = []
        if clampToUnit:
            value = self.clampToUnitValue(value)
        msg = Message(self._userId, verb, evidence, value)
        msg.setContextValue(STEP_ID_KEY, stepId)
        self.sendLoggingMessage(msg)

    '''
    Add context to the message.  This adds the userId, taskId, classroomId,
        activityType, and duration so far. It also adds any service context items,
        followed by the parameter context. Context within the context parameter does
        not override any existing message context.
        @param msg: The original message to modify by adding context data.
        @type msg: Messaging.Message
        @param context: Dictionary of key-value items to add to the message context. Not used if keys already exist.
        @type context: object
        @return: Modified message in msg
        @rtype: Messaging.Message
    '''

    def addContext(self, msg, context):
        msg.setContextValue(USER_ID_KEY, self._userId)
        msg.setContextValue(TASK_ID_KEY, self._taskId)
        msg.setContextValue(CLASSROOM_ID_KEY, self._classroomId)
        msg.setContextValue(ACTIVITY_TYPE_KEY, self._activityType)
        msg.setContextValue(DURATION_KEY, self.calcDuration())
        for key in self._context:
            if not msg.hasContextValue(key):
                msg.setContextValue(key, self._context[key])
        for key in context:
            if not msg.hasContextValue(key):
                msg.setContextValue(key, context[key])
        return msg

    '''
    Finalize any post-processing of the message and then send it
        @param msg: Message to send
        @type msg: Messaging.Message
        @param context: Dictionary of key-value items to add to the message context. Not used if keys already exist.
        @type context: object
    '''
    def sendLoggingMessage(self, msg, context=None):
        msg = self.addContext(msg, context)
        self.sendMessage(msg)

    # values to fit within a [0,1] range
    def clampToUnitValue(self, val):
        if val != None:
            return min(max(val, 0.0), 1.0)
        return val
