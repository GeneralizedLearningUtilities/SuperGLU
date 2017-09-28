package edu.usc.ict.superglu.ontology.converters;

import edu.usc.ict.superglu.util.SuperGlu_Serializable;
import edu.usc.ict.superglu.util.SerializationConvenience;
import edu.usc.ict.superglu.util.StorageToken;

import java.util.ArrayList;
import java.util.List;

/**
 * This converter will call multiple converters in series
 *
 * @author auerbach
 */

public class CompoundConverter extends SuperGlu_Serializable implements DataConverter {
    public static final String CONVERTER_LIST_KEY = "converterList";


    /**
     * the list of converters to apply
     */
    private List<DataConverter> converters;


    public CompoundConverter() {
        this.converters = new ArrayList<>();
    }


    public CompoundConverter(List<DataConverter> converters) {
        this.converters = converters;
    }


    public List<DataConverter> getConverters() {
        return this.converters;
    }


    public void setConverters(List<DataConverter> converters) {
        this.converters = converters;
    }


    // Equality Operators
    @Override
    public boolean equals(Object otherObject) {
        if (!super.equals(otherObject))
            return false;

        if (!(otherObject instanceof CompoundConverter))
            return false;

        CompoundConverter other = (CompoundConverter) otherObject;

        if (!fieldIsEqual(this.converters, other.converters))
            return false;


        return true;
    }

    @Override
    public int hashCode() {
        int result = super.hashCode();
        int arbitraryPrimeNumber = 23;

        if (this.converters != null)
            result = result * arbitraryPrimeNumber + this.converters.hashCode();

        return result;
    }


    @Override
    public boolean isApplicable(Object input) {
        if (this.converters.isEmpty())
            return false;

        return this.converters.get(0).isApplicable(input);
    }

    @Override
    public Object convert(Object input, Object context) {
        Object currentForm = input;

        for (DataConverter currentConverter : this.converters) {
            currentForm = currentConverter.convert(currentForm, context);
        }

        return currentForm;
    }


    // Serialization/Deserialization
    @Override
    public void initializeFromToken(StorageToken token) {
        super.initializeFromToken(token);

        this.converters = (List<DataConverter>) SerializationConvenience.untokenizeObject(token.getItem(CONVERTER_LIST_KEY));
    }

    @Override
    public StorageToken saveToToken() {
        StorageToken result = super.saveToToken();

        result.setItem(CONVERTER_LIST_KEY, SerializationConvenience.tokenizeObject(this.converters));
        return result;
    }
}
