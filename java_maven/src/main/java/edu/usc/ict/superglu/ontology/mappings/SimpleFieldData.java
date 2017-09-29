package edu.usc.ict.superglu.ontology.mappings;


import edu.usc.ict.superglu.util.SuperGlu_Serializable;
import edu.usc.ict.superglu.util.SerializationConvenience;
import edu.usc.ict.superglu.util.StorageToken;

/**
 * This is the FieldData class that stores the String type data for the default
 * values in the respective individuals
 *
 * @author auerbach
 */
public class SimpleFieldData extends SuperGlu_Serializable implements FieldData {

    public static final String FIELD_DATA_KEY = "fieldData";

    protected String fieldData;

    // PARAMETERIZED CONSTRUCTOR
    public SimpleFieldData(String data) {

        if (data == null)
            this.fieldData = "";
        else
            this.fieldData = data;
    }

    // DEFAULT CONSTRUCTOR
    public SimpleFieldData() {
        this.fieldData = "";
    }

    // RETURNS THE FIELD DATA
    public String getFieldData() {
        return fieldData;
    }

    // SETS THE FIELD DATA
    public void setFieldData(String data) {
        if (data != null)
            fieldData = data;
    }

    // Equality Operations
    @Override
    public boolean equals(Object otherObject) {
        if (!super.equals(otherObject))
            return false;

        if (!(otherObject instanceof SimpleFieldData))
            return false;

        SimpleFieldData other = (SimpleFieldData) otherObject;

        if (!fieldIsEqual(this.fieldData, other.fieldData))
            return false;

        return true;
    }

    @Override
    public int hashCode() {
        int result = super.hashCode();
        int arbitraryPrimeNumber = 23;

        if (this.fieldData != null)
            result = result * arbitraryPrimeNumber + this.fieldData.hashCode();

        return result;

    }

    // Serialization/Deserialization
    @Override
    public void initializeFromToken(StorageToken token) {
        super.initializeFromToken(token);
        this.fieldData = (String) SerializationConvenience.untokenizeObject(token.getItem(FIELD_DATA_KEY));
    }

    @Override
    public StorageToken saveToToken() {
        StorageToken result = super.saveToToken();
        result.setItem(FIELD_DATA_KEY, SerializationConvenience.tokenizeObject(this.fieldData));
        return result;
    }


    /**
     * This function will retrieve and nativize the field specified in this object from a passed in message in storageToken form
     *
     * @param msg
     * @return data object if it exists, null otherwise
     */
    public Object retrieveFieldData(StorageToken msg) {
        Object data = msg.getItem(this.fieldData);

        Object result;
        if (data != null)
            result = SerializationConvenience.untokenizeObject(data);
        else
            result = null;

        return result;
    }


    /**
     * This function will set the data in the field specified by this object.
     *
     * @param msg  the storage token into which the data is placed.
     * @param data
     */
    public void storeData(StorageToken msg, Object data) {
        Object dataAsStorageToken = SerializationConvenience.tokenizeObject(data);

        msg.setItem(fieldData, dataAsStorageToken);
    }

}
