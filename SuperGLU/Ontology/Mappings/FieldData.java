package Ontology.Mappings;

import Util.Serializable;
import Util.StorageToken;

public class FieldData extends Serializable{
	
	private String field_data;
	
	
	@Override
	public boolean equals(Object otherObject) {
		// TODO Auto-generated method stub
		return super.equals(otherObject);
	}

	@Override
	public int hashCode() {
		// TODO Auto-generated method stub
		return super.hashCode();
	}

	@Override
	public String getId() {
		// TODO Auto-generated method stub
		return super.getId();
	}

	@Override
	public void updateId(String id) {
		// TODO Auto-generated method stub
		super.updateId(id);
	}

	@Override
	public String getClassId() {
		// TODO Auto-generated method stub
		return super.getClassId();
	}

	@Override
	public void initializeFromToken(StorageToken token) {
		// TODO Auto-generated method stub
		super.initializeFromToken(token);
	}

	@Override
	public StorageToken saveToToken() {
		// TODO Auto-generated method stub
		return super.saveToToken();
	}

	@Override
	public Serializable clone(boolean newId) {
		// TODO Auto-generated method stub
		return super.clone(newId);
	}

	@Override
	protected Object clone() throws CloneNotSupportedException {
		// TODO Auto-generated method stub
		return super.clone();
	}

	@Override
	protected void finalize() throws Throwable {
		// TODO Auto-generated method stub
		super.finalize();
	}

	@Override
	public String toString() {
		// TODO Auto-generated method stub
		return super.toString();
	}

	
	
	
	
	//my methods
	public FieldData(String data)
	{
		this.field_data=data;
	}
	
		
	public FieldData()
	{
		this.field_data="";
	}
	
	
	public String getFieldData()
	{
		return field_data;
	}
	
	public void setFieldData(String data)
	{
		field_data=data;
	}

}
