package Ontology.Mappings;

import java.util.ArrayList;
import java.util.List;

public class Splitting implements ArgumentSeparator 
{
    public String argument;
    public Splitting(String arg)
    {
	argument=arg;
    }
    
    public List<String> action(String input)
    {
	List<String> ans=new ArrayList<>();
	String[] tobesent=input.split(argument);
	for(String in:tobesent)
	    ans.add(in);
	return ans;
    }
}

