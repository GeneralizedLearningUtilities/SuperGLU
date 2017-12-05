package edu.usc.ict.superglu.ontology.converters;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;

import edu.usc.ict.superglu.util.SuperGlu_Serializable;
/**
 * This converter will remove any html tags from a string 
 * @author auerbach
 *
 */
public class RemoveHTMLTags extends SuperGlu_Serializable implements DataConverter {

	@Override
	public boolean isApplicable(Object input) {
		if(input instanceof String)
			return true;
		else
			return false;
	}

	@Override
	public Object convert(Object input, Object context) {
		String inputAsString = (String)context;
		
		Document doc = Jsoup.parse(inputAsString);
		
		String result = inputAsString;
		
		if(doc.hasText())
			result = doc.text();
		
		return result;
	}

}
