package edu.usc.ict.superglu.core.config;


import edu.usc.ict.superglu.util.SuperGlu_Serializable;
import edu.usc.ict.superglu.core.blackwhitelist.BlackWhiteListEntry;
import edu.usc.ict.superglu.util.SerializationConvenience;
import edu.usc.ict.superglu.util.StorageToken;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * This class contains everything needed to configure and start up a SuperGLU
 * service
 *
 * @author auerbach
 */

public class GatewayConfiguration extends SuperGlu_Serializable {

    private static final String TYPE_KEY = "type";
    private static final String PARAMS_KEY = "params";
    private static final String NODES_KEY = "nodes";
    private static final String WHITE_LIST_KEY ="whiteList";
    private static final String BLACK_LIST_KEY = "blackList";
    
    public static final String ACTIVEMQ_PARAM_KEY = "activeMQConfig";
    public static final String SOCKETIO_PARAM_KEY = "socketIOConfig";

    private Class<?> type;

    private Map<String, Object> params;

    private List<String> nodes;

    private List<BlackWhiteListEntry> whiteList;
    
    private List<BlackWhiteListEntry> blackList;

    public GatewayConfiguration() {
        super();
        this.type = null;
        this.params = new HashMap<>();
        this.nodes = new ArrayList<>();
        
        this.blackList = new ArrayList<>();
        this.whiteList = new ArrayList<>();
    }


    public GatewayConfiguration(String ID, Class<?> type, Map<String, Object> params, List<String> nodes, List<BlackWhiteListEntry> blackList, List<BlackWhiteListEntry> whiteList) {
        super(ID);
        this.type = type;
        this.params = params;
        this.nodes = nodes;
        this.blackList = blackList;
        this.whiteList = whiteList;
    }

    
    private List<BlackWhiteListEntry> importBlackWhiteList(List<String> listOfStrings)
    {
    	List<BlackWhiteListEntry> result = new ArrayList<>();
    	
    	for(String entryAsString : listOfStrings)
    	{
    		BlackWhiteListEntry entry = new BlackWhiteListEntry(entryAsString);
    		result.add(entry);
    	}
    	
    	return result;
    }
    

    public void initializeFromToken(StorageToken token) {
        super.initializeFromToken(token);


        try {
            this.type = Class.forName((String) token.getItem(TYPE_KEY));
        } catch (ClassNotFoundException e) {
            // TODO: what should I do here?
            this.type = null;
        }

        this.params = (Map<String, Object>) SerializationConvenience.untokenizeObject(token.getItem(PARAMS_KEY, true, new HashMap<>()));
        this.nodes = (List<String>) SerializationConvenience.untokenizeObject(token.getItem(NODES_KEY, true, new ArrayList<>()));

        List<String> blackListAsString = (List<String>)SerializationConvenience.untokenizeObject(token.getItem(BLACK_LIST_KEY, true, new ArrayList<>()));
        this.blackList = importBlackWhiteList(blackListAsString);
        
        List<String> whiteListAsString = (List<String>)SerializationConvenience.untokenizeObject(token.getItem(WHITE_LIST_KEY, true, new ArrayList<>()));
        this.whiteList = importBlackWhiteList(whiteListAsString);
        
        return;
    }
    
    private List<String> exportBlackWhiteList(List<BlackWhiteListEntry> listOfEntries)
    {
    	List<String> result = new ArrayList<>();
    	
    	for(BlackWhiteListEntry entry : listOfEntries)
    	{
    		result.add(entry.toString());
    	}
    	
    	return result;
    }

    public StorageToken saveToToken() {
        StorageToken token = super.saveToToken();

        String classAsString = type.getName();

        token.setItem(TYPE_KEY, classAsString);
        token.setItem(PARAMS_KEY, SerializationConvenience.tokenizeObject(this.params));
        token.setItem(NODES_KEY, SerializationConvenience.tokenizeObject(this.nodes));

        List<String> whiteListAsStrings = exportBlackWhiteList(whiteList);
        token.setItem(WHITE_LIST_KEY, SerializationConvenience.tokenizeObject(whiteListAsStrings));
        
        List<String> blackListAsStrings = exportBlackWhiteList(blackList);
        token.setItem(BLACK_LIST_KEY, SerializationConvenience.tokenizeObject(blackListAsStrings));
        
        return token;
    }

    public Class<?> getType() {
        return type;
    }

    public void setType(Class<?> type) {
        this.type = type;
    }

    public Map<String, Object> getParams() {
        return params;
    }

    public void setParams(Map<String, Object> params) {
        this.params = params;
    }

    public List<String> getNodes() {
        return nodes;
    }

    public void setNodes(List<String> nodes) {
        this.nodes = nodes;
    }


	public List<BlackWhiteListEntry> getWhiteList() {
		return whiteList;
	}


	public void setWhiteList(List<BlackWhiteListEntry> whiteList) {
		this.whiteList = whiteList;
	}


	public List<BlackWhiteListEntry> getBlackList() {
		return blackList;
	}


	public void setBlackList(List<BlackWhiteListEntry> blackList) {
		this.blackList = blackList;
	}
    
    


}
