package edu.usc.ict.superglu.util;

import edu.usc.ict.superglu.util.tokenformat.JSONRWFormat;
import edu.usc.ict.superglu.util.tokenformat.TokenRWFormat;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Ease of access functions for serialization and deserialization
 *
 * @author auerbach
 */

public class SerializationConvenience {


    /**
     * """ Serialize some object(s) Must already be tokenized """
     *
     * @param storageToken
     * @param sFormat
     * @return
     */
    public static String makeSerialized(StorageToken storageToken, SerializationFormatEnum sFormat) {

        if (sFormat == null || sFormat == SerializationFormatEnum.JSON_FORMAT)
            return JSONRWFormat.serialize(storageToken);
        else if (sFormat == SerializationFormatEnum.XML_FORMAT)
            throw new RuntimeException("XML FORMAT NOT YET IMPLEMENTED");
        else if (sFormat == SerializationFormatEnum.PICKLE_FORMAT)
            throw new RuntimeException("PICKLE FORMAT NOT YET IMPLEMENTED");

        else
            return JSONRWFormat.serialize(storageToken);
    }

    /**
     * """ Unserialize some object(s) into tokens """
     *
     * @param input
     * @param sFormat
     * @return
     */
    public static StorageToken makeNative(String input, SerializationFormatEnum sFormat) {
        if (sFormat == null || sFormat == SerializationFormatEnum.JSON_FORMAT)
            return JSONRWFormat.parse(input);
        else if (sFormat == SerializationFormatEnum.XML_FORMAT)
            throw new RuntimeException("XML FORMAT NOT YET IMPLEMENTED");
        else if (sFormat == SerializationFormatEnum.PICKLE_FORMAT)
            throw new RuntimeException("PICKLE FORMAT NOT YET IMPLEMENTED");
        else
            return JSONRWFormat.parse(input);
    }

    /**
     * """ Generic function to tokenize an object """
     *
     * @param object
     * @return
     */
    public static Object tokenizeObject(Object object) {
        if (object == null)
            return null;

        if (object instanceof SuperGlu_Serializable)
            return ((SuperGlu_Serializable) object).saveToToken();
        if (TokenRWFormat.VALID_SEQUENCE_TYPES.contains(object.getClass())) {
            List<Object> result = new ArrayList<>();

            for (Object o : (Iterable<?>) object) {
                result.add(tokenizeObject(o));
            }
            return result;
        }
        if (TokenRWFormat.VALID_MAPPING_TYPES.contains(object.getClass())) {
            Map<Object, Object> result = new HashMap<>();

            Map<?, ?> o = (Map<?, ?>) object;
            for (Object key : o.keySet()) {
                Object value = o.get(key);
                result.put(tokenizeObject(key), tokenizeObject(value));
            }

            return result;
        } else
            return object;
    }

    /**
     * """ Generic function to create an object from a token """
     *
     * @param object
     * @return
     */
    public static Object untokenizeObject(Object object) {
        if (object == null)
            return null;

        if (object instanceof StorageToken)
            return SuperGlu_Serializable.createFromToken((StorageToken) object);
        else if (TokenRWFormat.VALID_SEQUENCE_TYPES.contains(object.getClass())) {
            List<Object> result = new ArrayList<>();
            Iterable<?> objList = (Iterable<?>) object;

            for (Object o : objList) {
                result.add(untokenizeObject(o));
            }

            return result;

        } else if (TokenRWFormat.VALID_MAPPING_TYPES.contains(object.getClass())) {
            Map<Object, Object> result = new HashMap<>();

            Map<?, ?> objMap = (Map<?, ?>) object;

            for (Object key : objMap.keySet()) {
                Object value = objMap.get(key);
                result.put(untokenizeObject(key), untokenizeObject(value));
            }

            return result;
        } else if (object instanceof BigDecimal) {
            BigDecimal bd = (BigDecimal) object;
            try {
                return bd.intValueExact();
            } catch (ArithmeticException e) {
                return bd.floatValue();
            }

        } else
            return object;
    }


    public static String serializeObject(SuperGlu_Serializable obj, SerializationFormatEnum sFormat) {
        StorageToken token = (StorageToken) tokenizeObject(obj);
        return makeSerialized(token, sFormat);
    }


    public static SuperGlu_Serializable nativeizeObject(String input, SerializationFormatEnum sFormat) {
        StorageToken token = makeNative(input, sFormat);
        return (SuperGlu_Serializable) untokenizeObject(token);
    }

}
