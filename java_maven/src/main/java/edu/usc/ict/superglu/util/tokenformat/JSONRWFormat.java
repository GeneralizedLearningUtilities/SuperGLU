/**
 * This class handles the serialization of StorageTokens to JSON as well as the deserialization of JSON to StorageToken
 * 
 * @author auerbach
 */
package edu.usc.ict.superglu.util.tokenformat;

import edu.usc.ict.superglu.util.StorageToken;
import org.json.simple.DeserializationException;
import org.json.simple.JsonArray;
import org.json.simple.JsonObject;
import org.json.simple.Jsoner;

import java.math.BigDecimal;
import java.util.*;
import java.util.Map.Entry;


/**
 *  """ JSON Serialization for SuperGLU Format Handler ""
 * @author auerbach
 *
 */
public class JSONRWFormat extends TokenRWFormat {
	
	
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
		NAME_MAPPING.put("long", Long.class);
		
		TYPE_MAPPING.put(Boolean.class, "bool");
		TYPE_MAPPING.put(String.class, "unicode");
		TYPE_MAPPING.put(Float.class, "float");
		TYPE_MAPPING.put(BigDecimal.class, "float");
		TYPE_MAPPING.put(Double.class, "float");
		TYPE_MAPPING.put(Short.class, "int");
		TYPE_MAPPING.put(Integer.class, "int");
		TYPE_MAPPING.put(List.class, "list");
		TYPE_MAPPING.put(Long.class, "long");
		TYPE_MAPPING.put(Map.class, "map");
		
	}
	
	
	public static StorageToken parse(String input)
	{
		try {
			Object rawParseResults =  Jsoner.deserialize(input);
			Object nativeObject = makeNative(rawParseResults);
			
			StorageToken result;
			if(nativeObject instanceof StorageToken)
				result = (StorageToken) nativeObject;
			else if (nativeObject instanceof Map<?,?>) //TODO: what should the classID be?
				result = new StorageToken((Map<String, Object>) nativeObject, null, null);
			else
			{
				Map<String, Object> data = new HashMap<>();
				data.put("data", nativeObject);
				result = new StorageToken(data, null, null);
			}
			return result;
		} catch (DeserializationException e) {
			e.printStackTrace();
			throw new RuntimeException(e);
		}
		
	}
	
	
	public static String serialize(StorageToken data)
	{
		Object processedObject = makeSerializable(data);
		Map<?,?> processedObjectAsMap = (Map<?, ?>) processedObject;
		String result = Jsoner.serialize(processedObjectAsMap);
		return result;
				
	}
	
	
	private static boolean isNullOrPrimitive(Object input)
	{
		if(input == null)
			return true;
		
		Class<?> inputClass = input.getClass();
		
		if(TokenRWFormat.VALID_ATOMIC_VALUE_TYPES.contains(inputClass))
			return true;
		
		if(!(input instanceof Iterable<?> || input instanceof Map<?, ?>))
			return true;
		
		return false;
	}
	
	//remember to check for null values.  Python code didn't have to explicitly do so.
	private static Object makeNative(Object input)
	{
		if(isNullOrPrimitive(input))
			return input;
		
		
		Class<?> inputClass = input.getClass();
		
		if(TokenRWFormat.VALID_ATOMIC_VALUE_TYPES.contains(inputClass))
			return input;
		
		if(!(input instanceof Iterable<?> || input instanceof Map<?, ?>))
			return input;
		
		
		if(input instanceof JsonObject)
		{
			JsonObject inputAsJsonObject = (JsonObject)input;
			
			//corner case if object is empty
			if(inputAsJsonObject.isEmpty())
			    return new HashMap<String, Object>();
			
			
			String datatypeName = inputAsJsonObject.keySet().iterator().next();
			Class<?> dataType = NAME_MAPPING.getOrDefault(datatypeName, StorageToken.class);
			
			if(dataType.equals(StorageToken.class))
			{//We are deserializing an object
				
				Map<String, Object> nativizedData = new HashMap<>();
				boolean primitivesPresent = false;
				for(String key : inputAsJsonObject.keySet())
				{
					Object value = inputAsJsonObject.get(key);
					
					
					if(isNullOrPrimitive(value))
					{
						nativizedData.put(key, value);
						primitivesPresent = true;
					}
					else
					{
					
					    if(value instanceof JsonObject)
					    {
						JsonObject innerData = (JsonObject) value;
						
						for(String innerKey : innerData.keySet())
						{
							Object innerValue = innerData.get(innerKey);
							nativizedData.put(innerKey, makeNative(innerValue));
						}
					    }
					    else if(value instanceof JsonArray)
					    {
						JsonArray innerData = (JsonArray) value;
						
						int index = 0;
						for(Object currentInnerItem :  innerData)
						{
						    nativizedData.put(Integer.toString(index), makeNative(currentInnerItem));
						    ++index;
						}
					    }
					}
				}
				
				if(primitivesPresent)
					return nativizedData;
				
				StorageToken result = new StorageToken(nativizedData,null,null);
				return result;
			}
			else if (dataType.equals(List.class))
			{
				for(String key : inputAsJsonObject.keySet())
				{
					Object value = inputAsJsonObject.get(key);
					return makeNative(value);
				}
			}
			
			else
			{//We are deserializing a Map
				
				Map<Object, Object> result = new HashMap<>();
				
				Map<Object, Object> innerData = inputAsJsonObject.getMap(TYPE_MAPPING.get(Map.class));
				
				
				for(Object key : innerData.keySet())
				{
					Object value = innerData.get(key);
					
					Object nativizedKey = makeNative(key);
					Object nativizedValue = makeNative(value);
					result.put(nativizedKey, nativizedValue);
				}
				
				return result;
			}
		}
		
		if(input instanceof JsonArray)
		{
			List<Object> result = new ArrayList<>();
			
			for(Object currentElement : (JsonArray)input)
			{
				result.add(makeNative(currentElement));
			}
			
			return result;
		}
		
	
		//should never reach here
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
			
			if(dataAsStorageToken.getClassId() != null)
			{
				processedStorageToken.put(dataAsStorageToken.getClassId(), storageTokenChildren);
				return processedStorageToken;
			}
			else
			{
				return storageTokenChildren;
			}
		}
		
		throw new RuntimeException("Tried to serialize unserializeable object of type " + clazz.toString());
	}

}
