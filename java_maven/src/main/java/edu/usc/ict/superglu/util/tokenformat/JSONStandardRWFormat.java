package edu.usc.ict.superglu.util.tokenformat;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

import org.json.simple.DeserializationException;
import org.json.simple.JsonArray;
import org.json.simple.JsonObject;
import org.json.simple.Jsoner;

import edu.usc.ict.superglu.util.StorageToken;

/**
 * This will convert a storageToken into standard JSON
 * 
 * @author auerbach
 *
 */

public class JSONStandardRWFormat extends TokenRWFormat {

	private static Map<String, Class<?>> NAME_MAPPING = new HashMap<>();

	private static Map<Class<?>, String> TYPE_MAPPING = new HashMap<>();

	static {
		NAME_MAPPING.put("bool", Boolean.class);
		NAME_MAPPING.put("unicode", String.class);
		NAME_MAPPING.put("float", Float.class);
		NAME_MAPPING.put("int", Integer.class);
		NAME_MAPPING.put("tuple", List.class);
		NAME_MAPPING.put("long", Long.class);

		TYPE_MAPPING.put(Boolean.class, "bool");
		TYPE_MAPPING.put(String.class, "unicode");
		TYPE_MAPPING.put(Float.class, "float");
		TYPE_MAPPING.put(BigDecimal.class, "float");
		TYPE_MAPPING.put(Double.class, "float");
		TYPE_MAPPING.put(Short.class, "int");
		TYPE_MAPPING.put(Integer.class, "int");
		TYPE_MAPPING.put(Long.class, "long");

	}

	// """ Parse a string into Storage Tokens """
	public static StorageToken parse(String input) {
		try {
			Object rawParseResults = Jsoner.deserialize(input);
			Object nativeObject = makeNative(rawParseResults);

			StorageToken result;
			if (nativeObject instanceof StorageToken)
				result = (StorageToken) nativeObject;
			else if (nativeObject instanceof Map<?, ?>) // TODO: what should the
														// classID be?
				result = new StorageToken((Map<String, Object>) nativeObject, null, null);
			else {
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

	// """ Serialize Storage Token objects into a string form """
	public static String serialize(StorageToken data) {
		Object processedObject = makeSerializable(data);
		Map<?, ?> processedObjectAsMap = (Map<?, ?>) processedObject;
		String result = Jsoner.serialize(processedObjectAsMap);
		return result;
	}

	private static Object makeSerializable(Object data) {
		if (data == null)
			return data;

		Class<?> clazz = data.getClass();

		if (VALID_ATOMIC_VALUE_TYPES.contains(clazz))
			return data;

		if (VALID_SEQUENCE_TYPES.contains(clazz)) {
			Collection<Object> dataAsCollection = (Collection<Object>) data;

			List<Object> sequenceData = new ArrayList<>();

			for (Object o : dataAsCollection)
				sequenceData.add(makeSerializable(o));

			return sequenceData;

		}
		if (VALID_MAPPING_TYPES.contains(clazz)) {
			Map<Object, Object> dataAsMap = (Map<Object, Object>) data;
			Map<Object, Object> processedMap = new HashMap<>();

			for (Entry<Object, Object> entry : dataAsMap.entrySet()) {
				processedMap.put(makeSerializable(entry.getKey()), makeSerializable(entry.getValue()));
			}

			processedMap.put("isMap", true);

			return processedMap;
		}
		if (clazz.equals(StorageToken.class)) {
			StorageToken dataAsStorageToken = (StorageToken) data;

			Map<String, Map<String, Object>> processedStorageToken = new HashMap<>();
			Map<String, Object> storageTokenChildren = new HashMap<>();

			for (String key : dataAsStorageToken) {
				Object value = dataAsStorageToken.getItem(key);
				storageTokenChildren.put(key, makeSerializable(value));
			}

//			if (dataAsStorageToken.getClassId() != null) {
//				processedStorageToken.put(dataAsStorageToken.getClassId(), storageTokenChildren);
//				return processedStorageToken;
	//		} else {
				return storageTokenChildren;
		//	}
		}

		throw new RuntimeException("Tried to serialize unserializeable object of type " + clazz.toString());
	}

	// remember to check for null values. Python code didn't have to explicitly
	// do so.
	private static Object makeNative(Object input) {
		if (isNullOrPrimitive(input))
			return input;
		
		
		if (input instanceof JsonArray) {
			List<Object> result = new ArrayList<>();

			for (Object currentElement : (JsonArray) input) {
				result.add(makeNative(currentElement));
			}

			return result;
		}
		
		else if (input instanceof JsonObject) {
			JsonObject inputAsJsonObject = (JsonObject) input;

			// corner case if object is empty
			if (inputAsJsonObject.isEmpty())
				return new HashMap<String, Object>();

			String datatypeName = inputAsJsonObject.keySet().iterator().next();
			
			Class<?> dataType = NAME_MAPPING.getOrDefault(datatypeName, StorageToken.class);

			

			
			if (!((JsonObject) input).containsKey("isMap")) {// We are deserializing an
														// object

				Map<String, Object> nativizedData = new HashMap<>();
				for (String key : inputAsJsonObject.keySet()) {
					Object value = inputAsJsonObject.get(key);

					if (isNullOrPrimitive(value)) {
						nativizedData.put(key, value);
					} else {

						if (value instanceof JsonObject) {
							Object nativeValue = makeNative(value);
							
							nativizedData.put(key, nativeValue);
							
						} else if (value instanceof JsonArray) {
							
							Object nativizedValue = makeNative(value);
							
							nativizedData.put(key, nativizedValue);
						}
					}
				}

				StorageToken result = new StorageToken(nativizedData, null, (String) nativizedData.get(StorageToken.CLASS_ID_KEY));
				return result;
			}
			 

			else {// We are deserializing a Map

				Map<Object, Object> result = new HashMap<>();

				for (Object key : inputAsJsonObject.keySet()) {
					if(!key.equals("isMap"))
					{
						Object value = inputAsJsonObject.get(key);	

						Object nativizedKey = makeNative(key);
						Object nativizedValue = makeNative(value);
						result.put(nativizedKey, nativizedValue);
					}
				}

				return result;
			}
		}

		

		// should never reach here
		return null;
	}
}
