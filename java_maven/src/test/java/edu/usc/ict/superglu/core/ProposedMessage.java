/**
 * 
 */
package edu.usc.ict.superglu.core;

/**
 * @author rthaker
 *
 */
public class ProposedMessage {

	private String msgId;

	private Message msg;

	private int numberOfRetries;

	private long lastTimeSent;

	public ProposedMessage(String msgId, Message proposedMessage, int numberOfRetries) {
		this.msgId = msgId;
		this.msg = proposedMessage;
		this.numberOfRetries = numberOfRetries;
	}

	public String getMsgId() {
		return msgId;
	}

	public void setMsgId(String msgId) {
		this.msgId = msgId;
	}

	public Message getMsg() {
		return msg;
	}

	public void setMsg(Message msg) {
		this.msg = msg;
	}

	public int getNumberOfRetries() {
		return numberOfRetries;
	}

	public void setNumberOfRetries(int numberOfRetries) {
		this.numberOfRetries = numberOfRetries;
	}

	public long getLastTimeSent() {
		return lastTimeSent;
	}

	public void setLastTimeSent(long lastTimeSent) {
		this.lastTimeSent = lastTimeSent;
	}
}