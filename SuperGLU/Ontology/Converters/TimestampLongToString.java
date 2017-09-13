package Ontology.Converters;

import java.util.Date;

import Core.Message;
import Util.Serializable;

public class TimestampLongToString extends Serializable implements DataConverter {

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
