package Ontology.Mappings;

import java.util.List;

public interface ArgumentSeparator
{
    public List<String> split(String input);
    
    
    public String join(List<String> input);
}
