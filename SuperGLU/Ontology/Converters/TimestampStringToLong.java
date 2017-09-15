package Ontology.Converters;

import java.text.ParseException;
import java.util.Date;

import Core.Message;
import Util.Serializable;

public class TimestampStringToLong extends Serializable implements DataConverter {

	@Override
	public boolean isApplicable(Object input) {
		if(input instanceof String)
			return true;
		
		return false;
	}

	@Override
	public Object convert(Object input, Object context) {
		String in = (String) context;
		
		try {
			Date date = Message.timestampFormat.parse(in);
			return date.getTime();
		} catch (ParseException e) {
			e.printStackTrace();
		}
		
		return null;
	}

}
