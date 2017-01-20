package Ontology.Mappings;
import java.util.*;

import Util.Serializable;
import Util.SerializationConvenience;
import Util.StorageToken;

public class MessageMap extends Serializable
{
	MessageType inMsgType= new MessageType();
	
	MessageType outMsgType= new MessageType();
	
	MessageTemplate inDefaultMsg= new MessageTemplate();
	
	MessageTemplate outDefaultMsg= new MessageTemplate();
	
	ArrayList<FieldMap> fieldMappings;
	
	
	public static final String MESSAGEMAP_INMSGTYPE_KEY = "inMsg";
	public static final String MESSAGEMAP_OUTMSGTYPE_KEY = "outMsg";
	public static final String MESSAGEMAP_INDEFAULT_KEY = "inDefaultMsg";
	public static final String MESSAGEMAP_OUTDEFAULT_KEY = "outDefaultMsg";
	public static final String MESSAGEMAP_FIELDMAPPINGS_KEY = "fieldMappings";
	
	//CONSTRUCTORS
	public MessageMap()
	{
		inMsgType=null;
		outDefaultMsg=null;
		outMsgType=null;
		inDefaultMsg=null;
		fieldMappings=null;
	}
	
	public MessageMap(MessageType in, MessageType out, MessageTemplate m_in, MessageTemplate m_out, ArrayList<FieldMap> arrmap)
	{
		if(in==null)
			inMsgType=null;
		else
			inMsgType=in;
		
		if(out==null)
			outMsgType=null;
		else
			outMsgType=out;
		
		if(m_in==null)
			inDefaultMsg=null;
		else
			inDefaultMsg=m_in;
		
		if(m_out==null)
			outDefaultMsg=null;
		else
			outDefaultMsg=m_out;
		
		if(arrmap==null)
			fieldMappings=null;
		else
		{
			for(FieldMap x:arrmap)
				fieldMappings.add(x);
		}
		
	}
	
	
	//Equality Operations
		@Override
		public boolean equals(Object otherObject) {
			if(!super.equals(otherObject))
				return false;
			
			if(!(otherObject instanceof MessageMap))
				return false;
			
			MessageMap other = (MessageMap)otherObject;
			
			if(!fieldIsEqual(this.inMsgType, other.inMsgType))
				return false;
			if(!fieldIsEqual(this.outMsgType, other.outMsgType))
				return false;
			if(!fieldIsEqual(this.inDefaultMsg, other.inDefaultMsg))
				return false;
			if(!fieldIsEqual(this.outDefaultMsg, other.outDefaultMsg))
				return false;
			if(!fieldIsEqual(this.fieldMappings, other.fieldMappings))
				return false;
			
			return true;
		}

		@Override
		public int hashCode() {
			int result = super.hashCode();
			int arbitraryPrimeNumber = 23;
			
			if(this.inMsgType != null)
				result = result * arbitraryPrimeNumber + this.inMsgType.hashCode();
			if(this.outMsgType != null)
				result = result * arbitraryPrimeNumber + this.outMsgType.hashCode();
			if(this.inDefaultMsg != null)
				result = result * arbitraryPrimeNumber + this.inDefaultMsg.hashCode();
			if(this.outDefaultMsg != null)
				result = result * arbitraryPrimeNumber + this.outDefaultMsg.hashCode();
			if(this.fieldMappings != null)
				result = result * arbitraryPrimeNumber + this.fieldMappings.hashCode();
			
			return result;
			
		}

		
		//Serialization/Deserialization
		@Override
		public void initializeFromToken(StorageToken token) {
			super.initializeFromToken(token);
			this.inMsgType = (MessageType)SerializationConvenience.untokenizeObject(token.getItem(MESSAGEMAP_INMSGTYPE_KEY));
			this.outMsgType = (MessageType)SerializationConvenience.untokenizeObject(token.getItem(MESSAGEMAP_OUTMSGTYPE_KEY));
			this.inDefaultMsg = (MessageTemplate)SerializationConvenience.untokenizeObject(token.getItem(MESSAGEMAP_INDEFAULT_KEY));
			this.outDefaultMsg = (MessageTemplate)SerializationConvenience.untokenizeObject(token.getItem(MESSAGEMAP_OUTDEFAULT_KEY));
			this.fieldMappings = (ArrayList<FieldMap>)SerializationConvenience.untokenizeObject(token.getItem(MESSAGEMAP_FIELDMAPPINGS_KEY));
		}

		@Override
		public StorageToken saveToToken() {
			StorageToken result = super.saveToToken();
			result.setItem(MESSAGEMAP_INMSGTYPE_KEY, SerializationConvenience.tokenizeObject(this.inMsgType));
			result.setItem(MESSAGEMAP_OUTMSGTYPE_KEY, SerializationConvenience.tokenizeObject(this.outMsgType));
			result.setItem(MESSAGEMAP_INDEFAULT_KEY, SerializationConvenience.tokenizeObject(this.inDefaultMsg));
			result.setItem(MESSAGEMAP_OUTDEFAULT_KEY, SerializationConvenience.tokenizeObject(this.outDefaultMsg));
			result.setItem(MESSAGEMAP_FIELDMAPPINGS_KEY, SerializationConvenience.tokenizeObject(this.fieldMappings));
			return result;
		}

	
	
	
	
	
	
	
	
	
	
	//GETTER AND SETTER METHODS
	
	public void setInMsgType(MessageType mtype)
	{
		if(mtype==null)
			inMsgType=null;
		else
			inMsgType=mtype;
	}
	
	public void setOutMsgType(MessageType mtype)
	{
		if(mtype==null)
			outMsgType=null;
		else
			outMsgType=mtype;
	}

	public void setInDefaultMsgType(MessageTemplate mtemp)
	{
		if(mtemp==null)
			inDefaultMsg=null;
		else
			inDefaultMsg=mtemp;
	}
	
	public void setOutDefaultMsgType(MessageTemplate mtemp)
	{
		if(mtemp==null)
			outDefaultMsg=null;
		else
			outDefaultMsg=mtemp;
	}
	
	public void setFieldMappings(ArrayList<FieldMap> arrFieldMap)
	{
		if(arrFieldMap==null)
			fieldMappings=null;
		else
		{
			for(FieldMap y:arrFieldMap)
				fieldMappings.add(y);
		}
	}
	
	
	
	
}

