package edu.usc.ict.superglu.services.logging;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.google.gson.Gson;

import edu.usc.ict.superglu.util.SuperGlu_Serializable;
import gov.adlnet.xapi.model.Activity;

public class ActivityTree extends SuperGlu_Serializable {

	public static String ACTIVITY_TREE_KEY = "activityTree";
    public static String CURRENT_PATH_KEY = "currentPath";
    
    
    private List<ActivityTreeEntry> activityTree;
    private List<Activity> currentPath;
    
    
    public ActivityTree()
    {
    	super();
    	
    	this.activityTree = new ArrayList<ActivityTreeEntry>();
    	this.currentPath = new ArrayList<>();
    }
    
    
    public Activity findCurrentActivity()
    {
    	if(this.currentPath.size() == 0)
    	{
    		return null;
    	}
    	else
    	{
    		return this.currentPath.get(this.currentPath.size() - 1);
    	}
    }
    
    
    public Activity findParentActivity()
    {
    	if(this.currentPath.size() < 2)
    	{
    		return null;
    	}
    	else
    	{
    		return this.currentPath.get(this.currentPath.size() - 2);
    	}
    }
    
    
    public String activityTreeToSimple()
    {
    	Gson jsonConverter = new Gson();
    	String activityTreeAsString = jsonConverter.toJson(this.activityTree);
    	String currentPathAsString = jsonConverter.toJson(this.currentPath);
    	
    	Map<String, String> result = new HashMap<>();
    	result.put(ACTIVITY_TREE_KEY, activityTreeAsString);
    	result.put(CURRENT_PATH_KEY, currentPathAsString);
    	
    	return jsonConverter.toJson(result);
    }
    
    
    public List<Activity> convertPathToGrouping()
    {
    	List<Activity> result = new ArrayList<>();
    	
    	for(int ii=this.currentPath.size() - 3; ii >= 0; --ii)
    	{
    		result.add(this.currentPath.get(ii));
    	}
    	
    	return result;
    }
    
    
    public void enterActivity(String label, Activity activity, Activity parentActivity)
    {
    	ActivityTreeEntry entry = new ActivityTreeEntry(activity, label);
    	
    	if(this.activityTree.size() == 0)
    	{
    		this.activityTree.add(entry);
    		this.currentPath.add(activity);
    	}
    	else
    	{
    		if(parentActivity == null)
    		{
    			parentActivity = this.findCurrentActivity();
    		}
    		if(!findAndInsertNode(entry.getActivity(), parentActivity, this.activityTree, new ArrayList<>()))
    		{
                System.out.println("WARNING: activity not found:" + parentActivity.toString());
                System.out.println("Inserting into activity tree at root");

                this.activityTree.add(entry);
                this.currentPath = new ArrayList<Activity>();
                this.currentPath.add(entry.getActivity());
    		}		
    	}
    }
    
    
    public void enterActivity(String label, Activity activity)
    {
    	this.enterActivity(label, activity, null);
    }
    
    
    public void exitActivity(Activity activity)
    {
        if(this.activityTree.size() == 0)
        {
            System.out.println("WARNING: trying to exit from empty activity tree");
        }
        else
        {
            if(activity == null)
            {
                activity = this.findCurrentActivity();
            }
            if (!findAndDeleteNode(activity, null, this.activityTree, new ArrayList<Activity>()))
            {
                System.out.println("WARNING: activity not found:" + activity.toString());
            }
        }
    }
    
    
    public void exitActivity()
    {
    	this.exitActivity(null);
    }
    
    
    public void createSibling(String label, Activity activity, List<ActivityTreeEntry> children, Activity parentActivity)
    {
        if (children == null)
            children = new ArrayList<ActivityTreeEntry>();

        ActivityTreeEntry entry = new ActivityTreeEntry(activity, label);
        entry.setChildren(children);

        if (this.activityTree.size() == 0)
        {
            this.activityTree.add(entry);
            this.currentPath.add(entry.getActivity());
        }
        else if (currentPath.size() == 1 && parentActivity == null)
        {
            this.activityTree.add(entry);
            this.currentPath.remove(this.currentPath.size() - 1);
            this.currentPath.add(entry.getActivity());
        }
        else
        {
            if (parentActivity == null)
            {
                parentActivity = this.findParentActivity();
            }
            if (!this.findAndInsertNode(entry.getActivity(), parentActivity, this.activityTree, new ArrayList<Activity>()))
            {
                System.out.println("WARNING: activity not found:" + parentActivity.toString());
                System.out.println("Inserting into activity tree at root");
                this.activityTree.add(entry);
                this.currentPath = new ArrayList<Activity>();
                this.currentPath.add(entry.getActivity());
            }
        }
    }
    
    
    
    public boolean findAndInsertNode(Activity newEntry, Activity activityTarget, List<ActivityTreeEntry> subTree, List<Activity> path)
    {
        for(ActivityTreeEntry entry : subTree)
        {
            if(entry.getActivity().equals(activityTarget))
            {
                entry.getChildren().add(new ActivityTreeEntry(newEntry, newEntry.getId()));
                path.add(entry.getActivity());
                path.add(newEntry);
                this.currentPath = path;
                return true;
            }
            else if (entry.getChildren().size() > 0)
            {
                List<Activity> newPath = new ArrayList<Activity>();
                for (Activity current : path)
                {
                    newPath.add(current);
                }

                newPath.add(entry.getActivity());
                return findAndInsertNode(newEntry, activityTarget, entry.getChildren(), newPath);
            }
        }

        return false;
    }
    
    
    public boolean findAndDeleteNode(Activity activityTarget, ActivityTreeEntry parent, List<ActivityTreeEntry> currentSubTree, List<Activity> path)
    {
        for (ActivityTreeEntry entry : currentSubTree)
        {
            if (entry.getActivity().equals(activityTarget))
            {
                if (parent != null)
                {
                    parent.getChildren().remove(entry);
                    this.currentPath = path;
                }
                else
                {
                    currentSubTree.remove(entry);
                    if (currentSubTree.size() == 0)
                    {
                        this.currentPath = new ArrayList<Activity>();
                    }
                    else
                    {
                        this.currentPath = new ArrayList<Activity>();
                        this.currentPath.add(currentSubTree.get(0).getActivity());
                    }
                }

                return true;
            }
            else if (entry.getChildren().size() > 0)
            {
                List<Activity> newPath = new ArrayList<Activity>();
                for (Activity current : path)
                {
                    newPath.add(current);
                }

                newPath.add(entry.getActivity());
                return this.findAndDeleteNode(activityTarget, entry, entry.getChildren(), newPath);
            }
        }

        return false;
    }
    
    
	
}
