package Ontology;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import Core.BaseMessage;
import Ontology.Mappings.MessageMap;
import Ontology.Mappings.MessageTemplate;
import Ontology.Mappings.MessageType;
import Util.Pair;
import Util.SerializationConvenience;
import Util.StorageToken;

/**
 * this class implements the chaining of various mappings together to allow the
 * conversion of one message type to another without requiring a direct mapping
 * 
 * @author auerbach
 *
 */
public class OntologyBroker
{

    /**
     * list of all individual mappings
     */
    protected List<MessageMap> mappings;

    /**
     * cache of previous mapping paths. The algorithm to find mappings can be
     * expensive, so it shouldn't be run if we can help it.
     */
    protected Map<Pair<MessageType, MessageType>, List<MessageMap>> mappingCache;

    /**
     * collection of default values for message types. This should be part of
     * the input data
     */
    protected Map<String, MessageTemplate> defaultTemplates;

    /**
     * constructor for the broker
     * 
     * @param mappings
     */
    public OntologyBroker(List<MessageMap> mappings, Map<String, MessageTemplate> defaultTemplates)
    {
	if (mappings != null)
	    this.mappings = mappings;
	else
	    this.mappings = new ArrayList<>();

	if (defaultTemplates != null)
	    this.defaultTemplates = defaultTemplates;
	else
	    this.defaultTemplates = new HashMap<>();

	this.mappingCache = new HashMap<>();
    }

    /**
     * This function will construct a default template given a message type and
     * name
     */
    public MessageType buildMessageType(String inMsgName, String inMsgType, float minVersion, float maxVersion)
    {
	MessageTemplate template;
	if (this.defaultTemplates.containsKey(inMsgType))
	    template = this.defaultTemplates.get(inMsgType);
	else
	    template = null;

	MessageType result = new MessageType(inMsgName, minVersion, maxVersion, template, inMsgType);
	return result;
    }

    /**
     * this function will attempt to find a path from inMsgType to
     * targetMsgType. If a path is found it will then call the converters in
     * order to produce a message of the targetMsgType
     * 
     * @param inMessage
     *            the source messages
     * @param inMsgType
     *            source message type
     * @param targetMsgType
     *            target message type
     * @param strict
     *            ??? speak to Ben about this.  I know it's about whether some loss can be allowed, but not sure how to implement that
     * @return
     */
    public BaseMessage findPathAndConvertMessage(BaseMessage inMsg, MessageType inMsgType, MessageType targetMsgType, boolean strict)
    {
	List<MessageMap> path;

	// First check the cache
	Pair<MessageType, MessageType> key = new Pair<MessageType, MessageType>(inMsgType, targetMsgType);

	if (this.mappingCache.containsKey(key))
	    path = this.mappingCache.get(key);
	else
	{// otherwise we'll have to build the path recursively
	    List<MessageMap> possiblePath = new ArrayList<>();
	    if (findMessageMappingPath(possiblePath, inMsgType, targetMsgType))
	    {
		path = possiblePath;

		// cache the built path
		this.mappingCache.put(key, path);
	    } else
		path = null;
	}

	BaseMessage result = this.convertMessage(inMsg, path);

	return result;
    }

    /**
     * This is the recursive call to build the mapping path
     * 
     * @param currentPath
     *            the current list of mappings in the partially built path
     * @param currentType
     *            the current end state of the mappings
     * @param targetType
     *            the target type
     * @return
     */
    protected boolean findMessageMappingPath(List<MessageMap> currentPath, MessageType currentType, MessageType targetType)
    {
	// If the two message types match, then we've found a path
	if (currentType.equals(targetType))
	    return true;

	
	
	// Otherwise we search through the list of mappings for a
	for (MessageMap possibleNextMap : this.mappings)
	{
	    //Make sure we don't get into a circular chain of mappings.
	    if (!possibleNextMap.getInMsgType().equals(currentType))
		continue;
	    else
	    {
		// Check to make sure we haven't passed through this type
		// already
		boolean alreadyVisited = false;
		for (MessageMap pathIndex : currentPath)
		{
		    if (currentPath.equals(pathIndex.getOutMsgType()) || (currentType.equals(pathIndex.getInMsgType())))
		    {
			alreadyVisited = true;
			break;
		    }
		}
		
		if(alreadyVisited)
		    continue;
		
		//add the mapping the chain
		currentPath.add(possibleNextMap);
		
		//Recursive call
		if(findMessageMappingPath(currentPath, possibleNextMap.getOutMsgType(), targetType))
		    return true; //We've found a path
		
		//remember to remove the dead end
		currentPath.remove(currentPath.size() - 1);
	    }
	}

	return false;
    }

    protected BaseMessage convertMessage(BaseMessage msg, List<MessageMap> path)
    {
	if (path == null)
	    return null;

	StorageToken currentForm = (StorageToken) SerializationConvenience.tokenizeObject(msg);
	
	for(MessageMap currentMap : path)
	{
	    if(currentMap.isValidSourceMsg(currentForm, null))
	    {
		currentForm = currentMap.convert(currentForm);
		
		if(currentForm == null)
		    return null;//something has gone wrong if this code is triggered.
	    }
	}
	
	
	BaseMessage result = (BaseMessage) SerializationConvenience.untokenizeObject(currentForm);
	
	return result;
    }
}
