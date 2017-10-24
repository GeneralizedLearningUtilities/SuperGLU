package edu.usc.ict.superglu.core;

import edu.usc.ict.superglu.core.blackwhitelist.BlackWhiteListEntry;
import edu.usc.ict.superglu.core.config.GatewayBlackWhiteListConfiguration;
import edu.usc.ict.superglu.ontology.OntologyBroker;
import edu.usc.ict.superglu.ontology.mappings.MessageMapFactory;
import edu.usc.ict.superglu.ontology.mappings.MessageType;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Predicate;

/**
 * Messaging Node specifically designed to act as a entry/exit point between
 * systems.
 *
 * @author auerbach
 */

public class MessagingGateway extends BaseMessagingNode {

	public static final String GATEWAY_BLACKLIST_KEY = "gatewayBlackList";

	private Map<String, Object> scope;

	private OntologyBroker ontologyBroker;

	private Map<String, List<BlackWhiteListEntry>> gatewayBlackList;

	public MessagingGateway() {// Default constructor for ease of access
		this(null, null, null, null, null, null, null, null);
		ontologyBroker = new OntologyBroker(MessageMapFactory.buildMessageMaps(),
				MessageMapFactory.buildDefaultMessageTemplates());
	}

	public MessagingGateway(String anId, Map<String, Object> scope, Collection<BaseMessagingNode> nodes,
			Predicate<BaseMessage> conditions, List<ExternalMessagingHandler> handlers,
			List<BlackWhiteListEntry> blackList, List<BlackWhiteListEntry> whiteList,
			GatewayBlackWhiteListConfiguration gatewayBlackList) {
		super(anId, conditions, nodes, handlers, blackList, whiteList);
		if (scope == null)
			this.scope = new HashMap<>();
		else
			this.scope = scope;

		this.scope.put(ORIGINATING_SERVICE_ID_KEY, this.id);

		ontologyBroker = new OntologyBroker(MessageMapFactory.buildMessageMaps(),
				MessageMapFactory.buildDefaultMessageTemplates());
		
		buildGatewayBlackWhiteList(gatewayBlackList);
	}
	
	
	private void buildGatewayBlackWhiteList(GatewayBlackWhiteListConfiguration config) {
		if(config == null)
			return;
		
		this.gatewayBlackList = new HashMap<>();

		for (String destination : config.getKeys()) {
			List<String> entriesAsString = config.getMessageList(destination);

			List<BlackWhiteListEntry> entries = new ArrayList<>();

			for (String entryAsString : entriesAsString) {
				BlackWhiteListEntry entry = new BlackWhiteListEntry(entryAsString);
				entries.add(entry);
			}

			this.gatewayBlackList.put(destination, entries);
		}
	}
	
	

	/**
	 * override this function to place disconnection code in here
	 **/
	public void disconnect() {

	}

	/**
	 * """ When gateway receives a message, it distributes it to child nodes """
	 */
	@Override
	public void handleMessage(BaseMessage msg, String senderId) {
		super.receiveMessage(msg);
		this.distributeMessage(msg, senderId);
	}

	/**
	 * """ Send a message from a child node to parent and sibling nodes """
	 *
	 * @param msg
	 *            Message to be sent
	 * @param senderId
	 *            Sender ID
	 */
	@Override
	public void distributeMessage(BaseMessage msg, String senderId) {
		this.addContextDataToMsg(msg);
		super.distributeMessage(msg, senderId);
	}

	/**
	 * """ Register the signatures of messages that the node is interested in "
	 * ""
	 *
	 * @param node
	 */
	public void register(BaseMessagingNode node) {
		this.nodes.put(node.id, node);
	}

	/**
	 * """ Take actions to remove the node from the list """
	 *
	 * @param node
	 */
	public void unregister(BaseMessagingNode node) {
		if (this.nodes.containsKey(node.id))
			this.nodes.remove(node.id);
	}

	/**
	 * """ Add extra context to the message, if not present """
	 *
	 * @param msg
	 */
	public void addContextDataToMsg(BaseMessage msg) {
		for (String key : this.scope.keySet()) {
			if (!msg.hasContextValue(key))
				msg.setContextValue(key, this.scope.get(key));
		}
	}

	/**
	 * This function will process a non-SuperGLU message through the ontology
	 * converter
	 */
	public BaseMessage convertMessages(BaseMessage incomingMessage, Class<?> destinationMessageType) {
		String incomingMessageTypeAsString = incomingMessage.getClassId();

		String messageName = "";

		if (incomingMessage instanceof Message)
			messageName = ((Message) incomingMessage).getVerb();
		else if (incomingMessage instanceof VHMessage)
			messageName = ((VHMessage) incomingMessage).getFirstWord();
		else if (incomingMessage instanceof GIFTMessage)
			messageName = ((GIFTMessage) incomingMessage).getHeader();

		MessageType inMsgType = ontologyBroker.buildMessageType(incomingMessageTypeAsString, messageName, 1.0f, 1.0f);
		MessageType outMsgType = ontologyBroker.buildMessageType(destinationMessageType.getSimpleName(), "", 1.0f,
				1.0f);

		BaseMessage result = ontologyBroker.findPathAndConvertMessage(incomingMessage, inMsgType, outMsgType,
				this.context, true);

		return result;
	}
}
