package edu.usc.ict.superglu.ontology.converters;

/**
 * This interface is responsible defining the conversion data from multiple fields into a single field.  The conversion
 * is not bi-directional.
 * @author auerbach
 *
 */
public interface DataConverter
{

    /**
     * Check if the object can be converted
     * @param input object to be converted
     * @return true if the input can be converted by this converter
     */
    public boolean isApplicable(Object input);
    
    
    /**
     * Convert the object
     * @param input
     * @param context additional information that some converters may need (e.g. inserting text into a list)
     * @return the converted object
     */
    public Object convert(Object input, Object context);
}
