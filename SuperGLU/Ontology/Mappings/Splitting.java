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
    
    public List<String> split(String input)
    {
	List<String> ans=new ArrayList<>();
	String[] tobesent=input.split(argument);
	for(String in:tobesent)
	    ans.add(in);
	return ans;
    }

    @Override
    public String join(List<String> input)
    {
	String result = "";
	for(String currentInput : input)
	{
	    if(result.equals(""))
		result += currentInput;
	    else
		result = result + argument + currentInput;
	}
	
	return result;
    }
    
    
    
}

