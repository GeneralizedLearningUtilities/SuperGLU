package edu.usc.ict.superglu.core;

import java.util.Arrays;
import java.util.List;

public enum HTTPRequestVerbEnum {

	GET("GET"), PUT("PUT"), POST("POST"), DELETE("DELETE");

	private String value;

	HTTPRequestVerbEnum(final String value) {
		this.value = value;
	}

	public String getValue() {
		return value;
	}

	@Override
	public String toString() {
		return this.getValue();
	}

	public static HTTPRequestVerbEnum getEnum(String value) {
		List<HTTPRequestVerbEnum> list = Arrays.asList(HTTPRequestVerbEnum.values());
		return list.stream().filter(m -> m.value.equals(value)).findAny().orElse(null);
	}

}
