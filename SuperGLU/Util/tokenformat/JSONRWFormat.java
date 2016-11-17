/**
 * This class handles the serialization of StorageTokens to JSON as well as the deserialization of JSON to StorageToken
 * 
 * @author auerbach
 */
package Util.tokenformat;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import Util.StorageToken;


public class JSONRWFormat extends TokenRWFormat {
	
	private static JSONParser parser = new JSONParser();
	
	private static Map<String, Class<?>> NAME_MAPPING = new HashMap<>();
	
	private static Map<Class<?>, String> TYPE_MAPPING = new HashMap<>();
	
	static
	{
		NAME_MAPPING.put("bool", Boolean.class);
		NAME_MAPPING.put("unicode", String.class);
		NAME_MAPPING.put("float", Float.class);
		NAME_MAPPING.put("int", Integer.class);
		NAME_MAPPING.put("tuple", List.class);
		NAME_MAPPING.put("list", List.class);
		NAME_MAPPING.put("map", Map.class);
		
		TYPE_MAPPING.put(Boolean.class, "bool");
		TYPE_MAPPING.put(String.class, "unicode");
		TYPE_MAPPING.put(Float.class, "float");
		TYPE_MAPPING.put(Double.class, "float");
		TYPE_MAPPING.put(Integer.class, "int");
		TYPE_MAPPING.put(List.class, "list");
		TYPE_MAPPING.put(Map.class, "map");
		
	}
	
	
	public static StorageToken parse(String input)
	{
		try {
			Object rawParseResults =  parser.parse(input);
			return (StorageToken) makeNative(rawParseResults);
		} catch (ParseException e) {
			e.printStackTrace();
			throw new RuntimeException(e);
		}
		
	}
	
	
	public static String serialize(StorageToken data)
	{
		Object processedObject = makeSerializable(data);
		Map<?,?> processedObjectAsMap = (Map<?, ?>) processedObject;
		String result = JSONObject.toJSONString(processedObjectAsMap);
		return result;
				
	}
	
	//remember to check for null values.  Python code didn't have to explicitly do so.
	public static Object makeNative(Object input)
	{
		if(input == null)
			return input;
		if(!(input instanceof Iterable<?>) || input instanceof String)
			return input;
		//if
		return null;
	}
	
	
	private static Object makeSerializable(Object data)
	{
		if(data == null)
			return data;
		
		Class<?> clazz = data.getClass();
		
		if(VALID_ATOMIC_VALUE_TYPES.contains(clazz))
			return data;
		
		if(VALID_SEQUENCE_TYPES.contains(clazz))
		{
			Collection<Object> dataAsCollection = (Collection<Object>)data;
			Map<String, List<?>> sequenceDataDictionary = new HashMap<>();
			String typeName = TYPE_MAPPING.get(List.class);
			
			List<Object> sequenceData = new ArrayList<>();
			
			for(Object o : dataAsCollection)
				sequenceData.add(makeSerializable(o));
			
			sequenceDataDictionary.put(typeName, sequenceData);
			return sequenceDataDictionary;
		}
		if(VALID_MAPPING_TYPES.contains(clazz))
		{
			Map<String, Map<?,?>> mapDataDictionary = new HashMap<>();
			Map<Object, Object> dataAsMap = (Map<Object, Object>) data;
			Map<Object, Object> processedMap = new HashMap<>();			
			
			for(Entry<Object, Object> entry : dataAsMap.entrySet())
			{
				processedMap.put(makeSerializable(entry.getKey()), makeSerializable(entry.getValue()));
			}
			
			mapDataDictionary.put(TYPE_MAPPING.get(Map.class), processedMap);
			
			return mapDataDictionary;
		}
		if(clazz.equals(StorageToken.class))
		{
			StorageToken dataAsStorageToken = (StorageToken)data;
			
			Map<String, Map<String, Object>> processedStorageToken = new HashMap<>();
			Map<String, Object> storageTokenChildren = new HashMap<>();
			
			for(String key : dataAsStorageToken)
			{
				Object value = dataAsStorageToken.getItem(key);
				storageTokenChildren.put(key, makeSerializable(value));
			}
			
			processedStorageToken.put(dataAsStorageToken.getClassId(), storageTokenChildren);
			
			return processedStorageToken;
		}
		
		throw new RuntimeException("Tried to serialize unserializeable object of type " + clazz.toString());
	}

}
