package edu.usc.ict.superglu.ontology.mappings;

import edu.usc.ict.superglu.util.StorageToken;

import java.util.Map;

/**
 * This interface defines the functionality of a mapping of fields within a message
 *
 * @author auerbach
 */
public interface FieldMap {

    /**
     * apply the field mapping to an incoming StorageToken
     *
     * @param sourceMessage      the message to be transformed
     * @param destinationMessage the partially transformed destination message
     * @return the modified destination message
     */
    public StorageToken applyMapping(StorageToken sourceMessage, StorageToken destinationMessage, Map<String, Object> context);


    /**
     * determine if mapping can apply to the current sourceMessage
     */
    public boolean doesMappingApply(StorageToken sourceMessage, Map<String, Object> context);
}
