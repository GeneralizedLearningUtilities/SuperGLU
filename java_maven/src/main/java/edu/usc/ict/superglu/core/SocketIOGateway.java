package edu.usc.ict.superglu.core;

import com.corundumstudio.socketio.*;
import com.corundumstudio.socketio.listener.DataListener;

import edu.usc.ict.superglu.core.blackwhitelist.BlackWhiteListEntry;
import edu.usc.ict.superglu.core.config.GatewayBlackWhiteListConfiguration;
import edu.usc.ict.superglu.core.config.ServiceConfiguration;
import edu.usc.ict.superglu.util.SerializationConvenience;
import edu.usc.ict.superglu.util.SerializationFormatEnum;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.function.Predicate;

/**
 * This class will send and receive messages over SocketIO. It's basically a
 * bridge between the SuperGLU infrastructure and the SocketIO framework.
 * 
 * @author auerbach
 *
 */

public class SocketIOGateway extends MessagingGateway implements DataListener<Map<String, String>> {

	/**
	 * This is the object that handles the communication over the socket.
	 */
	private SocketIOServer socketIO;

	/**
	 * store the clients in association with the persistent session id.
	 * 
	 */
	private ConcurrentHashMap<String, List<String>> clients;

	public static final String MESSAGES_KEY = "message";
	public static final String DATA_KEY = "data";
	public static final String MESSAGES_NAMESPACE = "/messaging";
	public static final String SID_KEY = "sid";

	public SocketIOGateway() {
		super();
		this.socketIO = new SocketIOServer(new Configuration());
		this.clients = new ConcurrentHashMap<>();
	}

	public SocketIOGateway(ServiceConfiguration serviceConfig) {
		super(serviceConfig.getId(), null, null, null, null, serviceConfig.getBlackList(), serviceConfig.getWhiteList(), (GatewayBlackWhiteListConfiguration) serviceConfig.getParams().getOrDefault(GATEWAY_BLACKLIST_KEY, null));
		log.debug("starting http messaging gateway");
		try
		{
		int socketIOPort = 5333;// Have a default port to fall back on.
		if (serviceConfig.getParams().containsKey(ServiceConfiguration.SOCKETIO_PARAM_KEY))
			socketIOPort = (int) serviceConfig.getParams().get(ServiceConfiguration.SOCKETIO_PARAM_KEY);
		Configuration socketConfig = new Configuration();
		socketConfig.setPort(socketIOPort);
		SocketIOServer socketIO = new SocketIOServer(socketConfig);

		log.debug("created SocketIOServer object");
		
		this.socketIO = socketIO;
		this.clients = new ConcurrentHashMap<>();

		log.debug("about to start socketIO");
		
		this.socketIO.start();
		
		log.debug("starting socketIO");

		this.socketIO.addNamespace(MESSAGES_NAMESPACE);

		this.socketIO.getNamespace(MESSAGES_NAMESPACE).addEventListener(MESSAGES_KEY, Map.class, (DataListener) this);
		
		log.debug("http messaging gateway started");
		}
		catch (Exception e)
		{
			log.error("caught exception", e);
			throw e;
		}
	}

	public SocketIOGateway(String anId, Map<String, Object> scope, Collection<BaseMessagingNode> nodes,
						   Predicate<BaseMessage> conditions, List<ExternalMessagingHandler> handlers, SocketIOServer socketIO, List<BlackWhiteListEntry> blackList, List<BlackWhiteListEntry> whiteList) {
		super(anId, scope, nodes, conditions, handlers, blackList, whiteList, new GatewayBlackWhiteListConfiguration());
		this.socketIO = socketIO;
		this.clients = new ConcurrentHashMap<>();

		this.socketIO.start();

		this.socketIO.addNamespace(MESSAGES_NAMESPACE);

		this.socketIO.getNamespace(MESSAGES_NAMESPACE).addEventListener(MESSAGES_KEY, Map.class, (DataListener) this);
	}

	/*
	 * @Override public void receiveMessage(BaseMessage msg) {
	 * super.receiveMessage(msg); log.log(Level.INFO, "message received");
	 * this.sendWebsocketMesage(msg); log.log(Level.INFO,
	 * "Distributing message: " + SerializationConvenience.serializeObject(msg,
	 * SerializationFormatEnum.JSON_FORMAT)); this.distributeMessage(msg,
	 * this.getId()); log.log(Level.INFO, "message distributed"); }
	 * 
	 * @Override public void sendMessage(BaseMessage msg) {
	 * super.sendMessage(msg); this.sendWebsocketMesage(msg); }
	 * 
	 */

	@Override
	public void distributeMessage(BaseMessage msg, String senderId) {
		this.addContextDataToMsg(msg);
		this.sendWebsocketMesage(msg);
		super.distributeMessage(msg, senderId);
	}

	@Override
	public void disconnect() {
		super.disconnect();
		this.socketIO.stop();
	}

	public void sendWebsocketMesage(BaseMessage msg) {
		
		if(this.IsMessageOnGatewayExternalBlackList(msg))
			return;
		
		String msgAsString = SerializationConvenience.serializeObject(msg, SerializationFormatEnum.JSON_FORMAT);

		Map<String, String> data = new HashMap<>();

		String sessionId = (String) msg.getContextValue(SESSION_KEY, null);

		if (sessionId != null) {
			data.put(DATA_KEY, msgAsString);
			data.put(SESSION_KEY, sessionId);

			BroadcastOperations broadcastOperations = this.socketIO.getRoomOperations(sessionId);
			broadcastOperations.sendEvent(MESSAGES_KEY, data);
		} else {
			log.warn("Message does not contain session id.  Cannot send: " + msgAsString);
		}

	}

	@Override
	public void onData(SocketIOClient client, Map<String, String> data, AckRequest ackSender) throws Exception {
		log.debug("data received from socket: " + data.toString());

		String sid = client.getSessionId().toString();

		if (data.containsKey(DATA_KEY)) {
			String sessionId = data.getOrDefault(SESSION_KEY, null);
			if (SESSION_KEY != null) {
				client.joinRoom(sessionId);

				if (!this.clients.containsKey(sessionId))
					this.clients.put(sessionId, new ArrayList<>());

				List<String> sids = new ArrayList<>();
				sids.add(sid);
				this.clients.put(sessionId, sids);

				String msgAsString = data.get(DATA_KEY);
				BaseMessage msg = (BaseMessage) SerializationConvenience.nativeizeObject(msgAsString,
						SerializationFormatEnum.JSON_FORMAT);

				msg.setContextValue(SID_KEY, sid);

				this.distributeMessage(msg, this.getId());
			}
		} else {
			log.warn("GATEWAY DID NOT UNDERSTAND: " + data.toString());
		}
	}

}
