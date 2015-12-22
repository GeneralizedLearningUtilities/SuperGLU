# -*- coding: utf-8 -*-
# Type Prefixes
#-----------------------------
VERBS_PREFIX = "http://adlnet.gov/expapi/verbs/"
ACTIVITIES_PREFIX = "http://adlnet.gov/expapi/activities/"

# Actors/Agents
#-----------------------------
AGENT_AGENT = "Agent"
GROUP_AGENT = "Group"

# Verbs
#-----------------------------
ANSWERED_VERB = "answered"
ASKED_VERB = "asked"
ATTEMPTED_VERB = "attempted"
ATTENDED_VERB = "attended"
COMMENTED_VERB = "commented"
COMPLETED_VERB = "completed"
EXITED_VERB = "exited"
EXPERIENCED_VERB = "experienced"
FAILED_VERB = "failed"
IMPORTED_VERB = "imported"
INITIALIZED_VERB = "initialized"
INTERACTED_VERB = "interacted"
LAUNCHED_VERB = "launched"
MASTERED_VERB = "mastered"
PASSED_VERB = "passed"
PREFERRED_VERB = "preferred"
PROGRESSED_VERB = "progressed"
REGISTERED_VERB = "registered"
RESPONDED_VERB = "responded"
RESUMED_VERB = "resumed"
SCORED_VERB = "scored"
SHARED_VERB = "shared"
SUSPENDED_VERB = "suspended"
TERMINATED_VERB = "terminated"
VOIDED_VERB = "voided"

VERB_SET = frozenset([ANSWERED_VERB, ASKED_VERB, ATTEMPTED_VERB,
                      ATTENDED_VERB, COMMENTED_VERB, COMPLETED_VERB,
                      EXITED_VERB, EXPERIENCED_VERB, FAILED_VERB,
                      IMPORTED_VERB, INITIALIZED_VERB, INTERACTED_VERB,
                      LAUNCHED_VERB, MASTERED_VERB, PASSED_VERB,
                      PREFERRED_VERB, PROGRESSED_VERB, REGISTERED_VERB,
                      RESPONDED_VERB, RESUMED_VERB, SCORED_VERB,
                      SHARED_VERB, SUSPENDED_VERB, TERMINATED_VERB,
                      VOIDED_VERB])

# Activities
#-----------------------------
ASSESSMENT_ACTIVITY = "assessment"
COURSE_ACTIVITY = "course"
FILE_ACTIVITY = "file"
INTERACTION_ACTIVITY = "interaction"
LESSON_ACTIVITY = "lesson"
LINK_ACTIVITY = "link"
MEDIA_ACTIVITY = "media"
MEETING_ACTIVITY = "meeting"
MODULE_ACTIVITY = "module"
OBJECTIVE_ACTIVITY = "objective"
PERFORMANCE_ACTIVITY = "performance"
QUESTION_ACTIVITY = "question"
SIMULATION_ACTIVITY = "simulation"

ACTIVITY_SET = frozenset([ASSESSMENT_ACTIVITY, COURSE_ACTIVITY,
                          FILE_ACTIVITY, INTERACTION_ACTIVITY,
                          LESSON_ACTIVITY, LINK_ACTIVITY, MEDIA_ACTIVITY,
                          MEETING_ACTIVITY, MODULE_ACTIVITY,
                          OBJECTIVE_ACTIVITY, PERFORMANCE_ACTIVITY,
                          QUESTION_ACTIVITY, SIMULATION_ACTIVITY])
