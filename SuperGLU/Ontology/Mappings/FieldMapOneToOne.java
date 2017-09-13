package Ontology.Mappings;
/**
 * FieldMapOneToOne Class
 * This is the class that provides a valid mapping for a single field in the incoming message to a single
 * field in the outgoing message.
 * 
 * @author auerbach
 * @author tirthmehta
 */

import java.util.Map;

import Util.Serializable;
import Util.SerializationConvenience;
import Util.StorageToken;

public class FieldMapOneToOne extends Serializable implements FieldMap {
	public static final String FIELD_MAP_INFIELD_KEY = "inField";
	public static final String FIELD_MAP_OUTFIELD_KEY = "outField";

	private static final String VARIABLE_IDENTIFIER = "~";

	protected FieldData inField;
	protected FieldData outField;

	// CONSTRUCTORS
	public FieldMapOneToOne() {
		super();
		inField = null;
		outField = null;
	}

	public FieldMapOneToOne(FieldData in, FieldData out) {
		super();
		inField = in;
		outField = out;
	}

	// GETTER AND SETTER METHODS FOR GETTING AND SETTING THE IN-FIELDS AND
	// OUT-FIELDS RESPECTIVELY

	public void setInField(FieldData in) {
		inField = in;
	}

	public FieldData getInField() {
		return inField;
	}

	public FieldData getOutField() {
		return outField;
	}

	public void setOutField(FieldData out) {
		outField = out;
	}

	// Equality Operations
	@Override
	public boolean equals(Object otherObject) {
		if (!super.equals(otherObject))
			return false;

		if (!(otherObject instanceof FieldMapOneToOne))
			return false;

		FieldMapOneToOne other = (FieldMapOneToOne) otherObject;

		if (!fieldIsEqual(this.inField, other.inField))
			return false;

		if (!fieldIsEqual(this.outField, other.outField))
			return false;

		return true;
	}

	@Override
	public int hashCode() {
		int result = super.hashCode();
		int arbitraryPrimeNumber = 23;

		if (this.inField != null)
			result = result * arbitraryPrimeNumber + this.inField.hashCode();
		if (this.outField != null)
			result = result * arbitraryPrimeNumber + this.outField.hashCode();
		return result;

	}

	// Serialization/Deserialization
	@Override
	public void initializeFromToken(StorageToken token) {
		super.initializeFromToken(token);
		this.inField = (NestedAtomic) SerializationConvenience.untokenizeObject(token.getItem(FIELD_MAP_INFIELD_KEY));
		this.outField = (NestedAtomic) SerializationConvenience.untokenizeObject(token.getItem(FIELD_MAP_OUTFIELD_KEY));
	}

	@Override
	public StorageToken saveToToken() {
		StorageToken result = super.saveToToken();
		result.setItem(FIELD_MAP_INFIELD_KEY, SerializationConvenience.tokenizeObject(this.inField));
		result.setItem(FIELD_MAP_OUTFIELD_KEY, SerializationConvenience.tokenizeObject(this.outField));
		return result;
	}

	/**
	 * apply the field mapping to an incoming StorageToken
	 * 
	 */
	public StorageToken applyMapping(StorageToken sourceMessage, StorageToken destinationMessage,
			Map<String, Object> context) {
		Object data = this.inField.retrieveFieldData(sourceMessage);
		Object contextData = getContextData(data, context);
		this.outField.storeData(destinationMessage, contextData);
		return destinationMessage;
	}

	/**
	 * Grab information from the context as needed
	 */
	public Object getContextData(Object data, Map<String, Object> context) {
		Object result = data;

		if (data instanceof String) {
			String key = (String) data;
			if (context.containsKey(key))
				result = context.get(key);
		}

		return result;
	}

	@Override
	public boolean doesMappingApply(StorageToken sourceMessage, Map<String, Object> context) {
		Object data = this.inField.retrieveFieldData(sourceMessage);

		return data != null;
	}

}
