package edu.usc.ict.superglu.ontology.converters;

import edu.usc.ict.superglu.util.SuperGlu_Serializable;
import edu.usc.ict.superglu.util.SerializationConvenience;
import edu.usc.ict.superglu.util.StorageToken;

import java.util.List;

/**
 * This data converter will take a List<String> and convert it into a delimited string.
 * The delimiter can be specified in the constructor
 *
 * @author auerbach
 */
public class ListToString extends SuperGlu_Serializable implements DataConverter {
    public static final String DELIMITER_KEY = "delimiter";


    /**
     * the character/characters that goes between each element of the List
     */
    protected String delimiter;


    public ListToString() {
        super();
        this.delimiter = " ";
    }


    public ListToString(String delimiter) {
        super();
        this.delimiter = delimiter;
    }


    //Getters/Setters
    public String getDelimiter() {
        return delimiter;
    }

    public void setDelimiter(String delimiter) {
        this.delimiter = delimiter;
    }


    // DataConverter Interface
    @Override
    public boolean isApplicable(Object input) {
        return input instanceof List;
    }

    /**
     * inputType: List<String>
     * outputType: String
     */
    @Override
    public Object convert(Object input, Object context) {
        List<String> inputAsList = (List<String>) input;

        String result = "";

        for (int ii = 0; ii < inputAsList.size(); ++ii) {
            String currentElement = inputAsList.get(ii);
            result += currentElement;

            if (ii != inputAsList.size() - 1)
                result += this.delimiter;
        }

        return result;
    }


    // Equality Operators
    @Override
    public boolean equals(Object otherObject) {
        if (!super.equals(otherObject))
            return false;

        if (!(otherObject instanceof ListToString))
            return false;

        ListToString other = (ListToString) otherObject;

        if (!fieldIsEqual(this.delimiter, other.delimiter))
            return false;


        return true;
    }

    @Override
    public int hashCode() {
        int result = super.hashCode();
        int arbitraryPrimeNumber = 23;

        if (this.delimiter != null)
            result = result * arbitraryPrimeNumber + this.delimiter.hashCode();

        return result;
    }


    // Serialization/Deserialization
    @Override
    public void initializeFromToken(StorageToken token) {
        super.initializeFromToken(token);

        this.delimiter = (String) SerializationConvenience.untokenizeObject(token.getItem(DELIMITER_KEY));
    }

    @Override
    public StorageToken saveToToken() {
        StorageToken result = super.saveToToken();

        result.setItem(DELIMITER_KEY, SerializationConvenience.tokenizeObject(this.delimiter));
        return result;
    }

}
