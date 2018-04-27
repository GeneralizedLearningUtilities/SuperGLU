package edu.usc.ict.superglu.core;

import java.util.List;
import java.util.function.Predicate;

import edu.usc.ict.superglu.core.blackwhitelist.BlackWhiteListEntry;

/**
 * Notional class to denote internal services
 *
 * @author auerbach
 */
public class BaseService extends BaseMessagingNode {

    private BaseMessagingGateway myGateway;

    public BaseService() {
        this(null, null, null);
    }

    public BaseService(BaseMessagingGateway myGateway, String anId, Predicate<BaseMessage> conditions) {
        super(anId, conditions, null, null, null);
        this.myGateway = myGateway;
    }

    public BaseService(BaseMessagingGateway myGateway, String anId, Predicate<BaseMessage> conditions, List<ExternalMessagingHandler> handlers, List<BlackWhiteListEntry> blackList, List<BlackWhiteListEntry> whiteList) {
        super(anId, conditions, handlers, blackList, whiteList);
        this.myGateway = myGateway;
    }

    public final void sendMessage(BaseMessage msg) {
        log.debug(this.id + " is sending " + this.messageToString(msg));
        String senderID = (String) msg.getContextValue(ORIGINATING_SERVICE_ID_KEY);
        this.myGateway.distributeMessage(msg, senderID);
    }

    public void setGateway(BaseMessagingGateway myGateway) {
        this.myGateway = myGateway;
    }
}
