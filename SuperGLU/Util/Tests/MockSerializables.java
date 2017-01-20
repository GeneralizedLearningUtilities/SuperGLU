package Util.Tests;

/**
 * This class contains sample serializable objects for testing and demonstration purposes
 * 
 * @author auerbach
 */

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import Util.Serializable;
import Util.SerializationConvenience;
import Util.StorageToken;

public class MockSerializables
{
	public static class MockSerializable extends Serializable
	{
		private int foo;
		private String bar;
		
		private static final String FOO_KEY = "foo";
		private static final String BAR_KEY = "bar";
		
		
		public MockSerializable()
		{
			super();
			this.foo = -1;
			this.bar = null;
		}
		
		
		public MockSerializable(int foo, String bar)
		{
			super();
			this.foo = foo;
			this.bar = bar;
		}
		
		
		
		//Equals and Hashcode don't strictly speaking have to be re-implemented in real objects, but it helps when testing.
		@Override
		public boolean equals(Object otherObject)
		{
			if(!super.equals(otherObject))
				return false;
			
			if(!(otherObject instanceof MockSerializable))
				return false;
			
			MockSerializable other = (MockSerializable)otherObject;
			
			if(this.foo != other.foo)
				return false;
			
			if(!this.bar.equals(other.bar))
				return false;
			
			return true;
		}
		
		
		@Override
		public int hashCode()
		{
			int result = super.hashCode();
			
			int arbitraryPrimeNumber = 29;
			
			result = result * arbitraryPrimeNumber + foo;
			if(bar != null)
				result = result * arbitraryPrimeNumber + bar.hashCode();
			
			return result;
		}
		
		
		@Override
		public void initializeFromToken(StorageToken token)
		{
			super.initializeFromToken(token);
			this.foo = ((Integer)SerializationConvenience.untokenizeObject(token.getItem(FOO_KEY, true, -1)));
			this.bar = (String)token.getItem(BAR_KEY, true, null);
		}
		
		
		@Override
		public StorageToken saveToToken()
		{
			StorageToken token = super.saveToToken();
			token.setItem(FOO_KEY, this.foo);
			token.setItem(BAR_KEY, this.bar);
			return token;
		}	
	}
	
	
	public static class MockSerializable2 extends Serializable
	{
		private int foo;
		private String bar;
		private List<String> baz;
		
		private static final String FOO_KEY = "foo";
		private static final String BAR_KEY = "bar";
		private static final String BAZ_KEY = "baz";
		
		public MockSerializable2()
		{
			super();
			this.foo = -1;
			this.bar = null;
			this.baz = null;
		}
		
		
		public MockSerializable2(int foo, String bar, List<String> baz)
		{
			super();
			this.foo = foo;
			this.bar = bar;
			this.baz = baz;
		}
		
		
		@Override
		public boolean equals(Object otherObject)
		{
			if(!super.equals(otherObject))
				return false;
			
			if(!(otherObject instanceof MockSerializable2))
				return false;
			
			MockSerializable2 other = (MockSerializable2)otherObject;
			
			if(this.foo != other.foo)
				return false;
			
			if(this.bar != other.bar)
				return false;
			
			if(!this.baz.equals(other.baz))
				return false;
			
			return true;
		}
		
		
		@Override
		public int hashCode()
		{
			int result = super.hashCode();
			
			int arbitraryPrimeNumber = 29;
			
			result = result * arbitraryPrimeNumber + foo;
			if(bar != null)
				result = result * arbitraryPrimeNumber + bar.hashCode();
			
			if(baz != null)
				result = result * arbitraryPrimeNumber + baz.hashCode();
			
			return result;
		}
		
		
		@Override
		public void initializeFromToken(StorageToken token)
		{
			super.initializeFromToken(token);
			this.foo = (int)token.getItem(FOO_KEY, true, -1);
			this.bar = (String)token.getItem(BAR_KEY, true, null);
			this.baz = (List<String>)token.getItem(BAZ_KEY, true, new ArrayList<>());
		}
		
		
		@Override
		public StorageToken saveToToken()
		{
			StorageToken token = super.saveToToken();
			token.setItem(FOO_KEY, this.foo);
			token.setItem(BAR_KEY, this.bar);
			token.setItem(BAZ_KEY, this.baz);
			return token;
		}	
	}
	
	
	public static class MockSerializable3 extends Serializable
	{
		private int foo;
		private String bar;
		private Map<String, Integer> baz;
		
