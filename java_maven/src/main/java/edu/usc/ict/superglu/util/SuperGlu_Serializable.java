package edu.usc.ict.superglu.util;

import java.util.HashMap;
import java.util.Map;
import java.util.Set;
import java.util.UUID;

import edu.usc.ict.superglu.ontology.mappings.NestedAtomic;
import org.reflections.Reflections;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * """ A serializable object, that can be saved to token and opened from token
 * """
 *
 * @author auerbach
 */
public abstract class SuperGlu_Serializable {

    protected Logger logger = LoggerFactory.getLogger(this.getClass().getSimpleName());

    /**
     * A unique ID (GUID) for the message, for later reference.
     */
    protected String id;

    protected static Map<String, Class<? extends SuperGlu_Serializable>> CLASS_IDS = new HashMap<>();

    static {
        populateClassIDs("edu.usc.ict.superglu");
    }

    public static void populateClassIDs(String packagePrefix) {
 
        Reflections reflections = new Reflections(packagePrefix);

        Set<Class<? extends SuperGlu_Serializable>> classes = reflections.getSubTypesOf(SuperGlu_Serializable.class);

        for (Class<? extends SuperGlu_Serializable> clazz : classes) {
            CLASS_IDS.put(clazz.getSimpleName(), clazz);
        }
    }

    public SuperGlu_Serializable(String id) {
        if (id == null) {
            this.id = UUID.randomUUID().toString();
        } else {
            this.id = id;
        }
    }

    public SuperGlu_Serializable() {
        this.id = UUID.randomUUID().toString();
    }

    protected boolean fieldIsEqual(Object thisField, Object otherField) {
        if (thisField == null && otherField == null)
            return true;

        // We now know that at least one of the fields in not null
        if (thisField == null)
            return false;

        if (otherField == null)
            return false;

        // We now know that that both fields are non-null
        return thisField.equals(otherField);
    }

    @Override
    public boolean equals(Object otherObject) {
        if (otherObject == null)
            return false;

        if (!this.getClass().equals(otherObject.getClass()))
            return false;

        SuperGlu_Serializable other = (SuperGlu_Serializable) otherObject;

        // TODO:ask Ben about checking id field during
        if (fieldIsEqual(this.id, other.id))
            return true;

        return false;
    }

    @Override
    public int hashCode() {
        return id.hashCode();
    }

    public String getId() {
        return this.id;
    }

    public void updateId(String id) {
        if (id == null)
            this.id = UUID.randomUUID().toString();
        else
            this.id = id;
    }

    public String getClassId() {
        return this.getClass().getSimpleName();
    }

    public void initializeFromToken(StorageToken token) {
        this.id = token.getId();
    }

    public StorageToken saveToToken() {
        StorageToken token = new StorageToken(new HashMap<String, Object>(), this.id, this.getClassId());
        return token;
    }

    public SuperGlu_Serializable clone(boolean newId) {
        StorageToken token = this.saveToToken();

        System.out.println("Token saved : ");
        System.out.println(token.toString());
        SuperGlu_Serializable copy = SuperGlu_Serializable.createFromToken(token);

        System.out.println("Copy : ");
        System.out.println(copy instanceof NestedAtomic);
        System.out.println(copy instanceof StorageToken);

        if (newId){
            copy.updateId(null);
        }
        return copy;
    }

    public static SuperGlu_Serializable createFromToken(StorageToken token) {
        return SuperGlu_Serializable.createFromToken(token, false);
    }

    /**
     * """ Create a serializable instance from an arbitrary storage token
     *
     * @param token:         Storage token
     * @param errorOnMissing
     * @return
     */
    public static SuperGlu_Serializable createFromToken(StorageToken token, boolean errorOnMissing) {
        String classId = token.getClassId();
        Class<? extends SuperGlu_Serializable> clazz = CLASS_IDS.getOrDefault(classId, null);

        boolean classInstantiationFailure = true;

        if (clazz != null) {
            try {
                SuperGlu_Serializable instance = (SuperGlu_Serializable) clazz.newInstance();
                instance.initializeFromToken(token);
                classInstantiationFailure = false;
                return instance;
            } catch (InstantiationException e) {
                e.printStackTrace();
                classInstantiationFailure = true;
            } catch (IllegalAccessException e) {
                e.printStackTrace();
                classInstantiationFailure = true;
            }
        }

        if (classInstantiationFailure) {
            if (errorOnMissing) {
                throw new RuntimeException(token.getClassId() + " failed to import " + token);
            } else {
                return token;
            }
        }

        // Should never reach this point in the code.
        return token;
    }
}
