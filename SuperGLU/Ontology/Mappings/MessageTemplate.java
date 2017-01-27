package Ontology.Mappings;
/**
 * MessageTemplate  Class
 * @author tirthmehta
 */
import java.util.ArrayList;

import Util.Serializable;
import Util.SerializationConvenience;
import Util.StorageToken;

public class MessageTemplate extends Serializable {
	
	private ArrayList<FieldData> defaultFieldData=new ArrayList<>();
	public static final String MESSAGE_TEMPLATE_DEFAULTFIELDDATA_KEY = "messageTemplate";
	
	public MessageTemplate()
	{
		defaultFieldData=null;
	}
	
	public MessageTemplate(ArrayList<FieldData> arrlist)
	{
		if(arrlist==null)
			defaultFieldData=null;
		else
		{
			for(FieldData x:arrlist)
			{
				defaultFieldData.add(x);
			}
		}
	}
	
	public ArrayList<FieldData> getDefaultFieldData()
	{
		return defaultFieldData;
	}
		
	//Equality Operations
		@Override
		public boolean equals(Object otherObject) {
			if(!super.equals(otherObject))
				return false;
			
			if(!(otherObject instanceof FieldData))
				return false;
			
			MessageTemplate other = (MessageTemplate)otherObject;
			
			if(!fieldIsEqual(this.defaultFieldData, other.defaultFieldData))
				return false;
			
			return true;
		}

		@Override
		public int hashCode() {
			int result = super.hashCode();
			int arbitraryPrimeNumber = 23;
			
			if(this.defaultFieldData != null)
				result = result * arbitraryPrimeNumber + this.defaultFieldData.hashCode();
			
			return result;
			
		}

		
		//Serialization/Deserialization
		@Override
		public void initializeFromToken(StorageToken token) {
			super.initializeFromToken(token);
			this.defaultFieldData = (ArrayList<FieldData>)SerializationConvenience.untokenizeObject(token.getItem(MESSAGE_TEMPLATE_DEFAULTFIELDDATA_KEY));
		}

		@Override
		public StorageToken saveToToken() {
			StorageToken result = super.saveToToken();
			result.setItem(MESSAGE_TEMPLATE_DEFAULTFIELDDATA_KEY, SerializationConvenience.tokenizeObject(this.defaultFieldData));
			return result;
		}

	
	
	
	
	
	
	
	
	
	
	//setter and getter methods
	public void setData(ArrayList<FieldData> arrFieldData)
	{
		if(arrFieldData==null)
			defaultFieldData=null;
		else
		{
			for(FieldData x:arrFieldData)
			{
				defaultFieldData.add(x);
			}
		}
	}
	
	public ArrayList<FieldData> getData()
	{
		return defaultFieldData;
	}
	
	
	
	

}
