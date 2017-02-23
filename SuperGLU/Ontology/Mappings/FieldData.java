package Ontology.Mappings;

import Util.StorageToken;

/**
 * This interface represents an object capable of storing and retrieving object data from a StorageToken
 * @author auerbach
 *
 */
public interface FieldData
{

    /**
     * This function will retrieve and nativize the field specified in this object from a passed in message in storageToken form
     * @param msg
     * @return data object if it exists, null otherwise
     */
    public Object retrieveFieldData(StorageToken msg);
    
    
    /**
     * This function will set the data in the field specified by this object.
     * @param msg the storage token into which the data is placed.
     * @param data 
     */
    public void storeData(StorageToken msg, Object data);
}
