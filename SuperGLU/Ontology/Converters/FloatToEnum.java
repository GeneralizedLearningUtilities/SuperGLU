package Ontology.Converters;

import java.util.ArrayList;
import java.util.List;

import Util.Serializable;
import Util.SerializationConvenience;
import Util.StorageToken;

/**
 * This converter will convert a floating point value to an enum
 * @author auerbach
 *
 */

public class FloatToEnum extends Serializable implements DataConverter {

	public static final String ENUM_VALUES_KEY = "enumValues";
	public static final String MIN_FLOAT_VALUE_KEY = "minFloatValue";
	public static final String MAX_FLOAT_VALUE_KEY = "maxFloatValue";
	
	
	private List<String> enumValues;
	
	private float minFloatValue;
	private float maxFloatValue;
	
	
	public FloatToEnum() {
		super();
		this.enumValues = new ArrayList<>();
		this.minFloatValue = 0.0f;
		this.maxFloatValue = 100.0f;
	}
	
	
	public FloatToEnum(List<String> enumValues, float minFloatValue, float maxFloatValue)
	{
		super();
		this.enumValues = enumValues;
		this.maxFloatValue = maxFloatValue;
		this.minFloatValue = minFloatValue;
	}
	
	
	
	
	
	@Override
	public boolean equals(Object otherObject) {
		if (!super.equals(otherObject))
		    return false;
		
		if (!(otherObject instanceof FloatToEnum))
		    return false;
		
		FloatToEnum other = (FloatToEnum) otherObject;
		
		if(!fieldIsEqual(this.enumValues, other.enumValues))
			return false;
		
		if(!fieldIsEqual(this.minFloatValue, other.minFloatValue))
			return false;
		
		if(!fieldIsEqual(this.maxFloatValue, other.maxFloatValue))
			return false;
		
		return true;
	}


	@Override
	public int hashCode() {
		int result = super.hashCode();
		int arbitraryPrimeNumber = 23;
		if (this.enumValues != null)
			result = result * arbitraryPrimeNumber + enumValues.hashCode();
		result = result * arbitraryPrimeNumber + Float.hashCode(minFloatValue);
		result = result * arbitraryPrimeNumber + Float.hashCode(maxFloatValue);
		return result;
	}


	@Override
	public void initializeFromToken(StorageToken token) {
		super.initializeFromToken(token);
		
		this.enumValues = (List<String>) SerializationConvenience.untokenizeObject(token.getItem(ENUM_VALUES_KEY, true, new ArrayList<String>()));
		this.maxFloatValue = (float) SerializationConvenience.untokenizeObject(token.getItem(MAX_FLOAT_VALUE_KEY, true, 100.0f));
		this.minFloatValue = (float) SerializationConvenience.untokenizeObject(token.getItem(MIN_FLOAT_VALUE_KEY, true, 0.0f));
		
	}


	@Override
	public StorageToken saveToToken() {
		StorageToken result = super.saveToToken();
		
		result.setItem(ENUM_VALUES_KEY, SerializationConvenience.tokenizeObject(this.enumValues));
		result.setItem(MIN_FLOAT_VALUE_KEY, SerializationConvenience.tokenizeObject(this.minFloatValue));
		result.setItem(MAX_FLOAT_VALUE_KEY, SerializationConvenience.tokenizeObject(this.maxFloatValue));
		
		return result;
		
	}


	@Override
	public boolean isApplicable(Object input) {
		return input != null && input instanceof Float && this.enumValues.size() > 0;
	}

	@Override
	public Object convert(Object input, Object context) {
		
		float in = (float) input;
		
		float adjustedInput;
		
		//This gives us a 0 - n scale.
		if(this.minFloatValue <= 0)
			adjustedInput = in + this.minFloatValue; 
		else
			adjustedInput = in - this.minFloatValue;
		
		int interval = (int) ((this.maxFloatValue - this.minFloatValue) / this.enumValues.size());
	
		String result;
		
		if(in > interval * this.enumValues.size() + this.minFloatValue)
			result = this.enumValues.get(this.enumValues.size() - 1);
		else if(in < this.minFloatValue)
			result = this.enumValues.get(0);
		else
		{
			int index = (int) (adjustedInput / interval);
			result = this.enumValues.get(index);
		}
		
		return result;
	}


}
