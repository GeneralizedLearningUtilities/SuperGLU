package Ontology.Mappings;
/**
 * FieldMap Class
 * This is the class that provides a valid mapping to have their respective in-fields and out-fields which
 * are involved in the mapping
 * @author tirthmehta
 */

import java.util.List;

import Util.Serializable;
import Util.SerializationConvenience;
import Util.StorageToken;

public class FieldMap extends Serializable
{

    public static final String FIELD_MAP_INFIELDS_KEY = "inFields";
    public static final String FIELD_MAP_OUTFIELDS_KEY = "outFields";
    public static final String FIELD_MAP_SPLITTING_KEY = "splittingObj";
    public static final String FIELD_MAP_INDEX_KEY = "index";
    
    private NestedAtomic inFields;
    private NestedAtomic outFields;
    private Splitting splitobj;
    private int index;
    
   
    

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

    // GETTER AND SETTER METHODS FOR GETTING AND SETTING THE IN-FIELDS AND
    // OUT-FIELDS RESPECTIVELY
    
    public void setSplitter(Splitting obj)
    {
	splitobj=obj;
    }
    
    public Splitting getSplitter()
    {
	return splitobj;
    }
    
    public void setIndex(int ind)
    {
	index=ind;
    }
    
    public int getIndex()
    {
	return index;
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
	if (!fieldIsEqual(this.index, other.index))
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
	

	return result;

    }

    // Serialization/Deserialization
    @Override
    public void initializeFromToken(StorageToken token)
    {
	super.initializeFromToken(token);
	this.inFields = (NestedAtomic) SerializationConvenience.untokenizeObject(token.getItem(FIELD_MAP_INFIELDS_KEY));
	this.outFields = (NestedAtomic) SerializationConvenience.untokenizeObject(token.getItem(FIELD_MAP_OUTFIELDS_KEY));
	this.splitobj = (Splitting) SerializationConvenience.untokenizeObject(token.getItem(FIELD_MAP_SPLITTING_KEY));
	this.index = (int) SerializationConvenience.untokenizeObject(token.getItem(FIELD_MAP_INDEX_KEY));
    }

    @Override
    public StorageToken saveToToken()
    {
	StorageToken result = super.saveToToken();
	result.setItem(FIELD_MAP_INFIELDS_KEY, SerializationConvenience.tokenizeObject(this.inFields));
	result.setItem(FIELD_MAP_OUTFIELDS_KEY, SerializationConvenience.tokenizeObject(this.outFields));
	result.setItem(FIELD_MAP_SPLITTING_KEY, SerializationConvenience.tokenizeObject(this.splitobj));
	result.setItem(FIELD_MAP_INDEX_KEY, SerializationConvenience.tokenizeObject(this.index));
	
	return result;
    }

}
