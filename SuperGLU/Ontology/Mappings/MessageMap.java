package Ontology.Mappings;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import Util.Pair;

/**
 * MessageMap  Class
 * The class is used to store the complete data regarding a valid mapping like inmsgtype,outmsgtype,fieldmappings, etc.
 * It basically stores all the necessary data required for identifying a valid mapping amongst a set of mappings.
 * @author tirthmehta
 */

import Util.Serializable;
import Util.SerializationConvenience;
import Util.StorageToken;

public class MessageMap extends Serializable
{
    protected MessageType inMsgType = new MessageType();

    protected MessageType outMsgType = new MessageType();

    protected MessageTemplate inDefaultMsg = new MessageTemplate();

    protected MessageTemplate outDefaultMsg = new MessageTemplate();

    protected List<FieldMapOneToOne> fieldMappings;

    public static final String MESSAGEMAP_INMSGTYPE_KEY = "inMsg";
    public static final String MESSAGEMAP_OUTMSGTYPE_KEY = "outMsg";
    public static final String MESSAGEMAP_INDEFAULT_KEY = "inDefaultMsg";
    public static final String MESSAGEMAP_OUTDEFAULT_KEY = "outDefaultMsg";
    public static final String MESSAGEMAP_FIELDMAPPINGS_KEY = "fieldMappings";

    public MessageMap()
    {
	inMsgType = null;
	outDefaultMsg = null;
	outMsgType = null;
	inDefaultMsg = null;
	fieldMappings = null;
    }

    // PARAMETERIZED CONSTRUCTORS
    public MessageMap(MessageType in, MessageType out, MessageTemplate m_in, MessageTemplate m_out, ArrayList<FieldMapOneToOne> arrmap)
    {
	if (in == null)
	    inMsgType = null;
	else
	    inMsgType = in;

	if (out == null)
	    outMsgType = null;
	else
	    outMsgType = out;

	if (m_in == null)
	    inDefaultMsg = null;
	else
	    inDefaultMsg = m_in;

	if (m_out == null)
	    outDefaultMsg = null;
	else
	    outDefaultMsg = m_out;

	if (arrmap != null)
	    fieldMappings = arrmap;

    }

    // GETTER AND SETTER METHODS FOR GETTING AND SETTING THE
    // INMSGTYPE,OUTMSGTYPE, AND OTHER DATA MENTIONED ABOVE

    public void setInMsgType(MessageType mtype)
    {
	inMsgType = mtype;
    }

    public void setOutMsgType(MessageType mtype)
    {
	outMsgType = mtype;
    }

    public void setInDefaultMsgType(MessageTemplate mtemp)
    {
	inDefaultMsg = mtemp;
    }

    public void setOutDefaultMsgType(MessageTemplate mtemp)
    {
	outDefaultMsg = mtemp;
    }

    public void setFieldMappings(ArrayList<FieldMapOneToOne> arrFieldMap)
    {
	if (arrFieldMap == null)
	    fieldMappings = null;
	else
	{
	    fieldMappings = new ArrayList<FieldMapOneToOne>();
	    for (FieldMapOneToOne y : arrFieldMap)
		fieldMappings.add(y);
	}
    }

    public MessageType getInMsgType()
    {
	if (inMsgType == null)
	    return null;
	else
	    return inMsgType;
    }

    public MessageType getOutMsgType()
    {
	if (outMsgType == null)
	    return null;
	else
	    return outMsgType;
    }

    public MessageTemplate getInDefaulttMsgTemp()
    {
	if (inDefaultMsg == null)
	    return null;
	else
	    return inDefaultMsg;
    }

    public MessageTemplate getOutDefaulttMsgTemp()
    {
	if (outDefaultMsg == null)
	    return null;
	else
	    return outDefaultMsg;
    }

    public List<FieldMapOneToOne> getFieldMappings()
    {
	if (fieldMappings == null)
	    return null;
	else
	    return fieldMappings;
    }

    // Equality Operations
    @Override
    public boolean equals(Object otherObject)
    {
	if (!super.equals(otherObject))
	    return false;

	if (!(otherObject instanceof MessageMap))
	    return false;

	MessageMap other = (MessageMap) otherObject;

	if (!fieldIsEqual(this.inMsgType, other.inMsgType))
	    return false;
	if (!fieldIsEqual(this.outMsgType, other.outMsgType))
	    return false;
	if (!fieldIsEqual(this.inDefaultMsg, other.inDefaultMsg))
	    return false;
	if (!fieldIsEqual(this.outDefaultMsg, other.outDefaultMsg))
	    return false;
	if (!fieldIsEqual(this.fieldMappings, other.fieldMappings))
	    return false;

	return true;
    }

    @Override
    public int hashCode()
    {
	int result = super.hashCode();
	int arbitraryPrimeNumber = 23;

	if (this.inMsgType != null)
	    result = result * arbitraryPrimeNumber + this.inMsgType.hashCode();
	if (this.outMsgType != null)
	    result = result * arbitraryPrimeNumber + this.outMsgType.hashCode();
	if (this.inDefaultMsg != null)
	    result = result * arbitraryPrimeNumber + this.inDefaultMsg.hashCode();
	if (this.outDefaultMsg != null)
	    result = result * arbitraryPrimeNumber + this.outDefaultMsg.hashCode();
	if (this.fieldMappings != null)
	    result = result * arbitraryPrimeNumber + this.fieldMappings.hashCode();

	return result;

    }

