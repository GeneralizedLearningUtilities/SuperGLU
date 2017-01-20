package Ontology.Mappings;

import Util.Serializable;
import Util.SerializationConvenience;
import Util.StorageToken;

public class NestedAtomic extends Serializable {

	public static final String NESTED_ATOMIC_INDICES_KEY = "nestedAtomicIndices";
	private String indices;
	
	//CONSTRUCTORS
	public NestedAtomic(String index)
	{
		if(index=="")
			indices="";
		else
			this.indices=index;
	}
	
	public NestedAtomic()
	{
		this.indices="";
	}
	
	//Equality Operations
		@Override
		public boolean equals(Object otherObject) {
			if(!super.equals(otherObject))
				return false;
			
			if(!(otherObject instanceof NestedAtomic))
				return false;
			
			NestedAtomic other = (NestedAtomic)otherObject;
			
			if(!fieldIsEqual(this.indices, other.indices))
				return false;
			
			return true;
		}

		@Override
		public int hashCode() {
			int result = super.hashCode();
			int arbitraryPrimeNumber = 23;
			
			if(this.indices != null)
				result = result * arbitraryPrimeNumber + this.indices.hashCode();
			
			return result;
			
		}

		
		//Serialization/Deserialization
		@Override
		public void initializeFromToken(StorageToken token) {
			super.initializeFromToken(token);
			this.indices = (String)SerializationConvenience.untokenizeObject(token.getItem(NESTED_ATOMIC_INDICES_KEY));
		}

		@Override
		public StorageToken saveToToken() {
			StorageToken result = super.saveToToken();
			result.setItem(NESTED_ATOMIC_INDICES_KEY, SerializationConvenience.tokenizeObject(this.indices));
			return result;
		}
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	//GETTER AND SETTER METHODS
	public String getIndices()
	{
		return indices;
	}
	
	public void setIndices(String index)
	{
		indices=index;
	}
	
}
