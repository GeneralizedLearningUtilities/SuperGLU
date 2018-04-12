import time
from SuperGLU.Core.Messaging import Message
from SuperGLU.Core.MessagingGateway import BaseService

LOADED_VERB = "Loaded";

RECOMMENDED_TASKS_VERB = "RecommendedTasks";

# Task Performance Verbs
COMPLETED_VERB = 'Completed',                       # Finished task, return result (e.g., score)
COMPLETED_ALL_STEPS_VERB = 'CompletedAllSteps',     # Completed all steps (true/false/% steps completed)
COMPLETED_STEP_VERB = 'CompletedStep',              # Completed a given task step
KC_SCORE_VERB = 'KnowledgeComponentScore';          # A score for a KC (e.g., performance on a given task)

# Task Adaptive Support Verbs
TASK_HELP_VERB = 'TaskHelp',                        # User received some other type of help on a task
TASK_HINT_VERB = 'TaskHint',                        # User received a hint (e.g., next step) on a task
TASK_FEEDBACK_VERB = 'TaskFeedback',                # User received reactive feedback (e.g., error correction, approval)
TASK_DECOMPOSITION_VERB = 'TaskDecomposition';      # User received a decomposed task (i.e., broken into subtasks)

# Task User Input Verbs
PRESENTED_VERB = 'Presented',                       # User was presented with some element
SELECTED_OPTION_VERB = 'SelectedOption',            # User selected some option or element
SUBMITTED_ANSWER_VERB = 'SubmittedAnswer',          # An answer submitted by a user
MISCONCEPTION_VERB = 'Misconception',               # User demonstrated a specific bug or misconception
TASK_SUPPORT_VERB = 'TaskSupport',                  # Overall level of support given to the user during task
TASK_HELP_COUNT_VERB = 'TaskHelpCount';             # Overall number of hints user received during the task.

# Peripheral Metrics Verbs - Calculated by Task
WORDS_PER_SECOND_VERB = 'WordsPerSecond',           # # Words per second, for text-input interactions (e.g., natural language ITS)
ACTIONS_PER_SECOND_VERB = 'ActionsPerSecond',       # # Actions per second (e.g., selecting choices, attempting to answer)
ANSWER_SEMANTIC_MATCH_VERB = 'AnswerSemanticMatch', # Match of an answer for the user to some ideal(s)
PERSISTENCE_VERB = 'Persistence',                   # Metric for persistence (e.g., continuing despite failure)
IMPETUOUSNESS_VERB = 'Impetuousness',               # Metric for impetuousness (e.g., answering overly quickly, carelessness)
GAMING_SYSTEM_VERB = 'GamingTheSystem',             # Metric for gaming the system (e.g., hint abuse)
WHEELSPINNING_VERB = 'WheelSpinning',               # Metric for wheel spinning (e.g., continued failure on similar skills w/o improvement)
CONFUSION_VERB = 'Confusion',                       # Metric for confusion (e.g., moderate delays, poor answer cohesion, video metrics)
DISENGAGEMENT_VERB = 'Disengagement',               # Metric for disengagement (e.g., long delays, inattentive gaze, leaning back in chair)
MASTERY_VERB = 'Mastery';

# Context Keys
USER_ID_KEY = 'userId',                             # Unique identifier for the user
DURATION_KEY = 'duration',                          # Duration spent on the task
TASK_ID_KEY = 'taskId',                             # ID for the task being performed
STEP_ID_KEY = 'stepId',                             # Unique ID for the current step or state.
                                                    # Intended to help to compare different user or system behavior in a comparable task state.
CLASSROOM_ID_KEY = 'classroomId',					# Unique ID for the classroom
ACTIVITY_TYPE_KEY = 'activityType',                 # Type of activity being performed
TOPIC_ID_KEY = 'topicId',                           # Topic ID for the current activity
KC_RELEVANCE_KEY = 'KCRelevance',                   # Knowledge component relevance
NUM_OBSERVATIONS_KEY = 'numberOfObservations',      # Number of observations for some behavior that is measured
HELP_TYPE_KEY = 'helpType',                         # Type of the help provided (e.g., Positive, Negative, neutral)
RESULT_CONTENT_TYPE_KEY = 'resultContentType';      # Type for the content of the help or other media (e.g., 'text', 'html', 'jpg')

