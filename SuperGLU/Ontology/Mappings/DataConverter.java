package Ontology.Mappings;

import java.util.List;

/**
 * This interface is responsible defining the conversion data from multiple fields into a single field.  The conversion
 * must be bi-directional 
 * @author auerbach
 *
 */
public interface DataConverter
{

    /**
     * this is the many to one mapping
     * @param inFields
     * @return
     */
    public Object join(List<Object> inFields);
    
    
    /**
     * this is the one to many mapping
     * @param inField
     * @return
     */
    public List<Object> split(Object inField);
    
}
