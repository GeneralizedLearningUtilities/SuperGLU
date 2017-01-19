package Ontology;

import Core.Message;
import Core.VHMessage;
import Ontology.Mappings.FieldData;
import Ontology.Mappings.FieldMap;
import Ontology.Mappings.MessageTemplate;
import Ontology.Mappings.MessageTwoWayMap;
import Ontology.Mappings.MessageType;
import Ontology.Mappings.NestedAtomic;
import Util.SerializationConvenience;
import Util.StorageToken;
import java.util.*;

public class OntologyConverter {
	
	private VHMessage vhmsg;
	private StorageToken vhmsgToken;
	private MessageType vhmsgV1;
	private MessageTemplate vhmsgTemp;
	private ArrayList<FieldData> vhmsgArrListDefaultFields;
	private ArrayList<NestedAtomic> vhmsgArrListIndividualFields;
	
	private MessageTwoWayMap VHT_SUPERGLU_Message;
	private ArrayList<FieldMap> VHT_SUPERGLU_Mappings;
	
	private StorageToken superglumsgToken;
	private Message superglumsg;
	private MessageType superglumsgS1;
	private MessageTemplate superglumsgTemp;
	private ArrayList<FieldData> superglusgArrListDefaultFields;
	private ArrayList<NestedAtomic> superglumsgArrListIndividualFields;
	
	public OntologyConverter()
	{
		vhmsg=null;
	}
	public OntologyConverter(VHMessage x)
	{
		vhmsg=x;
	}
	
	void createVHmsgToken()
	{
		vhmsgToken=(StorageToken) SerializationConvenience.tokenizeObject(vhmsg);
	}
	
	void setVHMsgTokenIds()
	{
		vhmsgToken.setId("FIRST_WORD_KEY");
		vhmsgToken.setId("BODY_KEY");		
	}
	
	void setValuestoVHTokenIds()
	{
		if(vhmsg.getFirstWord().equals("ScenarioName"))
		{
		vhmsgToken.setItem("FIRST_WORD_KEY", vhmsg.getFirstWord());
		vhmsgToken.setItem("BODY_KEY", vhmsg.getBody());
		}
	}
	
	void setVHMSG()
	{
		vhmsgV1=new MessageType(vhmsg.getFirstWord(),0.0f,0.0f);
		vhmsgV1.messageTypeTemplate=vhmsgTemp;
	}
	
	void setVHDefaultFields()
	{
		if(vhmsg.getFirstWord().equals("ScenarioName"))
		{
			FieldData vh=new FieldData(null);
			vhmsgArrListDefaultFields.add(vh);
		}
		else if(vhmsg.getFirstWord().equals("commAPI"))
		{
			
		}
	}
	
	void setVHMSGTemplate()
	{
		vhmsgTemp.setData(vhmsgArrListDefaultFields);
	} 
	
	void setIndividualVHMsgFields()
	{
		if(vhmsg.getFirstWord().equals("ScenarioName"))
		{
			NestedAtomic VHT_LabelField=new NestedAtomic();
			VHT_LabelField.setIndices("0");
			NestedAtomic VHT_BodyField=new NestedAtomic();
			VHT_LabelField.setIndices("1");
			vhmsgArrListIndividualFields.add(VHT_LabelField);
			vhmsgArrListIndividualFields.add(VHT_BodyField);
		}
		else if(vhmsg.getFirstWord().equals("commAPI"))
		{
			
		}
	}
	
	void setSuperGLUMsgTokenIds()
	{
		if(vhmsg.getFirstWord().equals("ScenarioName"))
		{
			superglumsgToken.setId("VERB_KEY");
			superglumsgToken.setId("OBJECT_KEY");	
		}
	}
	
	void setValuestoSuperGLUTokenIds()
	{
		if(vhmsg.getFirstWord().equals("ScenarioName"))
		{
			superglumsgToken.setItem("VERB_KEY", vhmsg.getFirstWord());
			superglumsgToken.setItem("OBJECT_KEY", vhmsg.getBody());
		}
	}
	
	void setSUPERGLUDefaultFields()
	{
		if(vhmsg.getFirstWord().equals("ScenarioName"))
		{
			FieldData SuperGLUDefaultSpeechAct=new FieldData("INFORM_ACT");
			FieldData SuperGLUDefaultContextField =new FieldData(" ");
			superglusgArrListDefaultFields.add(SuperGLUDefaultSpeechAct);
			superglusgArrListDefaultFields.add(SuperGLUDefaultContextField);
		}
		else if(vhmsg.getFirstWord().equals("commAPI"))
		{
			
		}
	}
	
