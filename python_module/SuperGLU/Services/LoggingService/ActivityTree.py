'''

Each node in the ActivityTree consists of an activity, label and list of child nodes.
In addition to the tree itself, we maintain the current path (i.e., the list of activities
from the root node to the last node entered into or removed from the tree).

'''
from SuperGLU.Util.Serialization import SuperGlu_Serializable, tokenizeObject, untokenizeObject
import json
from tincan.activity import Activity


class ActivityTree(SuperGlu_Serializable):
    '''This class represents the current state of the user's interaction
    with the software.  Users enter into activities and nodes are
    inserted into the activity tree. When users exit an activity the
    appropriate node is removed from the tree. New activities can be
    inserted directly into the activity tree at the root level, or as
    a child (i.e., subactivity) of an existing node. Currently, we
    make the assumption that each activity (name/string) in the tree
    is unique when we search for a particular node to delete, or add a
    child to. The label attribute is currently ignored during search
    and could be used to store a non-unique name for an activity.

    The default behavior implements an activity stack as stored in the
    current path. EnterActivity with no specified parentActivity is a
    PUSH to the current path, and adds a new node as a child of the
    last activity on the path. ExitActivity with no specified activity
    is a POP to the current path, and deletes this node from the
    activity tree. Applications creating siblings will have to track
    activity names to execute operations other than the PUSH/POP 
    described above.

    xAPI specifics: If you store activities as Activity objects
    created using the tincanapi library (instead of a simple type like
    a string for a name) you need to use saveXAPItoJSON and
    initializeFromXAPI_JSON/initializeFromXAPIfile for
    serialization/deserialization. 
    '''

    ACTIVITY_TREE_KEY = "activityTree"
    CURRENT_PATH_KEY = "currentPath"
    ACTIVITY_INDEX = 0
    LABEL_INDEX = 1
    CHILDREN_INDEX = 2

    def __init__(self):
        '''
        Constructor
        '''
        super(ActivityTree, self).__init__()
        self._activityTree = []
        self._currentPath = []        

    def findCurrentActivity(self):
        if len(self._currentPath) < 1:
            return None
        else:
            return self._currentPath[-1]

    def findParentActivity(self):
        if len(self._currentPath) < 2:
            return None
        else:
            return self._currentPath[-2]
        
    def findParentActivityByChild(self, childActivity, parentActivity=None, subtree=None):
        if len(self._activityTree) == 0:
            print("empty acctiviyt tree")
            return None
        if subtree == None:
            if len(self._activityTree) != 0:
                return self.findParentActivityByChild(childActivity, None, self._activityTree[0])
            else:
                return None
        else:
            if subtree[self.ACTIVITY_INDEX].id == childActivity.id:
                return parentActivity
            else:
                for currentChild in subtree[self.CHILDREN_INDEX]:
                    result = self.findParentActivityByChild(childActivity, subtree[self.ACTIVITY_INDEX], currentChild)
                    if result != None:
                        return result
                return None
        
    def findActivityByName(self, activityName, subtree=None):
        if len(self._activityTree) == 0:
            print("empty acctiviyt tree")
            return None
        if subtree == None:
            if len(self._activityTree) != 0:
                return self.findActivityByName(activityName, self._activityTree[0])
            else:
                return None
        else:
            if subtree[self.ACTIVITY_INDEX].id == activityName:
                return subtree[self.ACTIVITY_INDEX]
            else:
                for child in subtree[self.CHILDREN_INDEX]:
                    result = self.findActivityByName(activityName, child)
                    if result != None:
                        return result
                return None 

    def simpleActivityTree(self):
        return self.activityTreeToSimple(self._activityTree)

    def activityTreeToSimple(self,subtree):
        if subtree == []:
            return []
        else:
            simpleSubtree = []
            for node in subtree:
                simpleSubtree.append( ( node[self.ACTIVITY_INDEX].to_json(), node[self.LABEL_INDEX], self.activityTreeToSimple(node[self.CHILDREN_INDEX]) ) )
            return simpleSubtree
    
    def simpleTreeToActivityTree(self,subtree):
        if subtree == []:
            return []
        else:
            newSubtree = []
            for node in subtree:
                #                     activity
                newSubtree.append( ( Activity.from_json(node[self.ACTIVITY_INDEX]),\
                                     # label
                                     node[self.LABEL_INDEX],\
                                     # children
                                     self.simpleTreeToActivityTree(node[self.CHILDREN_INDEX]) ) )
            return newSubtree
    
    def simpleCurrentPath(self):
        newpath = []
        for activity in self._currentPath:
            newpath.append(activity.to_json())
        return newpath

    def saveXAPItoJSON(self):
        objectDictionary = {}
        objectDictionary[self.ACTIVITY_TREE_KEY] = self.simpleActivityTree()
        objectDictionary[self.CURRENT_PATH_KEY] = self.simpleCurrentPath()
        
        return json.dumps(objectDictionary)

    def initializeFromXAPIfile(self,filename):
        with open(filename, "r") as fileIN:
            raw_str = fileIN.read()
            fileIN.close()
            self.initializeFromXAPI_JSON(raw_str)

    def initializeFromXAPI_JSON(self, raw_str):
        objectDictionary = json.loads(raw_str)
        self._activityTree = self.simpleTreeToActivityTree(objectDictionary[self.ACTIVITY_TREE_KEY])
        self._currentPath = []
        for activity_str in objectDictionary[self.CURRENT_PATH_KEY]:
            self._currentPath.append(Activity.from_json(activity_str))

    def saveToToken(self):
        token = super(ActivityTree, self).saveToToken()
        if self._activityTree is not None:
            token[self.ACTIVITY_TREE_KEY] = tokenizeObject(self._activityTree)
        if self._currentPath is not None:
            token[self.CURRENT_PATH_KEY] = tokenizeObject(self._currentPath)
        
        return token
      
    def initializeFromToken(self, token, context=None):
        super(ActivityTree, self).initializeFromToken(token, context)
        self._activityTree = untokenizeObject(token.get(self.ACTIVITY_TREE_KEY, None))
        self._currentPath = untokenizeObject(token.get(self.CURRENT_PATH_KEY, None))

    def printState(self):
        print("Activity Tree:")
        print(self._activityTree)
        print("Current Path:")
        print(self._currentPath)

    def getActivityTree(self):
        return self._activityTree

    # reverse the path (go from specific to general)
    # omit current activity and its parent
    def convertPathToGrouping(self):
        grouping = []
        if len(self._currentPath)>2:
            # length - 1 = current activity
            # length - 2 = next to last activity (parent)
            for i in range(len(self._currentPath)-3,-1,-1):
                grouping.append(self._currentPath[i])
        return grouping

    def getCurrentPath(self):
        return self._currentPath
    
    # TODO: currently parentLabel is ignored
    def EnterActivity(self, label, activity, children=None, parentLabel=None, parentActivity=None):       
        if children is None: children = []
 
        entry = (activity, label, children)

        if len(self._activityTree) == 0:
            self._activityTree.append(entry)
            self._currentPath.append(entry[self.ACTIVITY_INDEX])
        else:
            if parentActivity == None:
                parentActivity = self.findCurrentActivity()
            if not(self.findAndInsertNode(entry,parentActivity,self._activityTree,[])):
                print("WARNING: activity not found:",parentActivity)
                print("Inserting into activity tree at root")
                self._activityTree.append(entry)
                self._currentPath = [entry[self.ACTIVITY_INDEX]]

    # TODO: currently parentLabel is ignored
    # NOTE: if parentActivity!=None then this is the same as EnterActivity
    def CreateSibling(self, label, activity, children=None, parentLabel=None, parentActivity=None):
        if children is None: children = []

        entry = (activity, label, children)

        if len(self._activityTree) == 0:
            self._activityTree.append(entry)
            self._currentPath.append(entry[self.ACTIVITY_INDEX])
        elif len(self._currentPath) == 1 and parentActivity==None:
            self._activityTree.append(entry)
            self._currentPath.pop()
            self._currentPath.append(entry[self.ACTIVITY_INDEX])
        else:
            if parentActivity == None:
                parentActivity = self.findParentActivity()
            if not(self.findAndInsertNode(entry,parentActivity,self._activityTree,[])):
                print("WARNING: activity not found:",parentActivity)
                print("Inserting into activity tree at root")
                self._activityTree.append(entry)
                self._currentPath = [ entry[self.ACTIVITY_INDEX] ]
    
    def ExitActivity(self,activity=None):
        if len(self._activityTree) == 0:
            print("WARNING: trying to exit from empty activity tree")
        else:
            if activity==None:
                activity = self.findCurrentActivity()
            if not(self.findAndDeleteNode(activity,None,self._activityTree,[])):
                print("WARNING: activity not found:",activity)
                print("Not deleted")

    # Find entry with activity==activity_target, and delete it
    # parent = parent of current_subtree (being searched)
    # path (to current_subtree)
    def findAndDeleteNode(self, activity_target, parent, current_subtree, path):
        for node in current_subtree:
            if node[self.ACTIVITY_INDEX] == activity_target:
                if parent:
                    parent[self.CHILDREN_INDEX].remove(node)
                    self._currentPath = path
                else:
                    current_subtree.remove(node)
                    if len(current_subtree)==0:
                        self._currentPath = []
                    else:
                        self._currentPath = [ current_subtree[0][self.ACTIVITY_INDEX] ]
                return True
            elif len(node[self.CHILDREN_INDEX]) > 0:
                newpath = list(path)
                newpath.append(node[self.ACTIVITY_INDEX])
                if self.findAndDeleteNode(activity_target,node,node[self.CHILDREN_INDEX],newpath):
                    return True
        return False           
        
    
    # Find entry with activity==activity_target,
    # and insert newEntry as a child.
    # path (to current_subtree)
    def findAndInsertNode(self, newEntry, activity_target, current_subtree, path):
        for node in current_subtree:
            if node[self.ACTIVITY_INDEX] == activity_target:
                node[self.CHILDREN_INDEX].append(newEntry)
                path.append(node[self.ACTIVITY_INDEX])
                path.append(newEntry[self.ACTIVITY_INDEX])
                self._currentPath = path
                return True
            elif len(node[self.CHILDREN_INDEX]) > 0:
                newpath = list(path)
                newpath.append(node[self.ACTIVITY_INDEX])
                if self.findAndInsertNode(newEntry,activity_target,node[self.CHILDREN_INDEX],newpath):
                    return True
        return False
                

