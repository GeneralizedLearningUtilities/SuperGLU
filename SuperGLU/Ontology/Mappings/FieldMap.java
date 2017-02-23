package Ontology.Mappings;
/**
 * FieldMap Class
 * This is the class that provides a valid mapping to have their respective in-fields and out-fields which
 * are involved in the mapping
 * @author tirthmehta
 */

import Util.Serializable;
import Util.SerializationConvenience;
import Util.StorageToken;

public class FieldMap extends Serializable
{

    public static final String FIELD_MAP_INFIELDS_KEY = "inFields";
    public static final String FIELD_MAP_OUTFIELDS_KEY = "outFields";
    public static final String FIELD_MAP_SPLITTING_KEY = "splittingObj";
    public static final String FIELD_MAP_INDEX_KEY = "index";
    public static final String FIELD_MAP_JOINING_KEY = "joiningObj";

    protected NestedAtomic inFields;
    protected NestedAtomic outFields;
    protected ArgumentSeparator splitobj;
    protected ArgumentSeparator joinObj;
    protected int inIndex;
    protected int outIndex;

    // CONSTRUCTORS
    public FieldMap()
    {
	inFields = null;
	outFields = null;
    }

    public FieldMap(NestedAtomic in, NestedAtomic out)
    {
	inFields = in;
	outFields = out;
    }

    public FieldMap(NestedAtomic in, NestedAtomic out, ArgumentSeparator splitObj, ArgumentSeparator joinObj)
    {
	this.inFields = in;
	this.outFields = out;
	this.splitobj = splitObj;
	this.joinObj = joinObj;
    }

    // GETTER AND SETTER METHODS FOR GETTING AND SETTING THE IN-FIELDS AND
    // OUT-FIELDS RESPECTIVELY

    public void setSplitter(ArgumentSeparator obj)
    {
	splitobj = obj;
    }

    public ArgumentSeparator getSplitter()
    {
	return splitobj;
    }

    public ArgumentSeparator getJoiner()
    {
	return this.joinObj;
    }

    public void setInIndex(int ind)
    {
	inIndex = ind;
    }

    public int getInIndex()
    {
	return inIndex;
    }

    public int getOutIndex()
    {
	return outIndex;
    }

    public void setOutIndex(int outIndex)
    {
	this.outIndex = outIndex;
    }

    public void setInField(NestedAtomic in)
    {
	inFields = in;
    }

    public NestedAtomic getInFields()
    {
	return inFields;
    }

    public NestedAtomic getOutFields()
    {
	return outFields;
    }

    public void setOutField(NestedAtomic out)
    {
	outFields = out;
    }

    // Equality Operations
    @Override
    public boolean equals(Object otherObject)
    {
	if (!super.equals(otherObject))
	    return false;

	if (!(otherObject instanceof FieldMap))
	    return false;

	FieldMap other = (FieldMap) otherObject;

	if (!fieldIsEqual(this.inFields, other.inFields))
	    return false;

	if (!fieldIsEqual(this.outFields, other.outFields))
	    return false;
	if (!fieldIsEqual(this.splitobj, other.splitobj))
	    return false;
	if (!fieldIsEqual(this.joinObj, other.joinObj))
	    return false;
	if (!fieldIsEqual(this.inIndex, other.inIndex))
	    return false;

	return true;
    }

    @Override
    public int hashCode()
    {
	int result = super.hashCode();
	int arbitraryPrimeNumber = 23;

	if (this.inFields != null)
	    result = result * arbitraryPrimeNumber + this.inFields.hashCode();
	if (this.outFields != null)
	    result = result * arbitraryPrimeNumber + this.outFields.hashCode();
	if (this.splitobj != null)
	    result = result * arbitraryPrimeNumber + this.splitobj.hashCode();
	if (this.joinObj != null)
	    result = result * arbitraryPrimeNumber + this.joinObj.hashCode();

	return result;

    }

    // Serialization/Deserialization
    @Override
    public void initializeFromToken(StorageToken token)
    {
	super.initializeFromToken(token);
	this.inFields = (NestedAtomic) SerializationConvenience.untokenizeObject(token.getItem(FIELD_MAP_INFIELDS_KEY));
	this.outFields = (NestedAtomic) SerializationConvenience.untokenizeObject(token.getItem(FIELD_MAP_OUTFIELDS_KEY));
	this.splitobj = (ArgumentSeparator) SerializationConvenience.untokenizeObject(token.getItem(FIELD_MAP_SPLITTING_KEY));
	this.joinObj = (ArgumentSeparator) SerializationConvenience.untokenizeObject(token.getItem(FIELD_MAP_JOINING_KEY));
	this.inIndex = (int) SerializationConvenience.untokenizeObject(token.getItem(FIELD_MAP_INDEX_KEY));
    }

    @Override
    public StorageToken saveToToken()
    {
	StorageToken result = super.saveToToken();
	result.setItem(FIELD_MAP_INFIELDS_KEY, SerializationConvenience.tokenizeObject(this.inFields));
	result.setItem(FIELD_MAP_OUTFIELDS_KEY, SerializationConvenience.tokenizeObject(this.outFields));
	result.setItem(FIELD_MAP_SPLITTING_KEY, SerializationConvenience.tokenizeObject(this.splitobj));
	result.setItem(FIELD_MAP_INDEX_KEY, SerializationConvenience.tokenizeObject(this.inIndex));
	result.setItem(FIELD_MAP_JOINING_KEY, SerializationConvenience.tokenizeObject(this.joinObj));
	return result;
    }

    /**
     * apply the field mapping to an incoming StorageToken
     * 
     */
    public StorageToken applyMapping(StorageToken sourceMsg, StorageToken destMsgTemplate)
    {//TODO: implement this function and replace the mess in MessageMap.convert.
	return null;
    }
}
