package edu.usc.ict.superglu.ontology.converters;


import edu.usc.ict.superglu.core.Message;
import edu.usc.ict.superglu.util.SuperGlu_Serializable;

import java.text.ParseException;
import java.util.Date;

public class TimestampStringToLong extends SuperGlu_Serializable implements DataConverter {

    @Override
    public boolean isApplicable(Object input) {
        if (input instanceof String)
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
