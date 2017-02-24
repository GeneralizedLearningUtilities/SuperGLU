package Ontology.Mappings;
/**
 * FieldMapOneToOne Class
 * This is the class that provides a valid mapping for a single field in the incoming message to a single
 * field in the outgoing message.
 * 
 * @author auerbach
 * @author tirthmehta
 */

import Util.Serializable;
import Util.SerializationConvenience;
import Util.StorageToken;

public class FieldMapOneToOne extends Serializable implements FieldMap
{
    public static final String FIELD_MAP_INFIELDS_KEY = "inFields";
    public static final String FIELD_MAP_OUTFIELDS_KEY = "outFields";

    protected FieldData inField;
    protected FieldData outField;
    
    // CONSTRUCTORS
    public FieldMapOneToOne()
    {
	super();
	inField = null;
	outField = null;
    }

    public FieldMapOneToOne(NestedAtomic in, NestedAtomic out)
    {
	super();
	inField = in;
	outField = out;
    }

    // GETTER AND SETTER METHODS FOR GETTING AND SETTING THE IN-FIELDS AND
    // OUT-FIELDS RESPECTIVELY

    public void setInField(NestedAtomic in)
    {
	inField = in;
    }

    public FieldData getInField()
    {
	return inField;
    }

    public FieldData getOutField()
    {
	return outField;
    }

    public void setOutField(NestedAtomic out)
    {
	outField = out;
    }

    // Equality Operations
    @Override
    public boolean equals(Object otherObject)
    {
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
    public int hashCode()
    {
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
    public void initializeFromToken(StorageToken token)
    {
	super.initializeFromToken(token);
	this.inField = (NestedAtomic) SerializationConvenience.untokenizeObject(token.getItem(FIELD_MAP_INFIELDS_KEY));
	this.outField = (NestedAtomic) SerializationConvenience.untokenizeObject(token.getItem(FIELD_MAP_OUTFIELDS_KEY));
    }

    @Override
    public StorageToken saveToToken()
    {
	StorageToken result = super.saveToToken();
	result.setItem(FIELD_MAP_INFIELDS_KEY, SerializationConvenience.tokenizeObject(this.inField));
	result.setItem(FIELD_MAP_OUTFIELDS_KEY, SerializationConvenience.tokenizeObject(this.outField));
	return result;
    }

    /**
     * apply the field mapping to an incoming StorageToken
     * 
     */
    public StorageToken applyMapping(StorageToken sourceMessage, StorageToken destinationMessage)
    {
	Object data = this.inField.retrieveFieldData(sourceMessage);
	this.outField.storeData(destinationMessage, data);
	return destinationMessage;
    }
}
