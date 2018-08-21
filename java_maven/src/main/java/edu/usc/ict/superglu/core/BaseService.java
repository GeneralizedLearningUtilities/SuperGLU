package edu.usc.ict.superglu.core;

import java.util.List;
import java.util.function.Predicate;

import edu.usc.ict.superglu.core.blackwhitelist.BlackWhiteListEntry;

/**
 * Notional class to denote internal services
 * @author auerbach
 *
 */
public class BaseService extends BaseMessagingNode {

	public BaseService()
	{
		this(null, null);
	}
	
	public BaseService(String anId, Predicate<BaseMessage> conditions) {
		super(anId, conditions, null, null, null, null);
	}
	
	public BaseService(String anId, Predicate<BaseMessage> conditions, List<ExternalMessagingHandler> handlers, List<BlackWhiteListEntry> blackList,  List<BlackWhiteListEntry> whiteList)
	{
	    super(anId, conditions, null, handlers,blackList, whiteList);
	}

}
