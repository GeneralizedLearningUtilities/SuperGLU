/**
 * This class is the framework for specifying how tokens are turned into a specific format (ie. JSON or XML)
 * The actual code is handled in subclasses.
 * 
 * @author auerbach
 */
package Util.tokenformat;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import Util.StorageToken;

/**
 * """ Class that writes storage tokens """
 * @author auerbach
 *
 */

public abstract class TokenRWFormat {

	public static ArrayList<Class<?>> VALID_KEY_TYPES = new ArrayList<>();
	public static ArrayList<Class<?>> VALID_VALUE_TYPES = new ArrayList<>();
	
	public static ArrayList<Class<?>> VALID_ATOMIC_VALUE_TYPES = new ArrayList<Class<?>>();
	public static ArrayList<Class<?>> VALID_SEQUENCE_TYPES = new ArrayList<>();
	public static ArrayList<Class<?>> VALID_MAPPING_TYPES = new ArrayList<>();
	
	
	static
	{
		VALID_KEY_TYPES.add(String.class);
		populateValidAtomicValueTypes();
		populateValidSequenceTypes();
		populateValidMappingTypes();
		VALID_VALUE_TYPES.addAll(VALID_ATOMIC_VALUE_TYPES);
		VALID_VALUE_TYPES.addAll(VALID_SEQUENCE_TYPES);
		VALID_VALUE_TYPES.addAll(VALID_MAPPING_TYPES);
	}
	
	
	private static void populateValidAtomicValueTypes()
	{
		VALID_ATOMIC_VALUE_TYPES.add(boolean.class);
		VALID_ATOMIC_VALUE_TYPES.add(Boolean.class);
		VALID_ATOMIC_VALUE_TYPES.add(int.class);
		VALID_ATOMIC_VALUE_TYPES.add(Integer.class);
		VALID_ATOMIC_VALUE_TYPES.add(Float.class);
		VALID_ATOMIC_VALUE_TYPES.add(Double.class);
		VALID_ATOMIC_VALUE_TYPES.add(float.class);
		VALID_ATOMIC_VALUE_TYPES.add(Number.class);
		VALID_ATOMIC_VALUE_TYPES.add(String.class);
		VALID_ATOMIC_VALUE_TYPES.add(BigDecimal.class);
		//VALID_ATOMIC_VALUE_TYPES.add(null);//Not sure if this should be here.  I don't think so.
	}
	
	private static void populateValidSequenceTypes()
	{
		VALID_SEQUENCE_TYPES.add(List.class);
		VALID_SEQUENCE_TYPES.add(ArrayList.class);
	}
	
	
	private static void populateValidMappingTypes()
	{
		VALID_MAPPING_TYPES.add(Map.class);
		VALID_MAPPING_TYPES.add(HashMap.class);
	}
	
	// """ Parse a string into Storage Tokens """
	public static StorageToken parse(String input)
	{
		throw new RuntimeException("Method Not Implemented");
	}
	
	//  """ Serialize Storage Token objects into a string form """
	public static Object serialize(StorageToken data)
	{
		throw new RuntimeException("Method Not Implemented");
	}
	
	
};
