package Ontology.Mappings;

/**
 * MessageType  Class
 * The class is used to store the various parameters of the Message like name,min-version and max-version
 * @author tirthmehta
 */
import Util.Serializable;
import Util.SerializationConvenience;
import Util.StorageToken;

public class MessageType extends Serializable
{

    public static final String MESSAGE_TYPE_NAME_KEY = "messageTypeName";
    public static final String MESSAGE_TYPE_CLASS_ID_KEY = "classId";
    public static final String MESSAGE_TYPE_MINVERSION_KEY = "messageTypeMinversion";
    public static final String MESSAGE_TYPE_MAXVERSION_KEY = "messageTypeMaxversion";
    public static final String MESSAGE_TYPE_MESSAGETEMPLATE_KEY = "messageTypeMessagetemplate";

    private String classId;
    private String messageName;
    private float min_Version;
    private float max_Version;
    public MessageTemplate messageTypeTemplate;

    // CONSTRUCTORS
    public MessageType(String name, float minversion, float maxversion, MessageTemplate mtemp, String cl)
    {
	this.messageName = name;
	this.min_Version = minversion;
	this.max_Version = maxversion;
	messageTypeTemplate = mtemp;
	classId = cl;
    }

    public MessageType()
    {
	this.messageName = "";
	this.max_Version = 0.0f;
	this.min_Version = 0.0f;
	this.messageTypeTemplate = null;
	classId = null;
    }

    // GETTER AND SETTER METHODS FOR GETTING AND SETTING THE MULTIPLE VALUES
    // LIKE MESSAGENAME,MIN-VERSION ETC LISTED ABOVE
    public String getMessageName()
    {
	return messageName;
    }

    public void setMessageName(String name)
    {
	messageName = name;
    }

    public float getMinVersion()
    {
	return min_Version;
    }

    public void setMinVersion(float minversion)
    {
	min_Version = minversion;
    }

    public float getMaxVersion()
    {
	return max_Version;
    }

    public void setMaxVersion(float maxversion)
    {

	max_Version = maxversion;
    }

    public MessageTemplate getMessageTemplate()
    {
	if (messageTypeTemplate != null)
	    return messageTypeTemplate;
	else
	    return null;
    }

    public void setClassId(String cl)
    {
	this.classId = cl;
    }

    public String getClassId()
    {
	return classId;
    }

    // Equality Operations
    @Override
    public boolean equals(Object otherObject)
    {
	if (!super.equals(otherObject))
	    return false;

	if (!(otherObject instanceof MessageType))
	    return false;

	MessageType other = (MessageType) otherObject;

	if (!fieldIsEqual(this.messageName, other.messageName))
	    return false;
	if (!fieldIsEqual(this.min_Version, other.min_Version))
	    return false;
	if (!fieldIsEqual(this.max_Version, other.max_Version))
	    return false;
	if (!fieldIsEqual(this.messageTypeTemplate, other.messageTypeTemplate))
	    return false;
	if (!fieldIsEqual(this.classId, other.classId))
	    return false;

	return true;
    }

    @Override
    public int hashCode()
    {
	int result = super.hashCode();
	int arbitraryPrimeNumber = 23;

	if (this.messageName != null)
	    result = result * arbitraryPrimeNumber + this.messageName.hashCode();
	if (this.min_Version != 0.0f)
	{
	    result = result * arbitraryPrimeNumber + Float.hashCode(min_Version);
	}
	if (this.max_Version != 0.0f)
	{
	    result = result * arbitraryPrimeNumber + Float.hashCode(max_Version);
	}
	if (this.messageTypeTemplate != null)
	    result = result * arbitraryPrimeNumber + this.messageTypeTemplate.hashCode();
	if (this.classId != null)
	    result = result * arbitraryPrimeNumber + this.classId.hashCode();

	return result;

    }

    // Serialization/Deserialization
    @Override
    public void initializeFromToken(StorageToken token)
    {
	super.initializeFromToken(token);
	this.messageName = (String) SerializationConvenience.untokenizeObject(token.getItem(MESSAGE_TYPE_NAME_KEY));
	this.min_Version = (float) SerializationConvenience.untokenizeObject(token.getItem(MESSAGE_TYPE_MINVERSION_KEY));
	this.max_Version = (float) SerializationConvenience.untokenizeObject(token.getItem(MESSAGE_TYPE_MAXVERSION_KEY));
	this.messageTypeTemplate = (MessageTemplate) SerializationConvenience.untokenizeObject(token.getItem(MESSAGE_TYPE_MESSAGETEMPLATE_KEY));
	this.classId = (String) SerializationConvenience.untokenizeObject(token.getItem(MESSAGE_TYPE_CLASS_ID_KEY));
    }

    @Override
    public StorageToken saveToToken()
    {
	StorageToken result = super.saveToToken();
	result.setItem(MESSAGE_TYPE_CLASS_ID_KEY, SerializationConvenience.tokenizeObject(this.classId));
	result.setItem(MESSAGE_TYPE_NAME_KEY, SerializationConvenience.tokenizeObject(this.messageName));
	result.setItem(MESSAGE_TYPE_MINVERSION_KEY, SerializationConvenience.tokenizeObject(this.min_Version));
	result.setItem(MESSAGE_TYPE_MAXVERSION_KEY, SerializationConvenience.tokenizeObject(this.max_Version));
	result.setItem(MESSAGE_TYPE_MESSAGETEMPLATE_KEY, SerializationConvenience.tokenizeObject(this.messageTypeTemplate));
	return result;
    }

}
