using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using TinCan;
using Newtonsoft.Json;

namespace SuperGLU
{
    public class ActivityTreeEntry
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


    public class ActivityTree : SuperGLU_Serializable
    {
        private static String ACTIVITY_TREE_KEY = "activityTree";
        private static String CURRENT_PATH_KEY = "currentPath";

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


        public String activityTreeToSimple()
        {

            String activityTreeAsString = JsonConvert.SerializeObject(this.activityTree);
            String currentPathAsString = JsonConvert.SerializeObject(this.currentPath);

            Dictionary<String, String> result = new Dictionary<string, string>();
            result.Add(ACTIVITY_TREE_KEY, activityTreeAsString);
            result.Add(CURRENT_PATH_KEY, currentPathAsString);

            return JsonConvert.SerializeObject(result);
        }


        public List<Activity> convertPathToGrouping()
        {
            List<Activity> result = new List<Activity>();
            for(int ii = this.currentPath.Count - 3; ii >= 0; --ii)
            {
                result.Add(this.currentPath[ii]);
            }

            return result;

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
                if(parentActivity == null)
                {
                    parentActivity = this.findCurrentActivity();
                }
                if (!findAndInsertNode(entry.activity, parentActivity, this.activityTree, new List<Activity>()))
                {
                    Console.Out.WriteLine("WARNING: activity not found:" + parentActivity.ToString());
                    Console.Out.WriteLine("Inserting into activity tree at root");

                    this.activityTree.Add(entry);
                    this.currentPath = new List<Activity>();
                    this.currentPath.Add(entry.activity);
                }

            }
        }



        public void exitActivity(Activity activity)
        {
            if(this.activityTree.Count == 0)
            {
                Console.Out.WriteLine("WARNING: trying to exit from empty activity tree");
            }
            else
            {
                if(activity == null)
                {
                    activity = this.findCurrentActivity();
                }
                if (!findAndDeleteNode(activity, null, this.activityTree, new List<Activity>()))
                {
                    Console.Out.WriteLine("WARNING: activity not found:" + activity.ToString());
                }
            }
        }


        public void createSibling(String label, Activity activity, List<ActivityTreeEntry> children, Activity parentActivity)
        {
            if (children == null)
                children = new List<ActivityTreeEntry>();

            ActivityTreeEntry entry = new ActivityTreeEntry(activity, label);
            entry.children = children;

            if (this.activityTree.Count == 0)
            {
                this.activityTree.Add(entry);
                this.currentPath.Add(entry.activity);
            }
            else if (currentPath.Count == 1 && parentActivity == null)
            {
                this.activityTree.Add(entry);
                this.currentPath.RemoveAt(this.currentPath.Count - 1);
                this.currentPath.Add(entry.activity);
            }
            else
            {
                if (parentActivity == null)
                {
                    parentActivity = this.findParentActivity();
                }
                if (!this.findAndInsertNode(entry.activity, parentActivity, this.activityTree, new List<Activity>()))
                {
                    Console.Out.WriteLine("WARNING: activity not found:" + parentActivity.ToString());
                    Console.Out.WriteLine("Inserting into activity tree at root");
                    this.activityTree.Add(entry);
                    this.currentPath = new List<Activity>();
                    this.currentPath.Add(entry.activity);
                }
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
