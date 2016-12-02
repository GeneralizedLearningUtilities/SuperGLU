/**
 * This is the base class for all SuperGLU representation objects.  It is responsible for converting itself to and from
 * StorageTokens.
 * 
 * NOTE: all serializables should have a default constructor
 * 
 * @author auerbach
 */
package Util;

import java.util.HashMap;
import java.util.Map;
import java.util.Set;
import java.util.UUID;

import org.reflections.Reflections;


public abstract class Serializable {

	protected String id;
	
	protected static Map<String, Class<? extends Serializable>> CLASS_IDS = new HashMap<>();
	
	
	static
	{
		populateClassIDs(null);
	}
	
	public static void populateClassIDs(String packagePrefix)
	{
		
		Reflections reflections = new Reflections(packagePrefix);
		
		Set<Class<? extends Serializable>> classes = reflections.getSubTypesOf(Serializable.class);
		
		for(Class<? extends Serializable> clazz : classes)
		{
			CLASS_IDS.put(clazz.getSimpleName(), clazz);
		}
	}
	
	
	public Serializable(String id)
	{
		if(id == null)
		{
			this.id = UUID.randomUUID().toString();
		}
		else
		{
			this.id = id;
		}
	}
	
	
	public Serializable()
	{
		this.id = UUID.randomUUID().toString();
	}
	
	
	@Override
	public boolean equals(Object otherObject)
	{
		if(!this.getClass().equals(otherObject.getClass()))
				return false;
		
		Serializable other = (Serializable) otherObject;
		
		if(this.id == other.id)
			return true;
		
		return false;
	}
	
	
	@Override
	public int hashCode()
	{
		return id.hashCode();
	}
	
	
	
	public void updateId(String id)
	{
		if(id == null)
			this.id = UUID.randomUUID().toString();
		else
			this.id = id;
	}
	
	
	public String getClassId()
	{
		return this.getClass().getSimpleName();
	}
	
	
	public void initializeFromToken(StorageToken token)
	{
		this.id = token.getId();
	}
	
	
	public StorageToken saveToToken()
	{
		StorageToken token = new StorageToken(new HashMap<String, Object>(), this.id, this.getClassId());
		return token;
	}
	
	
	public Serializable clone(boolean newId)
	{
		StorageToken token = this.saveToToken();
		Serializable copy = Serializable.createFromToken(token);
		
		if(newId)
			copy.updateId(null);
		
		return copy;
	}
	
	public static Serializable createFromToken(StorageToken token)
	{
		return Serializable.createFromToken(token, false);
	}
	
	
	public static Serializable createFromToken(StorageToken token, boolean errorOnMissing)
	{
		String classId = token.getClassId();
		Class<? extends Serializable> clazz = CLASS_IDS.getOrDefault(classId, null);
		
		boolean classInstantiationFailure = true;
		
		if(clazz != null)
		{
			try {
				Serializable instance = (Serializable) clazz.newInstance();
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
		
		if(classInstantiationFailure)
		{
			if(errorOnMissing)
			{
				throw new RuntimeException(token.getClassId() + " failed to import " + token);
			}
			else
			{
				return token;
			}
		}
		
		//Should never reach this point in the code.
		return token;
	}
}