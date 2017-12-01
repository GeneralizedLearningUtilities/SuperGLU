/**
 *
 */
package edu.usc.ict.superglu.ontology.converters;

import edu.usc.ict.superglu.util.SuperGlu_Serializable;
import edu.usc.ict.superglu.util.SerializationConvenience;
import edu.usc.ict.superglu.util.StorageToken;

import java.util.ArrayList;
import java.util.List;

/**
 * This class takes a string field and splits it into a list delimited by the delimiter passed in
 * through the constructor.  Default delimiter is space.
 *
 * @author auerbach
 */
public class StringToList extends SuperGlu_Serializable implements DataConverter {

    public static final String DELIMITER_KEY = "delimiter";


    /**
     * the character/characters that divide the input string into a list
     */
    protected String delimiter;


    public StringToList() {
        super();
        this.delimiter = " ";
    }


    public StringToList(String delimiter) {
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
        return input instanceof String;
    }

    /**
     * inputType: String
     * outputType: List<String>
     */
    @Override
    public Object convert(Object input, Object context) {
        String inputAsString = (String) input;

        String[] tokenizedString = inputAsString.split(this.delimiter, 4);

        List<String> result = new ArrayList<>();

        for (String currString : tokenizedString)
            result.add(currString);

        return result;
    }


    // Equality Operators
    @Override
    public boolean equals(Object otherObject) {
        if (!super.equals(otherObject))
            return false;

        if (!(otherObject instanceof StringToList))
            return false;

        StringToList other = (StringToList) otherObject;

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