    // Serialization/Deserialization
    @Override
    public void initializeFromToken(StorageToken token)
    {
	super.initializeFromToken(token);
	this.inMsgType = (MessageType) SerializationConvenience.untokenizeObject(token.getItem(MESSAGEMAP_INMSGTYPE_KEY));
	this.outMsgType = (MessageType) SerializationConvenience.untokenizeObject(token.getItem(MESSAGEMAP_OUTMSGTYPE_KEY));
	this.inDefaultMsg = (MessageTemplate) SerializationConvenience.untokenizeObject(token.getItem(MESSAGEMAP_INDEFAULT_KEY));
	this.outDefaultMsg = (MessageTemplate) SerializationConvenience.untokenizeObject(token.getItem(MESSAGEMAP_OUTDEFAULT_KEY));
	this.fieldMappings = (List<FieldMapOneToOne>) SerializationConvenience.untokenizeObject(token.getItem(MESSAGEMAP_FIELDMAPPINGS_KEY));
    }

    @Override
    public StorageToken saveToToken()
    {
	StorageToken result = super.saveToToken();
	result.setItem(MESSAGEMAP_INMSGTYPE_KEY, SerializationConvenience.tokenizeObject(this.inMsgType));
	result.setItem(MESSAGEMAP_OUTMSGTYPE_KEY, SerializationConvenience.tokenizeObject(this.outMsgType));
	result.setItem(MESSAGEMAP_INDEFAULT_KEY, SerializationConvenience.tokenizeObject(this.inDefaultMsg));
	result.setItem(MESSAGEMAP_OUTDEFAULT_KEY, SerializationConvenience.tokenizeObject(this.outDefaultMsg));
	result.setItem(MESSAGEMAP_FIELDMAPPINGS_KEY, SerializationConvenience.tokenizeObject(this.fieldMappings));
	return result;
    }

    /**
     * THE FUNCTION NECESSARY FOR CHECKING WHETHER THE MESSAGE INOUT TOKEN
     * COMING IN HAS A VALID MATCH WITH THE AVAIALABLE SET OF MAPPINGS
     */
/*
    public boolean isValidSourceMsg(StorageToken input, String firstwordkey)
    {
	boolean first = false, second = false;

	MessageType in = getInMsgType();

	StorageToken ST_inMsgType = in.saveToToken();

	if (input.getClassId().equals(ST_inMsgType.getItem(MessageType.MESSAGE_TYPE_CLASS_ID_KEY)))
	{
	    first = true;

	}
	MessageTemplate mTemp = in.getMessageTemplate();

	ArrayList<NestedAtomic> arr = mTemp.getDefaultFieldData();

	for (NestedAtomic nest : arr)
	{

	    if (nest.getFieldData().equals(firstwordkey))
	    {
		second = true;
		break;
	    }
	}

	if (first && second) // use more descriptive variable names for god's
			     // sake --Auerbach
	    return true;

	return false;
    }

    /**
     * 
     * THE CONVERT METHOD IS ACTUALLY USED TO PERFORM THE CONVERSION TO THE
     * TARGET MESSAGE OBJECT, ONCE THE VALID MAPPING HAS BEEN IDENTIFIED
     * 
     * @param b
     * @param input
     * @return
     */
/*
    public StorageToken convert(StorageToken input)
    {
	MessageType out = getOutMsgType();
	MessageTemplate mtemp = out.getMessageTemplate();
	StorageToken target = mtemp.createTargetStorageToken(out.getClassId());

	List<FieldMap> mappingList = getFieldMappings();
	for (FieldMap maps : mappingList)
	{

	    NestedAtomic inFields = maps.getInFields();
	    List<Pair<Class<?>,String>> inFieldsIndex = inFields.getIndices();

	    NestedAtomic outFields = maps.getOutFields();
	    List<Pair<Class<?>,String>> outFieldsIndex = outFields.getIndices();

	    String valueToBeInserted = "";
	    HashMap<String, String> hmap = new HashMap<>();
	    for (Pair<Class<?>, String> value : inFieldsIndex)
	    {
		if (input.contains(value.getSecond()))
		{

		    valueToBeInserted = (String) input.getItem(value.getSecond());
		    if (maps.getSplitter() == null)
			hmap.put(value.getSecond(), valueToBeInserted);
		    else
		    {

			ArgumentSeparator current = maps.getSplitter();
			List<String> obtained = current.split(valueToBeInserted);
			int index = maps.getInIndex();
			valueToBeInserted = obtained.get(index);
			hmap.put(value.getSecond(), valueToBeInserted);

		    }
		}

	    }

	    for (Pair<Class<?>, String>  value : outFieldsIndex)
	    {
		for (String key : hmap.keySet())
		{
		    target.setItem(value.getSecond(), hmap.get(key));
		    // Upgrade to a log file instead of console output
		    // --Auerbach
		    System.out.println("check value " + target.getItem(value.getSecond()));
		}

	    }

	}

	// SETTING THE DEFAULT FIELD DATA

	// THIS IS THE PART WHERE THE CORRECT MAPPING WAS USED TO SET THE
	// DEFAULT FIELD DATA
	// I HAVE COMMENTED IT OUT FOR THE MOMENT
	// PLEASE HAVE A LOOK AT IT

	MessageTemplate mtempOut = this.getOutDefaulttMsgTemp();
	ArrayList<NestedAtomic> outarr = mtempOut.getDefaultFieldData();
	HashMap<String, String> hmap = new HashMap<>();
	for (NestedAtomic in : outarr)
	{
	    List<Pair<Class<?>, String>> inside = in.getIndices();
	    for (Pair<Class<?>, String> key : inside)
	    {
		if (target.contains(key.getSecond()))
		{
		    hmap.put(key.getSecond(), in.getFieldData());
		}
	    }
	}
	System.out.println(hmap);

	for (String key : hmap.keySet())
	{
	    target.setItem(key, hmap.get(key));
	}

	return target;

    }
*/
}