	void setIndividualSUPERGLUMsgFields()
	{
		if(vhmsg.getFirstWord().equals("ScenarioName") && superglumsgToken!=null)
		{
			NestedAtomic SuperGLU_ObjectField=new NestedAtomic();
			SuperGLU_ObjectField.setIndices("object");
			NestedAtomic SuperGLU_VerbField=new NestedAtomic();
			SuperGLU_VerbField.setIndices("verb");
			superglumsgArrListIndividualFields.add(SuperGLU_ObjectField);
			superglumsgArrListIndividualFields.add(SuperGLU_VerbField);
		}
		else if(vhmsg.getFirstWord().equals("commAPI") && superglumsgToken!=null)
		{
			
		}
	}
	
	void setSUPERGLUMSGTemplate()
	{
		superglumsgTemp.setData(superglusgArrListDefaultFields);
	} 
	
	void setSUPERGLUMSG()
	{
		if(vhmsg.getFirstWord().equals("ScenarioName") && superglumsgToken!=null)
		{
			superglumsgS1=new MessageType("SUPERGLU-SCENARIO-NAME-CONVERSION",0.0f,0.0f);		
			superglumsgS1.messageTypeTemplate=superglumsgTemp;
		}
		else if(vhmsg.getFirstWord().equals("commAPI") && superglumsgToken!=null)
		{
			
		}
		
	}
	
	void setMappings()
	{
		if(vhmsg.getFirstWord().equals("ScenarioName") && superglumsgToken!=null)
		{
			FieldMap VHT_SuperGLU_TopicVerb_FM=new FieldMap();
			FieldMap VHT_SuperGLU_TopicObject_FM=new FieldMap();
			NestedAtomic a=null,b=null,c=null,d=null;
			for(NestedAtomic x:superglumsgArrListIndividualFields)
			{
				if(x.getIndices().equals("verb"))
				{
					a=x;
					break;
				}
			}
			for(NestedAtomic x:superglumsgArrListIndividualFields)
			{
				if(x.getIndices().equals("object"))
				{
					b=x;
					break;
				}
			}
			for(NestedAtomic x:vhmsgArrListIndividualFields)
			{
				if(x.getIndices().equals("0"))
				{
					c=x;
					break;
				}
			}
			for(NestedAtomic x:vhmsgArrListIndividualFields)
			{
				if(x.getIndices().equals("1"))
				{
					d=x;
					break;
				}
			}
			
			VHT_SuperGLU_TopicVerb_FM.setInField(c);
			VHT_SuperGLU_TopicVerb_FM.setOutField(a);
			VHT_SuperGLU_TopicObject_FM.setInField(d);
			VHT_SuperGLU_TopicObject_FM.setOutField(b);
			
			VHT_SUPERGLU_Mappings.add(VHT_SuperGLU_TopicVerb_FM);
			VHT_SUPERGLU_Mappings.add(VHT_SuperGLU_TopicObject_FM);
			
			
		}
		else if(vhmsg.getFirstWord().equals("commAPI") && superglumsgToken!=null)
		{
			
		}
		
	}
	
	void setFinalVHT_SUPERGLU_Msg()
	{
		if(vhmsg.getFirstWord().equals("ScenarioName") && superglumsgToken!=null)
		{
			
			VHT_SUPERGLU_Message.setOutMsgType(vhmsgV1);
			VHT_SUPERGLU_Message.setFieldMappings(VHT_SUPERGLU_Mappings);
			VHT_SUPERGLU_Message.setOutDefaultMsgType(vhmsgTemp);
			if(superglumsgTemp!=null)
			{
				VHT_SUPERGLU_Message.setInDefaultMsgType(superglumsgTemp);
			}
			else
			{
				VHT_SUPERGLU_Message.setInDefaultMsgType(null);
			}
			if(superglumsgS1!=null)
			{
				VHT_SUPERGLU_Message.setInMsgType(superglumsgS1);
			}
			else
			{
				VHT_SUPERGLU_Message.setInMsgType(null);
			}
			
		}
		else if(vhmsg.getFirstWord().equals("commAPI") && superglumsgToken!=null)
		{
			
		}
	}
	
	Message createSuperGLUMsgObj()
	{
		if(vhmsg.getFirstWord().equals("ScenarioName") && superglumsgToken!=null && superglumsgS1!=null)
		{
			
		}
		return null;
	}
	
	
	
	
	
	

}
