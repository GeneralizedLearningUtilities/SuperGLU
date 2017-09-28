package edu.usc.ict.superglu.ontology.converters;

import edu.usc.ict.superglu.util.SuperGlu_Serializable;
import edu.usc.ict.superglu.util.SerializationConvenience;
import edu.usc.ict.superglu.util.StorageToken;

import java.util.List;

/**
 * This converter will add an element to a specified index in a list of strings
 *
 * @author auerbach
 */

public class AddElementToStringList extends SuperGlu_Serializable implements DataConverter {
    public static final String INDEX_KEY = "index";


    /**
     * the character/characters that divide the input string into a list
     */
    protected int index;


    public AddElementToStringList() {
        super();
        this.index = -1;
    }


    public AddElementToStringList(int index) {
        super();
        this.index = index;
    }


    //Getters/Setters
    public int getIndex() {
        return this.index;
    }

    public void setDelimiter(int index) {
        this.index = index;
    }


    // DataConverter Interface
    @Override
    public boolean isApplicable(Object input) {
        return input instanceof List;
    }

    /**
     * inputType: List<String>
     * context : String - Element to add to list.
     * outputType: String
     */
    @Override
    public Object convert(Object input, Object context) {
        List<String> inputAsList = (List) input;

        //make sure the list is large enough
        while (inputAsList.size() <= this.index) {
            inputAsList.add("");
        }

        inputAsList.set(this.index, (String) context);

        return inputAsList;
    }


    // Equality Operators
    @Override
    public boolean equals(Object otherObject) {
        if (!super.equals(otherObject))
            return false;

        if (!(otherObject instanceof AddElementToStringList))
            return false;

        AddElementToStringList other = (AddElementToStringList) otherObject;

        if (this.index != other.index)
            return false;


        return true;
    }

    @Override
    public int hashCode() {
        int result = super.hashCode();
        int arbitraryPrimeNumber = 23;

        result = result * arbitraryPrimeNumber + Integer.hashCode(index);

        return result;
    }


    // Serialization/Deserialization
    @Override
    public void initializeFromToken(StorageToken token) {
        super.initializeFromToken(token);

        this.index = (int) SerializationConvenience.untokenizeObject(token.getItem(INDEX_KEY));
    }

    @Override
    public StorageToken saveToToken() {
        StorageToken result = super.saveToToken();

        result.setItem(INDEX_KEY, SerializationConvenience.tokenizeObject(this.index));
        return result;
    }

}
