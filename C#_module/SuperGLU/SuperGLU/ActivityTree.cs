using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using TinCan;

namespace SuperGLU
{
    class ActivityTreeEntry
    {
        public Activity  activity
        { get; set; }

        public String label
        { get; set; }

        public List<ActivityTreeEntry> children
        { get; set; }


        public ActivityTreeEntry(Activity activity, String label)
        {
            this.activity = activity;
            this.label = label;
            this.children = new List<ActivityTreeEntry>();
        }
    }


    class ActivityTree : SuperGLU_Serializable
    {
        private static String ACTIVITY_TREE_KEY = "activityTree";
        private static String CURRENT_PATH_KEY = "currentPath";

        private static int ACTIVITY_INDEX = 0;
        private static int LABEL_INDEX = 1;
        private static int CHILDREN_INDEX = 2;

        private List<ActivityTreeEntry> activityTree;
        private List<Activity> currentPath;


        public ActivityTree() : base()
        {
            activityTree = new List<ActivityTreeEntry>();
            currentPath = new List<Activity>();
        }


        public Activity findCurrentActivity()
        {
            if (this.currentPath.Count == 0)
                return null;
            else
                return this.currentPath[this.currentPath.Count - 1];
        }


        public Activity findParentActivity()
        {
            if (this.currentPath.Count < 2)
                return null;
            else
                return this.currentPath[this.currentPath.Count - 2];
        }


        public String activityTreeToActivityString(List<ActivityTreeEntry> subtree, String emptyString)
        {
            return null;
        }


        public void enterActivity(String label, Activity activity, Activity parentActivity)
        {
            ActivityTreeEntry entry = new ActivityTreeEntry(activity, label);

            if(this.activityTree.Count == 0)
            {
                this.activityTree.Add(entry);
                this.currentPath.Add(activity);
            }
            else
            {

            }
        }


        public bool findAndInsertNode(Activity newEntry, Activity activityTarget, List<ActivityTreeEntry> subTree, List<Activity> path)
        {
            foreach(ActivityTreeEntry entry in subTree)
            {
                if(entry.activity.Equals(activityTarget))
                {
                    entry.children.Add(new ActivityTreeEntry(newEntry, newEntry.id));
                    path.Add(entry.activity);
                    path.Add(newEntry);
                    this.currentPath = path;
                    return true;
                }
                else if (entry.children.Count > 0)
                {
                    List<Activity> newPath = new List<Activity>();
                    foreach (Activity current in path)
                    {
                        newPath.Add(current);
                    }

                    newPath.Add(entry.activity);
                    return findAndInsertNode(newEntry, activityTarget, entry.children, newPath);
                }
            }

            return false;
        }


        public bool findAndDeleteNode(Activity activityTarget, ActivityTreeEntry parent, List<ActivityTreeEntry> currentSubTree, List<Activity> path)
        {
            foreach (ActivityTreeEntry entry in currentSubTree)
            {
                if (entry.activity.Equals(activityTarget))
                {
                    if (parent != null)
                    {
                        parent.children.Remove(entry);
                        this.currentPath = path;
                    }
                    else
                    {
                        currentSubTree.Remove(entry);
                        if (currentSubTree.Count == 0)
                        {
                            this.currentPath = new List<Activity>();
                        }
                        else
                        {
                            this.currentPath = new List<Activity>();
                            this.currentPath.Add(currentSubTree[0].activity);
                        }
                    }

                    return true;
                }
                else if (entry.children.Count > 0)
                {
                    List<Activity> newPath = new List<Activity>();
                    foreach (Activity current in path)
                    {
                        newPath.Add(current);
                    }

                    newPath.Add(entry.activity);
                    return this.findAndDeleteNode(activityTarget, entry, entry.children, newPath);
                }
            }

            return false;
        }
    }


}
