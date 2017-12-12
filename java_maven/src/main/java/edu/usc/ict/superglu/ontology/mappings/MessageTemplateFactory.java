package edu.usc.ict.superglu.ontology.mappings;

import java.util.ArrayList;
import java.util.List;

import edu.usc.ict.superglu.util.Pair;
import edu.usc.ict.superglu.util.StorageToken;

/**
 * This class is responsible for converting a storage token into a message template.
 * 
 * It will go through all the fields and construct the appropriate FieldData object
 * for it.  If a field is a storage token, then it will also recursively go through it as well. 
 * @author auerbach
 *
 */

public class MessageTemplateFactory {

	
	public static MessageTemplate createMessageTemplate(StorageToken token, List<String> topLevelExcludedFields, List<String> globalExcludedFields)
	{
		List<Pair<Class<?>, String>> path = new ArrayList<>();
		List<Pair<FieldData, Object>> templateData = new ArrayList<>();

		populateFields(path, token, templateData, topLevelExcludedFields, globalExcludedFields);

		MessageTemplate template = new MessageTemplate(templateData);

		return template;
	}
	
	
	private static void populateFields(List<Pair<Class<?>,String>> path, StorageToken currentStorageToken, List<Pair<FieldData, Object>> templateData, List<String> topLevelExcludedFields, List<String> globalExcludedFields)
	{
		for (String currentField : currentStorageToken) {
			Object value = currentStorageToken.getItem(currentField);

			if (value instanceof StorageToken) {
				path.add(new Pair<Class<?>, String>(StorageToken.class, currentField));
				populateFields(path, (StorageToken) value, templateData, new ArrayList<>(), globalExcludedFields);
				path.remove(path.size() - 1);
			} else {
				if (globalExcludedFields.contains(currentField) || topLevelExcludedFields.contains(currentField))
					continue;// skip to the next field

				List<Pair<Class<?>, String>> copyOfPath = new ArrayList<>();
				copyOfPath.addAll(path);//use a copy of the path instead of the one that the function will be modifiying.
				copyOfPath.add(new Pair<Class<?>, String>(value.getClass(), currentField));
				NestedAtomic field = new NestedAtomic(copyOfPath);

				templateData.add(new Pair<FieldData, Object>(field, value));
			}
		}
	}
	
}
