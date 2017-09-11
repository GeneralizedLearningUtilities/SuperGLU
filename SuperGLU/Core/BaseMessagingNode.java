package Core;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.function.Consumer;
import java.util.function.Predicate;

import org.apache.log4j.LogManager;
import org.apache.log4j.Logger;
import Util.Pair;
import Util.SerializationConvenience;
import Util.SerializationFormatEnum;

/**
 * """ Base class for messaging """
 * 
 * @author auerbach
 *
 */
public class BaseMessagingNode {

	protected Logger log = LogManager.getLogger(this.getClass());

	protected String id;
	protected Map<String, Pair<Message, Consumer<Message>>> requests;
	protected Predicate<BaseMessage> conditions;
	protected Map<String, BaseMessagingNode> nodes;
	protected List<ExternalMessagingHandler> handlers;
	protected Map<String, Object> context;

	private static boolean CATCH_BAD_MESSAGES = false;

	public static final String ORIGINATING_SERVICE_ID_KEY = "originatingServiceId";
	public static final String SESSION_KEY = "sessionId";

	public BaseMessagingNode(String anId, Predicate<BaseMessage> conditions, Collection<BaseMessagingNode> nodes,
			List<ExternalMessagingHandler> handlers) {
		this.nodes = new HashMap<>();

		if (anId == null)
			this.id = UUID.randomUUID().toString();
		else
			this.id = anId;

		this.requests = new HashMap<>();

		if (conditions != null)
			this.conditions = conditions;

		this.requests = new HashMap<>();

		this.addNodes(nodes);

		if (handlers != null)
			this.handlers = handlers;
		else
			this.handlers = new ArrayList<>();
		
		this.context = new HashMap<>();

	}

	public void receiveMessage(BaseMessage msg) {
		log.info(this.id + " received MSG:" + this.messageToString(msg));
		if (msg instanceof Message)
			this.triggerRequests((Message) msg);

		for (ExternalMessagingHandler handler : this.handlers)
			handler.handleMessage(msg);
	}

	public void sendMessage(BaseMessage msg) {
		log.debug(this.id + " is sending " + this.messageToString(msg));
		String senderID = (String) msg.getContextValue(ORIGINATING_SERVICE_ID_KEY);
		this.distributeMessage(msg, senderID);
	}

	/**
	 * Handle an arriving message from some source. Services other than gateways
	 * should generally not need to change this.
	 * 
	 * @param msg:
	 *            The message arriving
	 * @param senderId:
	 *            The id string for the sender of this message.
	 **/
	public void handleMessage(BaseMessage msg, String senderId) {
		this.receiveMessage(msg);
	}

	/**
	 * """ Pass a message down all interested children (except sender) """
	 * 
	 * @param msg
	 * @param senderId
	 */
	public void distributeMessage(BaseMessage msg, String senderId) {
		this.distributeMessage_impl(this.nodes, msg, senderId);
	}

	/**
	 * Internal implementation of DistributeMessage ""
	 * " Implement passing a message down all interested children (except sender) "
	 * ""
	 * 
	 * @param nodes
	 * @param msg
	 * @param senderId
	 */
	protected void distributeMessage_impl(Map<String, BaseMessagingNode> nodes, BaseMessage msg, String senderId) {
		for (BaseMessagingNode node : nodes.values()) {
			if (node.id != senderId && (node.getMessageConditions() == null || node.getMessageConditions().test(msg)))
				node.receiveMessage(msg);
		}
	}

	/** Transmit the message to another node **/
	protected void transmitMessage(BaseMessagingNode node, BaseMessage msg, String senderId) {
		node.handleMessage(msg, senderId);
	}

	// """ Function to check if this node is interested in this message type """
	public Predicate<BaseMessage> getMessageConditions() {
		return conditions;
	}

	/* handler management */

	public void addHandler(ExternalMessagingHandler handler) {
		this.handlers.add(handler);
	}

	/* Node Management */

