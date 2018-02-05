/** ASSISTments Learning Task Linkages **/
const Zet = require('../../util/zet'),
    Serialization = require('../../util/serialization'),
    tokenizeObject = Serialization.tokenizeObject,
    untokenizeObject = Serialization.untokenizeObject

const // ASSISTments Storage Keys
    ASSISTMENTS_ITEM_ID_KEY = "itemId",
    PROBLEM_SET_ID_KEY = "problemSetId",
    PROBLEM_SET_NAME_KEY = "problemSetName",
    ASSIGNMENTS_KEY = "assignments",
    ASSIGNMENT_NUMBER_KEY = "assignmentNumber"

var SerializableAssistmentsItem = Zet.declare({
    superclass: Serialization.Serializable,
    CLASS_ID: 'SerializableAssistmentsItem',
    defineBody: function (self) {
        // Public Properties
        self.construct = function construct(itemId, problemSetId, problemSetName, assignments,
                                            assignmentNumber, anId) {
            self.inherited(construct, [anId])
            if (itemId == null) {
                itemId = null
            }
            if (problemSetId == null) {
                problemSetId = null
            }
            if (problemSetName == null) {
                problemSetName = null
            }
            if (assignments == null) {
                assignments = []
            }
            if (assignmentNumber == null) {
                assignmentNumber = null
            }
            self._itemId = itemId
            self._problemSetId = problemSetId
            self._problemSetName = problemSetName
            self._assignments = assignments
            self._assignmentNumber = assignmentNumber
        }

        self.getActiveAssignmentURL = function getActiveAssignmentURL() {
            if (self._assignmentNumber < self._assignments.length) {
                return self._assignments[self._assignmentNumber]
            }
            return null
        }

        self.saveToToken = function saveToToken() {
            var token = self.inherited(saveToToken, [])
            token.setitem(ASSIGNMENT_NUMBER_KEY, tokenizeObject(self._assignmentNumber))
            token.setitem(ASSISTMENTS_ITEM_ID_KEY, tokenizeObject(self._itemId))
            token.setitem(PROBLEM_SET_ID_KEY, tokenizeObject(self._problemSetId))
            token.setitem(PROBLEM_SET_NAME_KEY, tokenizeObject(self._problemSetName))
            token.setitem(ASSIGNMENTS_KEY, tokenizeObject(self._assignments))
            return token
        }

        self.initializeFromToken = function initializeFromToken(token, context) {
            self.inherited(initializeFromToken, [token, context])
            self._assignmentNumber = untokenizeObject(token.getitem(ASSIGNMENT_NUMBER_KEY, true, null), context)
            self._itemId = untokenizeObject(token.getitem(ASSISTMENTS_ITEM_ID_KEY, true, null), context)
            self._problemSetId = untokenizeObject(token.getitem(PROBLEM_SET_ID_KEY, true, null), context)
            self._problemSetName = untokenizeObject(token.getitem(PROBLEM_SET_NAME_KEY, true, null), context)
            self._assignments = untokenizeObject(token.getitem(ASSIGNMENTS_KEY, true, []), context)
        }
    }
})
module.exports = SerializableAssistmentsItem