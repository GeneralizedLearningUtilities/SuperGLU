/** Convenience functions for generating common logging messages for an
 intelligent tutoring system or adaptive learning system

 Package: SuperGLU (Generalized Learning Utilities)
 Author: Benjamin Nye
 License: APL 2.0

 Requires:
 - Util\uuid.js
 - Util\zet.js
 - Util\serializable.js
 - Core\messaging.js
 - Core\messaging-gateway.js

 Some notes about the use of context parameters:
 1. stepId: This should represent some decision point or state where you would want to compare the behavior that occurred with different users. It should be a string, but this string can be structured (e.g., a JSON object) rather than an arbitrary UUID (though a uuid is also valid). Since these are only meant to be compared within a single task, there is a great deal of variability possible.
 2. relevance: This is typically optional (defaults to 1), and represents the degree to which some knowledge or skill was assessed by a given activity. This paramter should be provided when a skill was not partially measured (relevance=0) or if confidence was uncertain (relevance above 0 but less than 1).
 **/

const Zet = require('../../util/zet'),
    Serialization = require('../../util/serialization'),
    tokenizeObject = Serialization.tokenizeObject,
    untokenizeObject = Serialization.untokenizeObject

var TASK_ID_KEY = "taskId",
    SYSTEM_KEY = "system",
    ALIAS_IDS_KEY = "aliasIds",
    NAME_KEY = "name",
    DISPLAY_NAME_KEY = "displayName",
    KCS_KEY = "kcs",
    BASE_URL_KEY = "baseURL",
    ASSISTMENTS_ITEM_KEY = "assistmentsItem",
    DESCRIPTION_KEY = "description",
    CAN_BE_RECOMMENDED_INDIVIDUALLY_KEY = "canBeRecommendedIndividually",
    SUBTASKS_KEY = "subtasks"

/** Learning Task Data, for linking to a task **/
var LearningTask = Zet.declare({
    superclass: Serialization.Serializable,
    CLASS_ID: 'LearningTask',
    defineBody: function (self) {
        // Public Properties
        self.construct = function construct(taskId, aliasIds, name, displayName, description,
                                            system, subtasks, kcs, baseURL, assistmentsItem,
                                            canRecommendIndividually, anId) {
            self.inherited(construct, [anId])
            if (taskId == null) {
                taskId = null
            }
            if (aliasIds == null) {
                aliasIds = null
            }
            if (name == null) {
                name = null
            }
            if (displayName == null) {
                displayName = null
            }
            if (description == null) {
                description = null
            }
            if (system == null) {
                system = null
            }
            if (subtasks == null) {
                subtasks = []
            }
            if (kcs == null) {
                kcs = []
            }
            if (baseURL == null) {
                baseURL = null
            }
            if (assistmentsItem == null) {
                assistmentsItem = null
            }
            if (canRecommendIndividually == null) {
                canRecommendIndividually = true
            }
            self._taskId = taskId
            self._system = system
            self._subtasks = subtasks
            self._aliasIds = aliasIds
            self._name = name
            self._displayName = displayName
            self._description = description
            self._kcs = kcs
            self._baseURL = baseURL
            self._assistmentsItem = assistmentsItem
            self._canBeRecommendedIndividually = canRecommendIndividually
        }

        self.saveToToken = function saveToToken() {
            var token = self.inherited(saveToToken, [])
            token.setitem(TASK_ID_KEY, tokenizeObject(self._taskId))
            token.setitem(SYSTEM_KEY, tokenizeObject(self._system))
            token.setitem(ALIAS_IDS_KEY, tokenizeObject(self._subtasks))
            token.setitem(SUBTASKS_KEY, tokenizeObject(self._taskId))
            token.setitem(NAME_KEY, tokenizeObject(self._name))
            token.setitem(DISPLAY_NAME_KEY, tokenizeObject(self._displayName))
            token.setitem(KCS_KEY, tokenizeObject(self._kcs))
            token.setitem(BASE_URL_KEY, tokenizeObject(self._baseURL))
            token.setitem(ASSISTMENTS_ITEM_KEY, tokenizeObject(self._assistmentsItem))
            token.setitem(DESCRIPTION_KEY, tokenizeObject(self._description))
            token.setitem(CAN_BE_RECOMMENDED_INDIVIDUALLY_KEY, tokenizeObject(self._canBeRecommendedIndividually))
            return token
        }

        self.initializeFromToken = function initializeFromToken(token, context) {
            self.inherited(initializeFromToken, [token, context])
            self._taskId = untokenizeObject(token.getitem(TASK_ID_KEY, true, null), context)
            self._system = untokenizeObject(token.getitem(SYSTEM_KEY, true, null), context)
            self._subtasks = untokenizeObject(token.getitem(SUBTASKS_KEY, true, []), context)
            self._aliasIds = untokenizeObject(token.getitem(ALIAS_IDS_KEY, true, []), context)
            self._name = untokenizeObject(token.getitem(NAME_KEY, true, null), context)
            self._displayName = untokenizeObject(token.getitem(DISPLAY_NAME_KEY, true, null), context)
            self._description = untokenizeObject(token.getitem(DESCRIPTION_KEY, true, null), context)
            self._kcs = untokenizeObject(token.getitem(KCS_KEY, true, []), context)
            self._baseURL = untokenizeObject(token.getitem(BASE_URL_KEY, true, null), context)
            self._assistmentsItem = untokenizeObject(token.getitem(ASSISTMENTS_ITEM_KEY, true, null), context)
            self._canBeRecommendedIndividually = untokenizeObject(token.getitem(CAN_BE_RECOMMENDED_INDIVIDUALLY_KEY, true, null), context)
        }
    }
})

module.exports = LearningTask