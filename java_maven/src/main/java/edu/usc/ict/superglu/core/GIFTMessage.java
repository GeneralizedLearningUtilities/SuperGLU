package edu.usc.ict.superglu.core;

import edu.usc.ict.superglu.util.SerializationConvenience;
import edu.usc.ict.superglu.util.StorageToken;

import java.util.Map;

/**
 * generic wrapper for a GIFT message
 *
 * @author auerbach
 */
public class GIFTMessage extends BaseMessage {

    public static final String HEADER_KEY = "header";
    public static final String PAYLOAD_KEY = "payload";

    public static final String MESSAGE_TYPE_KEY = "Message_Type";


    protected String header;

    protected StorageToken payload;


    public GIFTMessage(String id, Map<String, Object> context, String header, StorageToken payload) {
        super(id, context);

        if (header == null)
            this.header = "";
        else
            this.header = header;

        if (payload == null)
            this.payload = new StorageToken();
        else
            this.payload = payload;
    }


    public GIFTMessage() {
        super();
        this.header = "";
        this.payload = new StorageToken();
    }


    public String getHeader() {
        return header;
    }


    public void setHeader(String header) {
        this.header = header;
    }


    public StorageToken getPayload() {
        return payload;
    }


    public void setPayload(StorageToken payload) {
        this.payload = payload;
    }

    
    public String getDestinationQueueName()
    {
    	String result = (String) this.payload.getItem("DestinationQueueName", true,  ActiveMQTopicMessagingGateway.pedagogicalQueueName);
    	return result;
    }

    @Override
    public boolean equals(Object otherObject) {
        if (!super.equals(otherObject))
            return false;

        if (!(otherObject instanceof GIFTMessage))
            return false;

        GIFTMessage other = (GIFTMessage) otherObject;

        if (!fieldIsEqual(this.header, other.header))
            return false;

        if (!fieldIsEqual(this.payload, other.payload))
            return false;

        return true;
    }


    @Override
    /**
     *
     *   Generate a hash value for the message.
     */
    public int hashCode() {
        int result = super.hashCode();
        int arbitraryPrimeNumber = 23;

        if (this.context != null)
            result = result * arbitraryPrimeNumber + this.header.hashCode();
        if (this.payload != null)
            result = result * arbitraryPrimeNumber + this.payload.hashCode();

        return result;
    }


    //Serialization/Deserialization
    @Override
    public StorageToken saveToToken() {
        StorageToken result = super.saveToToken();
        result.setItem(HEADER_KEY, SerializationConvenience.tokenizeObject(this.header));
        result.setItem(PAYLOAD_KEY, this.payload);

        return result;
    }


    @Override
    public void initializeFromToken(StorageToken token) {
        super.initializeFromToken(token);
        this.header = (String) SerializationConvenience.untokenizeObject(token.getItem(HEADER_KEY, true, ""));
        this.payload = (StorageToken) token.getItem(PAYLOAD_KEY, true, new StorageToken());
    }
}
