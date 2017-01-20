package Ontology.Mappings;

import Util.Serializable;
import Util.SerializationConvenience;
import Util.StorageToken;

public class FieldMap extends Serializable {
	
	public static final String FIELD_MAP_INFIELDS_KEY = "inFields";
	public static final String FIELD_MAP_OUTFIELDS_KEY = "outFields";
	
	private NestedAtomic inFields;
	private NestedAtomic outFields;
	
	//CONSTRUCTORS
	public FieldMap()
	{
		inFields=null;
		outFields=null;
	}
	public FieldMap(NestedAtomic in, NestedAtomic out)
	{
		inFields=in;
		outFields=out;
	}
	
	
	//Equality Operations
		@Override
		public boolean equals(Object otherObject) {
			if(!super.equals(otherObject))
				return false;
			
			if(!(otherObject instanceof FieldMap))
				return false;
			
			FieldMap other = (FieldMap)otherObject;
			
			if(!fieldIsEqual(this.inFields, other.inFields))
				return false;
			
			if(!fieldIsEqual(this.outFields, other.outFields))
				return false;
			
			return true;
		}

		@Override
		public int hashCode() {
			int result = super.hashCode();
			int arbitraryPrimeNumber = 23;
			
			if(this.inFields != null)
				result = result * arbitraryPrimeNumber + this.inFields.hashCode();
			if(this.outFields != null)
				result = result * arbitraryPrimeNumber + this.outFields.hashCode();
			
			return result;
			
		}

		
		//Serialization/Deserialization
		@Override
		public void initializeFromToken(StorageToken token) {
			super.initializeFromToken(token);
			this.inFields = (NestedAtomic)SerializationConvenience.untokenizeObject(token.getItem(FIELD_MAP_INFIELDS_KEY));
			this.outFields = (NestedAtomic)SerializationConvenience.untokenizeObject(token.getItem(FIELD_MAP_OUTFIELDS_KEY));
		}

		@Override
		public StorageToken saveToToken() {
			StorageToken result = super.saveToToken();
			result.setItem(FIELD_MAP_INFIELDS_KEY, SerializationConvenience.tokenizeObject(this.inFields));
			result.setItem(FIELD_MAP_OUTFIELDS_KEY, SerializationConvenience.tokenizeObject(this.outFields));
			return result;
		}

	
	
	//GETTER AND SETTER METHODS
	public void setInField(NestedAtomic in)
	{
		inFields=in;
	}
	
	public void setOutField(NestedAtomic out)
	{
		outFields=out;
	}
	
	
	public void apply(StorageToken in, StorageToken out)
	{
		
	}
	
	
	
		
		
	
	
}