# Other Constants
UNKNOWN_PREFIX = 'Unknown',
POSITIVE_HELP_TYPE = 'Positive',
NEUTRAL_HELP_TYPE = 'Neutral',
NEGATIVE_HELP_TYPE = 'Negative';


class SuperGLULearnLogger(BaseLearningLoggerService):


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

    def __init__(gateway, userId, classroomId, taskId, url, activityType, context, id):
        super(SuperGLULearnLogger, self).__init__(userId, classroomId, taskId, url, activityType, context, id)

    /********************************
         **  LOG MESSAGE GENERATORS    **
     ********************************/

    '''Send the loaded message, for when the task is ready to start.
        Message Data: <frameName> | Loaded | <url> | true
        @param frameName: The name for the current window
        @type frameName: string
    '''

    def sendLoadedTask(frameName):
        msg = Message(frameName, LOADED_VERB, self._url, true);
        self.sendLoggingMessage(msg);

    '''
    Send the task completed message
        Message Data: <userId> | Completed | <taskId> | <score>
        @param score: A score between 0 and 1. Scores outside this range will be clipped to fit. If score None, task presumed incomplete/invalid.
        @type score: float
    '''
    def sendCompletedTask(score):
        score = self.clampToUnitV87alue(score);
        msg = Message(self._userId, COMPLETED_VERB, self._taskId, score);
        self.sendLoggingMessage(msg);

    '''
    Send if all steps completed message (or % complete, if unfinished)
        Message Data: <userId> | CompletedAllSteps | <taskId> | <percentComplete>
        @param percentComplete: The percentage of steps that were completed. In [0,1]. If None, assumed 100%.
        @param percentComplete: float
    '''
    def sendCompletedAllSteps(percentComplete):
        if percentComplete == None:
            percentComplete = 1.0
        percentComplete = self.clampToUnitValue(percentComplete);
        msg = Message(self._userId, COMPLETED_ALL_STEPS_VERB, self._taskId, percentComplete*1.0);
        self.sendLoggingMessage(msg);

    '''
    Send a message that a step was completed (or marked incomplete, alternatively).
        Message Data: <userId> | CompletedStep | <stepId> | <percentComplete>
        @param stepId: An id that represents the task situation (e.g., decision point) that the user completed or failed to complete. Uniquely represents some decision point in the current task.
        @type stepId: string
        @param isComplete: The amount of the step that was completed, from 0 (nothing completed) to 1 (fully complete).
        @type isComplete: float
    '''
    def sendCompletedStep(stepId, isComplete):
        if isComplete == None:
            isComplete = 1.0
        isComplete = self.clampToUnitValue(isComplete);
        msg = Message(self._userId, COMPLETED_STEP_VERB, stepId, 1.0*isComplete);
        self.sendLoggingMessage(msg);

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

    def sendKCScore(kcName, score, relevance):
        if relevance == None:
            relevance = 1.0
        relevance = self.clampToUnitValue(relevance);
        score = self.clampToUnitValue(score);
        msg = Message(self._userId, KC_SCORE_VERB, kcName, score);
        msg.setContextValue(KC_RELEVANCE_KEY, relevance);
        self.sendLoggingMessage(msg);

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
    def sendMastery(kcName, score, numObservations):
        score = self.clampToUnitValue(score);
        msg = Message(self._userId, MASTERY_VERB, kcName, score);
        if numObservations != None and numObservations > 0:
            msg.setContextValue(NUM_OBSERVATIONS_KEY, numObservations);
        }
        self.sendLoggingMessage(msg);

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
    def sendHint(content, stepId, helpType, contentType):
        self._sendHelpMessage(TASK_HINT_VERB, content, stepId, helpType, contentType);

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

    def sendFeedback(content, stepId, helpType, contentType):
        self._sendHelpMessage(TASK_FEEDBACK_VERB, content, stepId, helpType, contentType)

    #Notify that positive feedback was presented
    def sendPositiveFeedback(content, stepId, contentType):
        self.sendFeedback(content, stepId, POSITIVE_HELP_TYPE, contentType)

    #Notify that neutral feedback was presented
    def sendNeutralFeedback(content, stepId, contentType):
        self.sendFeedback(content, stepId, NEUTRAL_HELP_TYPE, contentType)

    #Notify that negative feedback was presented
    def sendNegativeFeedback(content, stepId, contentType):
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

    def sendTaskDecomposed(content, stepId, helpType, contentType):
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
    def sendHelp(content, stepId, helpType, contentType):
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
    def sendPresented(elementId, content, stepId, contentType):
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
    def sendSelectedOption(elementId, content, stepId, contentType):
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
    def sendSubmittedAnswer(elementId, content, stepId, contentType):
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
    def sendMisconception(misconceptionId, content, stepId, contentType):
        self._sendInputMessage(MISCONCEPTION_VERB, misconceptionId, content, stepId, contentType)

    '''Send the overall level of system support given to the user for this task.
        This is the system's assessment of the level of support that was provided.
        Message Data: <userId> | TaskSupport | <taskId> | <supportLevel>
        @param supportLevel: Fraction of the total support given to the user during the task, in [0,1].
        @type supportLevel: float
    '''
    def sendTaskSupport(supportLevel):
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
    def sendTaskHelpCount(numHelpActs):
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
    def sendWordsPerSecond(value, evidence, stepId):
            if value < 0:
                value = 0
            self._sendMetricMessage(WORDS_PER_SECOND_VERB, value, evidence, stepId, false)

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
    def sendActionsPerSecond(value, evidence, stepId):
            if value < 0:
                value = 0
            self._sendMetricMessage(ACTIONS_PER_SECOND_VERB, value, evidence, stepId, false)

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
    def sendAnswerSemanticMatch(value, evidence, stepId):
        self._sendMetricMessage(ANSWER_SEMANTIC_MATCH_VERB, value, evidence, stepId, true)

    def sendPersistence(value, evidence, stepId):
        self._sendMetricMessage(PERSISTENCE_VERB, value, evidence, stepId, true);

    def sendImpetuousness(value, evidence, stepId):
        self._sendMetricMessage(IMPETUOUSNESS_VERB, value, evidence, stepId, true);

    def sendGamingTheSystem(value, evidence, stepId):
        self._sendMetricMessage(GAMING_SYSTEM_VERB, value, evidence, stepId, true);

    def sendConfusion(value, evidence, stepId):
        self._sendMetricMessage(CONFUSION_VERB, value, evidence, stepId, true);

    def sendDisengagement(value, evidence, stepId):
        self._sendMetricMessage(DISENGAGEMENT_VERB, value, evidence, stepId, true);

    def sendWheelspinning(value, evidence, stepId):
        self._sendMetricMessage(WHEELSPINNING_VERB, value, evidence, stepId, true);

    def sendRequestRecommendedTasks(userName, numberOfRecommendations):
        msg = Message(userName, RECOMMENDED_TASKS_VERB, numberOfRecommendations, "", "Request")
        self.sendLoggingMessage(msg);

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
    def _sendHelpMessage(verb, content, stepId, helpType, contentType):
        if ((contentType == None) && content != None){
            contentType = 'text';
            content = content.toString();
        }
        if (helpType == None){ helpType = NEUTRAL_HELP_TYPE;}
        var msg = Message(self._taskId, verb, stepId, content);
        msg.setContextValue(STEP_ID_KEY, stepId);
        msg.setContextValue(HELP_TYPE_KEY, helpType);
        msg.setContextValue(RESULT_CONTENT_TYPE_KEY, contentType);
        self.sendLoggingMessage(msg);

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
    def _sendInputMessage(verb, elementId, content, stepId, contentType):
        if ((contentType == None) and content != None):
            contentType = 'text';
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
    def _sendMetricMessage(verb, value, evidence,  stepId, clampToUnit):
        if evidence == None:
            evidence = []
        if clampToUnit:
            value = self.clampToUnitValue(value)
        msg = Message(self._userId, verb, evidence, value)
        msg.setContextValue(STEP_ID_KEY, stepId)
        self.sendLoggingMessage(msg)

    # values to fit within a [0,1] range
    def clampToUnitValue(val):
        if val != None:
            return Math.min(Math.max(val, 0.0), 1.0)
        return val
