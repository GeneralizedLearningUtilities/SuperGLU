LOADED_VERB = "Started"

RECOMMENDED_TASKS_VERB = "RecommendedTasks"

XAPI_LOG_VERB = "XAPILogStatement"

# Task Performance Verbs
COMPLETED_VERB = 'Completed'                       # Finished task, return result (e.g., score)
COMPLETED_ALL_STEPS_VERB = 'CompletedAllSteps'     # Completed all steps (true/false/% steps completed)
COMPLETED_STEP_VERB = 'CompletedStep'              # Completed a given task step
KC_SCORE_VERB = 'KnowledgeComponentScore'          # A score for a KC (e.g., performance on a given task)

# Task Adaptive Support Verbs
TASK_HELP_VERB = 'TaskHelp'                        # User received some other type of help on a task
TASK_HINT_VERB = 'TaskHint'                        # User received a hint (e.g., next step) on a task
TASK_FEEDBACK_VERB = 'TaskFeedback'                # User received reactive feedback (e.g., error correction, approval)
TASK_DECOMPOSITION_VERB = 'TaskDecomposition'      # User received a decomposed task (i.e., broken into subtasks)

# Task User Input Verbs
PRESENTED_VERB = 'Presented'                       # User was presented with some element
SELECTED_OPTION_VERB = 'SelectedOption'            # User selected some option or element
SUBMITTED_ANSWER_VERB = 'SubmittedAnswer'          # An answer submitted by a user
MISCONCEPTION_VERB = 'Misconception'               # User demonstrated a specific bug or misconception
TASK_SUPPORT_VERB = 'TaskSupport'                  # Overall level of support given to the user during task
TASK_HELP_COUNT_VERB = 'TaskHelpCount'             # Overall number of hints user received during the task.

# Peripheral Metrics Verbs - Calculated by Task
WORDS_PER_SECOND_VERB = 'WordsPerSecond'           # # Words per second, for text-input interactions (e.g., natural language ITS)
ACTIONS_PER_SECOND_VERB = 'ActionsPerSecond'       # # Actions per second (e.g., selecting choices, attempting to answer)
ANSWER_SEMANTIC_MATCH_VERB = 'AnswerSemanticMatch' # Match of an answer for the user to some ideal(s)
PERSISTENCE_VERB = 'Persistence'                   # Metric for persistence (e.g., continuing despite failure)
IMPETUOUSNESS_VERB = 'Impetuousness'               # Metric for impetuousness (e.g., answering overly quickly, carelessness)
GAMING_SYSTEM_VERB = 'GamingTheSystem'             # Metric for gaming the system (e.g., hint abuse)
WHEELSPINNING_VERB = 'WheelSpinning'               # Metric for wheel spinning (e.g., continued failure on similar skills w/o improvement)
CONFUSION_VERB = 'Confusion'                       # Metric for confusion (e.g., moderate delays, poor answer cohesion, video metrics)
DISENGAGEMENT_VERB = 'Disengagement'               # Metric for disengagement (e.g., long delays, inattentive gaze, leaning back in chair)
MASTERY_VERB = 'Mastery'

# Context Keys
USER_ID_KEY = 'userId'                             # Unique identifier for the user
DURATION_KEY = 'duration'                          # Duration spent on the task
TASK_ID_KEY = 'taskId'                             # ID for the task being performed
STEP_ID_KEY = 'stepId'                             # Unique ID for the current step or state.
                                                   # Intended to help to compare different user or system behavior in a comparable task state.
CLASSROOM_ID_KEY = 'classroomId'		   # Unique ID for the classroom
TOPIC_ID_KEY = 'topicId'                           # Topic ID for the current activity
KC_RELEVANCE_KEY = 'KCRelevance'                   # Knowledge component relevance
NUM_OBSERVATIONS_KEY = 'numberOfObservations'      # Number of observations for some behavior that is measured
HELP_TYPE_KEY = 'helpType'                         # Type of the help provided (e.g., Positive, Negative, neutral)
RESULT_CONTENT_TYPE_KEY = 'resultContentType'      # Type for the content of the help or other media (e.g., 'text', 'html', 'jpg')
ACTIVITY_TREE_KEY = 'serialized_activitytree'

# Other Constants
UNKNOWN_PREFIX = 'Unknown'
POSITIVE_HELP_TYPE = 'Positive'
NEUTRAL_HELP_TYPE = 'Neutral'
NEGATIVE_HELP_TYPE = 'Negative'

# xAPI Verbs
ProcessCoachFeedback = TASK_FEEDBACK_VERB
RegisterResponse = "Scored"
SelectedResponse = "Submitted"
ProcessCoachHint = TASK_HINT_VERB
SendHint = "Presented"
SendFeedback = "Presented"
SendResponse = "Speech"
SendChoice = "Presented"
PotentialFeedback= "PotentialTaskFeedback"
Coach = "Launched"
LoadingAAR = "Launched"
BeginAAR = "Started"
DoOver= "Presented"
ClickedItem = "SelectedOption"
CoachConfiguration= "Initialized"
AppStart = "Started"
LogIn = "Logged-in"
VideoPlayBackStart= "Played"
WatchedEntireMovieClip= "Completed"
PotentialHint= "PotentialTaskFeedback"
EndAAR= "Completed"
Calculations= "Scored"
Sustain= "Scored"
VHUtterance= "Speech"
Validating= "Unimportant"
Change= "Unimportant"
utteranceMatch= "Redundant"
RandomizedChoices= "Interaction"
RemoveDuplicateFeedback= "Unimportant"
GetAARSummary= "Assessment"
AfterActionReviewSummary= "Unimportant"
CompletionStatus= COMPLETED_VERB
Calculation= "Scored"
AppStop= "Terminated"
Exiting= "Terminated"
Diagnose= "Progressed"
MASTERED_VERB = "mastered"
