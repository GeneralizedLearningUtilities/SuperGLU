package edu.usc.ict.superglu.ontology.converters;

import edu.usc.ict.superglu.core.Message;
import edu.usc.ict.superglu.util.SuperGlu_Serializable;

import java.util.Date;

public class TimestampLongToString extends SuperGlu_Serializable implements DataConverter {

	@Override
	public boolean isApplicable(Object input) {
		if(input instanceof Long)
			return true;
		
		return false;
	}

	@Override
	public Object convert(Object input, Object context) {
		long in = (long) input;
		
		Date date = new Date(in);
		
		return Message.timestampFormat.format(date);
	}

}
