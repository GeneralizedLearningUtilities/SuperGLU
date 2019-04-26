package edu.usc.ict.superglu.core;

/**
 * This class is simply a collection of basic verbs for the SuperGLU Messaging
 * system
 * 
 * @author auerbach
 *
 */
public class MessagingVerbConstants
{

    // Internal functionality Verbs
    public static final String HEARTBEAT_VERB = "Heartbeat";
    public static final String LOADED_VERB = "Loaded";

    // Message concerns the results of the recommender.
    public static final String RECOMMENDED_TASKS_VERB = "RecommendedTasks";
    // // Finished task, return result (e.g., score)
    public static final String COMPLETED_VERB = "Completed";
    // // Completed all steps (true/false/% steps completed)
    public static final String COMPLETED_ALL_STEPS_VERB = "CompletedAllSteps";
    // // Completed a given task step
    public static final String COMPLETED_STEP_VERB = "CompletedStep";
    // // A score for a KC (e.g., performance on a given task)
    public static final String KC_SCORE_VERB = "KnowledgeComponentScore";

    // Task Adaptive Support Verbs

    // User received some other type of help on a task
    public static final String TASK_HELP_VERB = "TaskHelp";
    // User received a hint (e.g., next step) on a task
    public static final String TASK_HINT_VERB = "TaskHint";
    // User received reactive feedback (e.g., error correction, approval)
    public static final String TASK_FEEDBACK_VERB = "TaskFeedback";
    // User received a decomposed task (i.e., broken into subtasks)
    public static final String TASK_DECOMPOSITION_VERB = "TaskDecomposition";

    // Task User Input Verbs

    // User was presented with some element
    public static final String PRESENTED_VERB = "Presented";
    // User selected some option or element
    public static final String SELECTED_OPTION_VERB = "SelectedOption";
    // An answer submitted by a user
    public static final String SUBMITTED_ANSWER_VERB = "SubmittedAnswer";
    // User demonstrated a specific bug or misconception
    public static final String MISCONCEPTION_VERB = "Misconception";
    // Overall level of support given to the user during task
    public static final String TASK_SUPPORT_VERB = "TaskSupport";
    // Overall number of hints user received during the task.
    public static final String TASK_HELP_COUNT_VERB = "TaskHelpCount";
    
    
    public static final String XAPI_LOG_VERB ="XAPILogStatement";

}
    



    

/* 
//Peripheral Metrics Verbs - Calculated by Task
WORDS_PER_SECOND_VERB = "WordsPerSecond"           // // Words per second, for text-input interactions (e.g., natural language ITS)
ACTIONS_PER_SECOND_VERB = "ActionsPerSecond"       // // Actions per second (e.g., selecting choices, attempting to answer) 
ANSWER_SEMANTIC_MATCH_VERB = "AnswerSemanticMatch" // Match of an answer for the user to some ideal(s)
PERSISTENCE_VERB = "Persistence"                   // Metric for persistence (e.g., continuing despite failure)
IMPETUOUSNESS_VERB = "Impetuousness"               // Metric for impetuousness (e.g., answering overly quickly, carelessness)
GAMING_SYSTEM_VERB = "GamingTheSystem"             // Metric for gaming the system (e.g., hint abuse)
WHEELSPINNING_VERB = "WheelSpinning"               // Metric for wheel spinning (e.g., continued failure on similar skills w/o improvement)
CONFUSION_VERB = "Confusion"                       // Metric for confusion (e.g., moderate delays, poor answer cohesion, video metrics)
DISENGAGEMENT_VERB = "Disengagement"               // Metric for disengagement (e.g., long delays, inattentive gaze, leaning back in chair)
MASTERY_VERB = "Mastery"

//Context Keys
CLASS_ID_CONTEXT_KEY = "classId"
SESSION_ID_CONTEXT_KEY = "sessionId"
USER_ID_CONTEXT_KEY = "userId"                             // Unique identifier for the user
DURATION_CONTEXT_KEY = "duration"                          // Duration spent on the task, 
TASK_ID_CONTEXT_KEY = "taskId"                             // ID for the task being performed
STEP_ID_CONTEXT_KEY = "stepId"                             // Unique ID for the current step or state.
ACTIVITY_TYPE_CONTEXT_KEY = "activityType"                 // Type of activity being performed
KC_RELEVANCE_CONTEXT_KEY = "KCRelevance"                   // Knowledge component relevance
HELP_TYPE_CONTEXT_KEY = "helpType"                         // Type of the help provided (e.g., Positive, Negative, neutral)
RESULT_CONTENT_TYPE_CONTEXT_KEY = "resultContentType"      // Type for the content of the help or other media (e.g., "text", "html", "jpg")
STUDENT_MODEL_CONTEXT_KEY = "studentModel"                 // student model for the student to which this message pertains

*/