	/** Connect nodes to this node **/
	public void addNodes(Collection<BaseMessagingNode> newNodes) {
		if (newNodes != null) {
			for (BaseMessagingNode node : newNodes) {
				addNode(node);
			}
		}
	}

	public void addNode(BaseMessagingNode node) {
		node.onBindToNode(this);
		this.onBindToNode(node);
	}

	public Collection<BaseMessagingNode> getNodes() {
		return this.nodes.values();
	}

	/**
	 * Register the node and signatures of messages that the node is interested
	 * in
	 **/
	public void onBindToNode(BaseMessagingNode node) {
		if (!this.nodes.containsKey(node.getId())) {
			this.nodes.put(node.getId(), node);
		}
	}

	/** This removes this node from a connected node (if any) **/
	public void onUnbindToNode(BaseMessagingNode node) {
		if (this.nodes.containsKey(node.getId())) {
			this.nodes.remove(node.getId());
		}
	}

	protected Collection<Pair<Message, Consumer<Message>>> getRequests() {
		return this.requests.values();
	}

	protected void addRequest(Message msg, Consumer<Message> callback) {
		if (callback != null) {
			Message clone = (Message) msg.clone(false);
			Pair<Message, Consumer<Message>> messageAndCallback = new Pair<Message, Consumer<Message>>(clone, callback);

			this.requests.put(msg.getId(), messageAndCallback);
		}
	}

	protected void makeRequest(Message msg, Consumer<Message> callback) {
		this.addRequest(msg, callback);
		this.sendMessage(msg);
	}

	protected void triggerRequests(Message msg) {
		String convoId = (String) msg.getContextValue(Message.CONTEXT_CONVERSATION_ID_KEY, null);
		if (convoId != null && this.requests.containsKey(convoId)) {
			String key = convoId;
			Pair<Message, Consumer<Message>> value = this.requests.get(key);
			Message oldMsg = value.getFirst();
			Consumer<Message> callback = value.getSecond();
			callback.accept(msg);
			if (!oldMsg.getSpeechAct().equals(SpeechActEnum.REQUEST_WHENEVER_ACT))
				this.requests.remove(key);
		}
	}

	protected BaseMessage createRequestReply(BaseMessage msg) {
		String oldId = msg.getId();
		BaseMessage copy = (BaseMessage) msg.clone(true);
		copy.setContextValue(Message.CONTEXT_CONVERSATION_ID_KEY, oldId);
		return copy;
	}

	// # Pack/Unpack Messages
	public String messageToString(BaseMessage msg) {
		return SerializationConvenience.serializeObject(msg, SerializationFormatEnum.JSON_FORMAT);
	}

	public Message stringToMessage(String msgAsString) {
		Message result = null;
		if (CATCH_BAD_MESSAGES) {

			try {
				result = (Message) SerializationConvenience.nativeizeObject(msgAsString,
						SerializationFormatEnum.JSON_FORMAT);
			} catch (Exception e) {
				log.error("ERROR: could not process message data received.  Received: " + msgAsString);
				log.error("Exception Caught:" + e.toString());
			}
		} else {
			result = (Message) SerializationConvenience.nativeizeObject(msgAsString,
					SerializationFormatEnum.JSON_FORMAT);
		}

		return result;
	}

	public List<String> messagesToStringList(List<Message> msgs) {
		List<String> result = new ArrayList<>();

		for (BaseMessage msg : msgs) {
			result.add(messageToString(msg));
		}

		return result;
	}

	public List<Message> stringListToMessages(List<String> strMsgs) {
		List<Message> result = new ArrayList<>();

		for (String strMsg : strMsgs) {
			Message msg = this.stringToMessage(strMsg);
			result.add(msg);
		}

		return result;
	}

	public String getId() {
		return this.id;
	}

	public Map<String, Object> getContext() {
		return context;
	}

	public void setContext(Map<String, Object> context) {
		this.context = context;
	}
	
	public void addToContext(String key, Object value)
	{
		this.context.put(key, value);
	}

}
