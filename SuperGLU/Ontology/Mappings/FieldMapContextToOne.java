package Ontology.Mappings;

import java.util.Map;

import Util.Serializable;
import Util.StorageToken;

/**
 * This map will map a value from the global context to a field in the destination message
 * @author auerbach
 *
 */

//TODO: Add serialization code equals and hashcode

public class FieldMapContextToOne extends Serializable implements FieldMap {
	
	protected String contextKey;
	protected FieldData outField;

	public FieldMapContextToOne() {
		this.contextKey = "";
		this.outField = null;
	}
	
	
	public FieldMapContextToOne(String contextKey, FieldData outField)
	{
		this.contextKey = contextKey;
		this.outField = outField;
	}
	
	
	@Override
	public StorageToken applyMapping(StorageToken sourceMessage, StorageToken destinationMessage,
			Map<String, Object> context) {
		Object contextData = context.get(contextKey);
		this.outField.storeData(destinationMessage, contextData);
		return destinationMessage;
	}

	@Override
	public boolean doesMappingApply(StorageToken sourceMessage, Map<String, Object> context) {
		return true;
	}


	public String getContextKey() {
		return contextKey;
	}


	public void setContextKey(String contextKey) {
		this.contextKey = contextKey;
	}


	public FieldData getOutField() {
		return outField;
	}


	public void setOutField(FieldData outField) {
		this.outField = outField;
	}
	
	
	

}
