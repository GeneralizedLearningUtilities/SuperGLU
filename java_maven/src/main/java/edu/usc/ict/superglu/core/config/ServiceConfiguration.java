package edu.usc.ict.superglu.core.config;


import edu.usc.ict.superglu.util.SuperGlu_Serializable;
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

public class ServiceConfiguration extends SuperGlu_Serializable {

    private static final String TYPE_KEY = "type";
    private static final String PARAMS_KEY = "params";
    private static final String NODES_KEY = "nodes";
    public static final String ACTIVEMQ_PARAM_KEY = "activeMQConfig";
    public static final String SOCKETIO_PARAM_KEY = "socketIOConfig";

    private Class<?> type;

    private Map<String, Object> params;

    private List<String> nodes;


    public ServiceConfiguration() {
        super();
        this.type = null;
        this.params = new HashMap<>();
        this.nodes = new ArrayList<>();
    }


    public ServiceConfiguration(String ID, Class<?> type, Map<String, Object> params, List<String> nodes) {
        super(ID);
        this.type = type;
        this.params = params;
        this.nodes = nodes;
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

        return;
    }

    public StorageToken saveToToken() {
        StorageToken token = super.saveToToken();

        String classAsString = type.getName();

        token.setItem(TYPE_KEY, classAsString);
        token.setItem(PARAMS_KEY, SerializationConvenience.tokenizeObject(this.params));
        token.setItem(NODES_KEY, SerializationConvenience.tokenizeObject(this.nodes));

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


}
