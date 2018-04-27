package edu.usc.ict.superglu.core;

import edu.usc.ict.superglu.core.blackwhitelist.BlackWhiteListEntry;
import edu.usc.ict.superglu.util.Pair;
import edu.usc.ict.superglu.util.SerializationConvenience;
import edu.usc.ict.superglu.util.SerializationFormatEnum;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.*;
import java.util.function.Consumer;
import java.util.function.Predicate;

/**
 * """ Base class for messaging """
 *
 * @author auerbach
 */
public abstract class BaseMessagingNode {

    protected Logger log = LoggerFactory.getLogger(this.getClass().getSimpleName());

    protected String id;
    protected Map<String, Pair<Message, Consumer<Message>>> requests;
    protected Predicate<BaseMessage> conditions;

    protected List<ExternalMessagingHandler> handlers;
    protected Map<String, Object> context;

    protected List<BlackWhiteListEntry> blackList;
    protected List<BlackWhiteListEntry> whiteList;

    private static boolean CATCH_BAD_MESSAGES = false;

    public static final String ORIGINATING_SERVICE_ID_KEY = "originatingServiceId";
    public static final String SESSION_KEY = "sessionId";

    protected static final boolean USE_BLACK_WHITE_LIST = true;

    public BaseMessagingNode(String anId, Predicate<BaseMessage> conditions,
                             List<ExternalMessagingHandler> handlers, List<BlackWhiteListEntry> blackList,
                             List<BlackWhiteListEntry> whiteList) {
        if (anId == null)
            this.id = UUID.randomUUID().toString();
        else
            this.id = anId;

        if (conditions != null)
            this.conditions = conditions;

        this.requests = new HashMap<>();

        if (handlers != null)
            this.handlers = handlers;
        else
            this.handlers = new ArrayList<>();

        this.context = new HashMap<>();

        if (blackList != null)
            this.blackList = blackList;
        else
            this.blackList = new ArrayList<>();

        if (whiteList != null)
            this.whiteList = whiteList;
        else
            this.whiteList = new ArrayList<>();
    }

    protected boolean acceptIncomingMessage(BaseMessage msg) {
        boolean result = true;

        if (USE_BLACK_WHITE_LIST) {
            // black list takes priority of white list.
            for (BlackWhiteListEntry entry : this.whiteList) {
                if (entry.evaluateMessage(msg)) {
                    result = true;
                    break;
                }
            }

            for (BlackWhiteListEntry entry : this.blackList) {
                if (entry.evaluateMessage(msg)) {
                    log.info(this.id + " recieved a blacklisted message: "
                            + SerializationConvenience.serializeObject(msg, SerializationFormatEnum.JSON_FORMAT)
                            + "| message will be ignored");
                    result = false;
                    break;
                }
            }
        }

        return result;
    }

    /**
     * Handler for receiving messages.
     * Would be extended by Services through super.receiveMessage()
     * Checks if the msg received is allowed by blacklist/whitelist
     *
     * @param msg incoming message
     * @return true if we should handle the message, false otherwise.
     */
    public boolean receiveMessage(BaseMessage msg) {
        if (!acceptIncomingMessage(msg))
            return false;

        log.info(this.id + " received MSG:" + this.messageToString(msg));

        if (msg instanceof Message)
            this.triggerRequests((Message) msg);

        for (ExternalMessagingHandler handler : this.handlers)
            handler.handleMessage(msg);

        return true;
    }

    protected boolean isMessageOnGatewayBlackList(BaseMessagingNode destination, BaseMessage msg) {
        return false;
    }

    protected boolean isMessageOnGatewayWhiteList(BaseMessagingNode destination, BaseMessage msg) {
        return true;
    }

    /**
     * Transmit the message to another node
     **/
//    protected void transmitMessage(BaseMessagingNode node, BaseMessage msg, String senderId) {
//        node.handleMessage(msg, senderId);
//    }

    // """ Function to check if this node is interested in this message type """
    public Predicate<BaseMessage> getMessageConditions() {
        return conditions;
    }

    /* handler management */

    public void addHandler(ExternalMessagingHandler handler) {
        this.handlers.add(handler);
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

//    protected void makeRequest(Message msg, Consumer<Message> callback) {
//        this.addRequest(msg, callback);
//        this.sendMessage(msg);
//    }

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

    public BaseMessage stringToMessage(String msgAsString) {
        BaseMessage result = null;
        if (CATCH_BAD_MESSAGES) {

            try {
                result = (Message) SerializationConvenience.nativeizeObject(msgAsString,
                        SerializationFormatEnum.JSON_FORMAT);
            } catch (Exception e) {
                log.error("ERROR: could not process message data received.  Received: " + msgAsString);
                log.error("Exception Caught:" + e.toString());
            }
        } else {
            result = (BaseMessage) SerializationConvenience.nativeizeObject(msgAsString,
                    SerializationFormatEnum.JSON_FORMAT);
        }

        return result;
    }

    public List<String> messagesToStringList(List<BaseMessage> msgs) {
        List<String> result = new ArrayList<>();

        for (BaseMessage msg : msgs) {
            result.add(messageToString(msg));
        }

        return result;
    }

    public List<BaseMessage> stringListToMessages(List<String> strMsgs) {
        List<BaseMessage> result = new ArrayList<>();

        for (String strMsg : strMsgs) {
            BaseMessage msg = this.stringToMessage(strMsg);
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

    public void addToContext(String key, Object value) {
        this.context.put(key, value);
    }

}
