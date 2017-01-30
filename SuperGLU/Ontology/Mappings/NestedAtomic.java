package Ontology.Mappings;
/**
 * NestedAtomic  Class
 * @author tirthmehta
 */
import Util.Serializable;
import Util.SerializationConvenience;
import Util.StorageToken;

public class NestedAtomic extends Serializable {

	public static final String NESTED_ATOMIC_INDICES_KEY = "nestedAtomicIndices";
	private String indices;
	private FieldData fielddata;
	
	//CONSTRUCTORS
	public NestedAtomic(String index)
	{
		if(index==null)
			indices=null;
		else
			this.indices=index;
	}
	
	public NestedAtomic()
	{
		this.indices=null;
	}
	
	//GETTER AND SETTER METHODS
	
	public String getIndex()
	{
		return indices;
	}
	
	public void setIndex(String ind)
	{
		this.indices=ind;
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
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
}
