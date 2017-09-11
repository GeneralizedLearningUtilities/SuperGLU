package Ontology.Mappings;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import Util.Serializable;
import Util.SerializationConvenience;
import Util.StorageToken;

/**
 * MessageMap Class The class is used to store the complete data regarding a
 * valid mapping like inmsgtype,outmsgtype,fieldmappings, etc. It basically
 * stores all the necessary data required for identifying a valid mapping
 * amongst a set of mappings.
 * 
 * @author auerbach
 * @author tirthmehta
 */

public class MessageMap extends Serializable {
	protected MessageType inMsgType = new MessageType();

	protected MessageType outMsgType = new MessageType();

	protected List<FieldMap> fieldMappings;

	public static final String MESSAGEMAP_INMSGTYPE_KEY = "inMsgType";
	public static final String MESSAGEMAP_OUTMSGTYPE_KEY = "outMsgType";
	public static final String MESSAGEMAP_FIELDMAPPINGS_KEY = "fieldMappings";

	public MessageMap() {
		inMsgType = null;
		outMsgType = null;
		fieldMappings = null;
	}

	// PARAMETERIZED CONSTRUCTORS
	public MessageMap(MessageType in, MessageType out, List<FieldMap> arrmap) {
		if (in == null)
			inMsgType = null;
		else
			inMsgType = in;

		if (out == null)
			outMsgType = null;
		else
			outMsgType = out;

		if (arrmap != null)
			fieldMappings = arrmap;

	}

	// GETTER AND SETTER METHODS FOR GETTING AND SETTING THE
	// INMSGTYPE,OUTMSGTYPE, AND OTHER DATA MENTIONED ABOVE

	public void setInMsgType(MessageType mtype) {
		inMsgType = mtype;
	}

	public void setOutMsgType(MessageType mtype) {
		outMsgType = mtype;
	}

	public void setFieldMappings(ArrayList<FieldMap> arrFieldMap) {
		if (arrFieldMap == null)
			fieldMappings = null;
		else {
			fieldMappings = new ArrayList<FieldMap>();
			for (FieldMap y : arrFieldMap)
				fieldMappings.add(y);
		}
	}

	public MessageType getInMsgType() {
		if (inMsgType == null)
			return null;
		else
			return inMsgType;
	}

	public MessageType getOutMsgType() {
		if (outMsgType == null)
			return null;
		else
			return outMsgType;
	}

	public List<FieldMap> getFieldMappings() {
		if (fieldMappings == null)
			return null;
		else
			return fieldMappings;
	}

	// Equality Operations
	@Override
	public boolean equals(Object otherObject) {
		if (!super.equals(otherObject))
			return false;

		if (!(otherObject instanceof MessageMap))
			return false;

		MessageMap other = (MessageMap) otherObject;

		if (!fieldIsEqual(this.inMsgType, other.inMsgType))
			return false;
		if (!fieldIsEqual(this.outMsgType, other.outMsgType))
			return false;
		if (!fieldIsEqual(this.fieldMappings, other.fieldMappings))
			return false;

		return true;
	}

	@Override
	public int hashCode() {
		int result = super.hashCode();
		int arbitraryPrimeNumber = 23;

		if (this.inMsgType != null)
			result = result * arbitraryPrimeNumber + this.inMsgType.hashCode();
		if (this.outMsgType != null)
			result = result * arbitraryPrimeNumber + this.outMsgType.hashCode();
		if (this.fieldMappings != null)
			result = result * arbitraryPrimeNumber + this.fieldMappings.hashCode();

		return result;

	}

	// Serialization/Deserialization
	@Override
	public void initializeFromToken(StorageToken token) {
		super.initializeFromToken(token);
		this.inMsgType = (MessageType) SerializationConvenience
				.untokenizeObject(token.getItem(MESSAGEMAP_INMSGTYPE_KEY));
		this.outMsgType = (MessageType) SerializationConvenience
				.untokenizeObject(token.getItem(MESSAGEMAP_OUTMSGTYPE_KEY));
		this.fieldMappings = (List<FieldMap>) SerializationConvenience
				.untokenizeObject(token.getItem(MESSAGEMAP_FIELDMAPPINGS_KEY));
	}

	@Override
	public StorageToken saveToToken() {
		StorageToken result = super.saveToToken();
		result.setItem(MESSAGEMAP_INMSGTYPE_KEY, SerializationConvenience.tokenizeObject(this.inMsgType));
		result.setItem(MESSAGEMAP_OUTMSGTYPE_KEY, SerializationConvenience.tokenizeObject(this.outMsgType));
		result.setItem(MESSAGEMAP_FIELDMAPPINGS_KEY, SerializationConvenience.tokenizeObject(this.fieldMappings));
		return result;
	}

	/**
	 * THE FUNCTION NECESSARY FOR CHECKING WHETHER THE MESSAGE INOUT TOKEN
	 * COMING IN HAS A VALID MATCH WITH THE AVAIALABLE SET OF MAPPINGS
	 */
	public boolean isValidSourceMsg(StorageToken input) {
		for (FieldMap currentFieldMap : this.fieldMappings) {
			if (!currentFieldMap.doesMappingApply(input))
				return false;
		}

		return true;
	}

	/**
	 * 
	 * THE CONVERT METHOD IS ACTUALLY USED TO PERFORM THE CONVERSION TO THE
	 * TARGET MESSAGE OBJECT, ONCE THE VALID MAPPING HAS BEEN IDENTIFIED
	 * 
	 * @param input
	 * @return
	 */
	public StorageToken convert(StorageToken input, Map<String, Object> context) {
		StorageToken output = outMsgType.getMessageTemplate().createTargetStorageToken(UUID.randomUUID().toString(),
				outMsgType.getClassId());

		for (FieldMap currentMap : this.fieldMappings) {
			currentMap.applyMapping(input, output, context);
		}

		return output;

	}
}
