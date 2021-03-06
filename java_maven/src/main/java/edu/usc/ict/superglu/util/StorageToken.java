/**
 * This is the intermediate form of data that allows it to be serialized to multiple formats.
 */
package edu.usc.ict.superglu.util;

import edu.usc.ict.superglu.util.tokenformat.JSONRWFormat;
import edu.usc.ict.superglu.util.tokenformat.JSONStandardRWFormat;
import edu.usc.ict.superglu.util.tokenformat.TokenRWFormat;

import java.util.*;

/**
 * """ An object that stores data in a form that can be serialized """
 *
 * @author auerbach
 */

public class StorageToken extends SuperGlu_Serializable implements Iterable<String> {

    public static final String ID_KEY = "id";
    public static final String CLASS_ID_KEY = "classId";

    public static final Set<String> reservedKeys = new HashSet<>();

    private Map<String, Object> data;

    static {
        reservedKeys.add(CLASS_ID_KEY);
        reservedKeys.add(ID_KEY);
    }

    public StorageToken() {
        super();
        this.data = new HashMap<>();
    }

    public StorageToken(Map<String, Object> data, String id, String classId) {
        this.data = data;

        if (data == null)
            this.data = new HashMap<>();

        if (id != null) {
            this.setId(id);
        } else if (!this.data.containsKey(ID_KEY)) {
            this.data.put(ID_KEY, UUID.randomUUID().toString());
        }

        if (classId != null) {
            this.setClassId(classId);
        }

    }

    // Serialization
    public StorageToken saveToToken() {// Don't add an additional hashmap if
        // it's already a storage token.
        return this;
    }

    // Accessors
    public String getId() {
        return (String) this.data.get(ID_KEY);
    }

    public void setId(String id) {
        this.data.put(ID_KEY, id);
    }

    public String getClassId() {
        return (String) this.data.get(CLASS_ID_KEY);
    }

    public void setClassId(String classId) {
        this.data.put(CLASS_ID_KEY, classId);
    }

    public int getSize() {
        return data.size();
    }

    public boolean contains(String key) {
        return this.data.containsKey(key);
    }

    public Object getItem(String key, boolean hasDefault, Object defalt) {
        if (hasDefault)
            return this.data.getOrDefault(key, defalt);
        else
            return this.data.get(key);
    }

    public void setItem(String key, Object value) {
        this.data.put(key, value);
    }

    public void removeItem(String key) {
        this.data.remove(key);
    }

    public Object getItem(String key) {
        return this.getItem(key, false, null);
    }

    public Iterator<String> iterator() {
        return data.keySet().iterator();
    }

    // Equals and HashCode function overrides

    @Override
    public boolean equals(Object otherObject) {
        if (otherObject == null)
            return false;

        if (!otherObject.getClass().equals(this.getClass()))
            return false;

        StorageToken other = (StorageToken) otherObject;

        return fieldIsEqual(this.data, other.data);
    }

    @Override
    public int hashCode() {
        return this.data.hashCode();
    }

    // Validation
    public boolean isValidKey(Object key) {
        return TokenRWFormat.VALID_KEY_TYPES.contains(key.getClass());
    }

    @Override
    public String toString() {
        return JSONRWFormat.serialize(this);
    }

    public boolean isValidValue(Object value) {
        return TokenRWFormat.VALID_VALUE_TYPES.contains(value.getClass());
    }

    public boolean isValid() {
        Object id = data.get(ID_KEY);

        if (id == null)
            return false;
        if (!id.getClass().equals(int.class) && !id.getClass().equals(String.class))
            return false;

        Object classId = data.get(CLASS_ID_KEY);

        if (classId != null) {
            if (!classId.getClass().equals(String.class))
                return false;
        }

        return true;

    }

}