		private static final String FOO_KEY = "foo";
		private static final String BAR_KEY = "bar";
		private static final String BAZ_KEY = "baz";
		
		public MockSerializable3()
		{
			super();
			this.foo = -1;
			this.bar = null;
			this.baz = null;
		}
		
		
		public MockSerializable3(int foo, String bar, Map<String, Integer> baz)
		{
			super();
			this.foo = foo;
			this.bar = bar;
			this.baz = baz;
		}
		
		
		@Override
		public boolean equals(Object otherObject)
		{
			if(!super.equals(otherObject))
				return false;
			
			if(!(otherObject instanceof MockSerializable3))
				return false;
			
			MockSerializable3 other = (MockSerializable3)otherObject;
			
			if(this.foo != other.foo)
				return false;
			
			if(this.bar != other.bar)
				return false;
			
			if(!this.baz.equals(other.baz))
				return false;
			
			return true;
		}
		
		
		@Override
		public int hashCode()
		{
			int result = super.hashCode();
			
			int arbitraryPrimeNumber = 29;
			
			result = result * arbitraryPrimeNumber + foo;
			if(bar != null)
				result = result * arbitraryPrimeNumber + bar.hashCode();
			
			if(baz != null)
				result = result * arbitraryPrimeNumber + baz.hashCode();
			
			return result;
		}
		
		
		
		@Override
		public void initializeFromToken(StorageToken token)
		{
			super.initializeFromToken(token);
			this.foo = (int)token.getItem(FOO_KEY, true, -1);
			this.bar = (String)token.getItem(BAR_KEY, true, null);
			this.baz = (Map<String, Integer>)SerializationConvenience.untokenizeObject(token.getItem(BAZ_KEY, true, new HashMap<>()));
		}
		
		
		@Override
		public StorageToken saveToToken()
		{
			StorageToken token = super.saveToToken();
			token.setItem(FOO_KEY, this.foo);
			token.setItem(BAR_KEY, this.bar);
			token.setItem(BAZ_KEY, SerializationConvenience.tokenizeObject(this.baz));
			return token;
		}	
	}
	
	
	public static class MockSerializable4 extends Serializable
	{
		private int foo;
		private String bar;
		private MockSerializable baz;
		
		private static final String FOO_KEY = "foo";
		private static final String BAR_KEY = "bar";
		private static final String BAZ_KEY = "baz";
		
		public MockSerializable4()
		{
			super();
			this.foo = -1;
			this.bar = null;
			this.baz = null;
		}
		
		
		public MockSerializable4(int foo, String bar, MockSerializable baz)
		{
			super();
			this.foo = foo;
			this.bar = bar;
			this.baz = baz;
		}
		
		
		@Override
		public boolean equals(Object otherObject)
		{
			if(!super.equals(otherObject))
				return false;
			
			if(!(otherObject instanceof MockSerializable4))
				return false;
			
			MockSerializable4 other = (MockSerializable4)otherObject;
			
			if(this.foo != other.foo)
				return false;
			
			if(this.bar != other.bar)
				return false;
			
			if(!this.baz.equals(other.baz))
				return false;
			
			return true;
		}
		
		
		@Override
		public int hashCode()
		{
			int result = super.hashCode();
			
			int arbitraryPrimeNumber = 29;
			
			result = result * arbitraryPrimeNumber + foo;
			if(bar != null)
				result = result * arbitraryPrimeNumber + bar.hashCode();
			
			if(baz != null)
				result = result * arbitraryPrimeNumber + baz.hashCode();
			
			return result;
		}
		
		
		@Override
		public void initializeFromToken(StorageToken token)
		{
			super.initializeFromToken(token);
			this.foo = (int)token.getItem(FOO_KEY, true, -1);
			this.bar = (String)token.getItem(BAR_KEY, true, null);
			this.baz = (MockSerializable) Serializable.createFromToken((StorageToken) token.getItem(BAZ_KEY, true, null));
		}
		
		
		@Override
		public StorageToken saveToToken()
		{
			StorageToken token = super.saveToToken();
			token.setItem(FOO_KEY, this.foo);
			token.setItem(BAR_KEY, this.bar);
			token.setItem(BAZ_KEY, this.baz.saveToToken());
			return token;
		}	
	}
}