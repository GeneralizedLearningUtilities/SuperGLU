package edu.usc.ict.superglu.ontology.mappings;

import edu.usc.ict.superglu.ontology.converters.DataConverter;
import edu.usc.ict.superglu.util.Pair;
import edu.usc.ict.superglu.util.SerializationConvenience;
import edu.usc.ict.superglu.util.StorageToken;

import java.util.List;

/**
 * This class represents all the information to retrieve data from part of a field
 *
 * @author auerbach
 */
public class NestedSubAtomic extends NestedAtomic {

    public static String STORAGE_CONVERTER_KEY = "storageConverter";
    public static String RETRIEVAL_CONVERTER_KEY = "retrievalConverter";


    private DataConverter storageConverter;
    private DataConverter retrievalConverter;
    //private int index;


    public NestedSubAtomic(List<Pair<Class<?>, String>> indices, DataConverter storageConverter, DataConverter retrievalConverter) {
        super(indices);
        this.storageConverter = storageConverter;
        this.retrievalConverter = retrievalConverter;
    }

    public NestedSubAtomic() {
        super();
        this.storageConverter = null;
        this.retrievalConverter = null;
    }


    //Accessors
    public DataConverter getConverter() {
        return storageConverter;
    }

    public void setConverter(DataConverter converter) {
        this.storageConverter = converter;
    }

    public DataConverter getRetrievalConverter() {
        return retrievalConverter;
    }

    public void setRetrievalConverter(DataConverter retrievalConverter) {
        this.retrievalConverter = retrievalConverter;
    }


    //Equality operators
    @Override
    public boolean equals(Object otherObject) {
        if (!super.equals(otherObject))
            return false;

        if (!(otherObject instanceof NestedSubAtomic))
            return false;

        NestedSubAtomic other = (NestedSubAtomic) otherObject;

        if (!fieldIsEqual(this.storageConverter, other.storageConverter))
            return false;

        if (!fieldIsEqual(this.retrievalConverter, other.retrievalConverter))
            return false;

        return true;
    }

    @Override
    public int hashCode() {
        int result = super.hashCode();
        int arbitraryPrimeNumber = 23;

        if (this.storageConverter != null)
            result = result * arbitraryPrimeNumber + this.storageConverter.hashCode();

        if (this.retrievalConverter != null)
            result = result * arbitraryPrimeNumber + this.retrievalConverter.hashCode();

        return result;

    }


    // Serialization/Deserialization
    @Override
    public void initializeFromToken(StorageToken token) {
        super.initializeFromToken(token);

        this.storageConverter = (DataConverter) SerializationConvenience.untokenizeObject(token.getItem(STORAGE_CONVERTER_KEY));
        this.retrievalConverter = (DataConverter) SerializationConvenience.untokenizeObject(token.getItem(RETRIEVAL_CONVERTER_KEY));

    }

    @Override
    public StorageToken saveToToken() {
        StorageToken result = super.saveToToken();

        result.setItem(STORAGE_CONVERTER_KEY, SerializationConvenience.tokenizeObject(storageConverter));
        result.setItem(RETRIEVAL_CONVERTER_KEY, SerializationConvenience.tokenizeObject(retrievalConverter));
        return result;
    }


    //data storage and retrieval
    @Override
    public Object retrieveFieldData(StorageToken msg) {
        Object fieldData = super.retrieveFieldData(msg);
        Object result = retrievalConverter.convert(fieldData, msg);
        return result;
    }


    @Override
    public void storeData(StorageToken msg, Object data) {
        Object currentFieldData = super.retrieveFieldData(msg);

        if (currentFieldData == null)
            currentFieldData = "";

        Object newFieldData = storageConverter.convert(currentFieldData, data);

	/*
    List<Object> tokenizedObjectList;
	
	if(currentFieldData == null)
	    tokenizedObjectList = new ArrayList<>(index);
	else
	    tokenizedObjectList = storageConverter.split(currentFieldData);
	
	while(tokenizedObjectList.size() < index + 1)
	    tokenizedObjectList.add(null);
	
	tokenizedObjectList.set(index, data);
	
	Object newFieldData = storageConverter.join(tokenizedObjectList);
	*/
        super.storeData(msg, newFieldData);
    }


}
