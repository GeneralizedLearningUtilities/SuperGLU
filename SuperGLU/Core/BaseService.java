package Core;

import java.util.function.Predicate;

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
		super(anId, conditions, null);
	}

}
