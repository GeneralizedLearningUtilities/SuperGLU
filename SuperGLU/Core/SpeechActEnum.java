package Core;

public enum SpeechActEnum {
	INFORM_ACT ("Inform"),
	REQUEST_ACT ("Request");
	
    private String value;

    SpeechActEnum(final String value) {
        this.value = value;
    }

    public String getValue() {
        return value;
    }

    @Override
    public String toString() {
        return this.getValue();
    }
}
