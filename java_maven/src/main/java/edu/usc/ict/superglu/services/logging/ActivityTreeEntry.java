package edu.usc.ict.superglu.services.logging;

import java.util.ArrayList;
import java.util.List;

import gov.adlnet.xapi.model.Activity;

public class ActivityTreeEntry {
	
	private Activity activity;
	
	private String label;
	
	private List<ActivityTreeEntry> children;
	
	
	
	public ActivityTreeEntry(Activity activity, String label)
	{
		this.activity = activity;
		this.label = label;
		this.children = new ArrayList<>();
	}



	public Activity getActivity() {
		return activity;
	}



	public void setActivity(Activity activity) {
		this.activity = activity;
	}



	public String getLabel() {
		return label;
	}



	public void setLabel(String label) {
		this.label = label;
	}



	public List<ActivityTreeEntry> getChildren() {
		return children;
	}



	public void setChildren(List<ActivityTreeEntry> children) {
		this.children = children;
	}
	
	
	
}
