package edu.usc.ict.superglu.ontology;


import edu.usc.ict.superglu.core.BaseMessage;
import edu.usc.ict.superglu.ontology.mappings.MessageMap;
import edu.usc.ict.superglu.ontology.mappings.MessageTemplate;
import edu.usc.ict.superglu.ontology.mappings.MessageType;
import edu.usc.ict.superglu.util.Pair;
import edu.usc.ict.superglu.util.SerializationConvenience;
import edu.usc.ict.superglu.util.StorageToken;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * this class implements the chaining of various mappings together to allow the
 * conversion of one message type to another without requiring a direct mapping
 * 
 * @author auerbach
 *
 */
public class OntologyBroker {

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
	public OntologyBroker(List<MessageMap> mappings, Map<String, MessageTemplate> defaultTemplates) {
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
	public MessageType buildMessageType(String inMsgType, String inMsgName, float minVersion, float maxVersion) {
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
	 * @param inMsg
	 *            the source messages
	 * @param inMsgType
	 *            source message type
	 * @param targetMsgType
	 *            target message type
	 * @param strict
	 *            ??? speak to Ben about this. I know it's about whether some
	 *            loss can be allowed, but not sure how to implement that
	 * @return
	 */
	public BaseMessage findPathAndConvertMessage(BaseMessage inMsg, MessageType inMsgType, MessageType targetMsgType, Map<String,Object> context,
												 boolean strict) {
		List<MessageMap> path;

		// First check the cache
		Pair<MessageType, MessageType> key = new Pair<MessageType, MessageType>(inMsgType, targetMsgType);

		if (this.mappingCache.containsKey(key))
			path = this.mappingCache.get(key);
		else {// otherwise we'll have to build the path recursively
			List<MessageMap> possiblePath = new ArrayList<>();
			if (findMessageMappingPath(possiblePath, inMsgType, targetMsgType)) {
				path = possiblePath;

				// cache the built path
				this.mappingCache.put(key, path);
			} else
				path = null;
		}

		BaseMessage result = this.convertMessage(inMsg, path, context);

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
	protected boolean findMessageMappingPath(List<MessageMap> currentPath, MessageType currentType,
			MessageType targetType) {
		// If the two message types match, then we've found a path
		if (currentType.getClassId().equals(targetType.getClassId()))
			return true;

		// Otherwise we search through the list of mappings for a possible map
		for (MessageMap possibleNextMap : this.mappings) {
			// We have a map with matching input
			if (possibleNextMap.getInMsgType().getClassId().equals(currentType.getClassId())
					&& possibleNextMap.getInMsgType().getMessageName().equals(currentType.getMessageName())) {

				// Check to make sure we haven't passed through this type
				// already
				boolean alreadyVisited = false;
				for (MessageMap pathIndex : currentPath) {
					if ((currentType.equals(pathIndex.getInMsgType().getClassId()))) {
						alreadyVisited = true;
						break;
					}
				}

				// If we've already passed through this system. Then skip this
				// mapping.
				if (alreadyVisited)
					continue;

				// add the mapping the chain
				currentPath.add(possibleNextMap);

				// Recursive call
				if (findMessageMappingPath(currentPath, possibleNextMap.getOutMsgType(), targetType))
					return true; // We've found a path

				// remember to remove the dead end
				currentPath.remove(currentPath.size() - 1);
			}
		}

		return false;
	}

	protected BaseMessage convertMessage(BaseMessage msg, List<MessageMap> path, Map<String, Object> context) {
		if (path == null)
			return null;

		StorageToken currentForm = (StorageToken) SerializationConvenience.tokenizeObject(msg);

		for (MessageMap currentMap : path) {
			if (currentMap.isValidSourceMsg(currentForm, context)) {
				currentForm = currentMap.convert(currentForm, context);
			}
		}

		BaseMessage result = (BaseMessage) SerializationConvenience.untokenizeObject(currentForm);

		return result;
	}
}
