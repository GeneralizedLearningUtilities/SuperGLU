package Core;

/**
 * This interface is designed to allow external classes to handle messages from the Messaging Gateway
 * @author auerbach
 *
 */

public interface ExternalMessagingHandler
{

    /**
     * the function that will be called by the messaging gateway.
     * @param msg
     */
    public void handleMessage(BaseMessage msg);
    
}
