// Requires Util\Zet, SKO_Architecture\Messaging
if (typeof window === "undefined") {
    var window = this;
}

(function(namespace, undefined) {

var CATCH_BAD_MESSAGES = false,
    SESSION_ID_KEY = 'sessionId';

Zet.declare('BaseMessagingNode', {
    // Base class for messaging gateways
    superclass : Serialization.Serializable,
    defineBody : function(that){
        // Public Properties

        that.construct = function construct(id, gateway){
            that.inherited(construct, [id]);
            if (typeof gateway === "undefined") {gateway = null;}
            that._gateway = null;
            if (gateway != null){
                that.bindToGateway(gateway);
            }
            that._requests = {};
		};
        
        that.sendMessage = function sendMessage(msg){
			//console.log(that._id + " sent MSG: "+ that.messageToString(msg));
            if (that._gateway != null){
                //console.log("SEND MSG (" + that.getId() + "):" + Serialization.makeSerialized(Serialization.tokenizeObject(msg)));
                that._gateway.dispatchMessage(msg, that.getId());
            }
        };
        
        that.receiveMessage = function receiveMessage(msg){
            // Processing to handle a received message
			//console.log(that._id + " received MSG: "+ that.messageToString(msg));
            that._triggerRequests(msg);
        };
        
        that.bindToGateway = function bindToGateway(gateway){
            that.unbindToGateway();
            that._gateway = gateway;
            that._gateway.register(that);
        };
        
        that.unbindToGateway = function unbindToGateway(){
            if (that._gateway != null){
                that._gateway.unregister(that);
            }
        };
        
        that.getMessageConditions = function getMessageConditions(){
            /** Function to check if this node is interested in this message type */
            return function(){return true;};
        };
        
        // Request Management 
        that._getRequests = function _getRequests(){
            var key, reqs;
            reqs = [];
            for (key in that._requests){
                reqs.push(that._requests[key][0]);
            }
        };
        
        //@TODO: Add a timeout for requests, with a timeout callback (maxWait, timeoutCallback)
        that._addRequest = function _addRequest(msg, callback){
            if (callback != null){
                that._requests[msg.getId()] = [msg.clone(), callback];
            }
        };
        
        that._makeRequest = function _makeRequest(msg, callback){
            that._addRequest(msg, callback);
            that.sendMessage(msg);
            //console.log("SENT REQUEST:" + Serialization.makeSerialized(Serialization.tokenizeObject(msg)));
        };
        
        that._triggerRequests = function _triggerRequests(msg){
            var key, convoId, oldMsg, callback;
            //console.log("Heard REPLY:" + Serialization.makeSerialized(Serialization.tokenizeObject(msg)));
            convoId = msg.getContextValue(Messaging.CONTEXT_CONVERSATION_ID_KEY, null);
            //console.log("CONVO ID: " + convoId);
            //console.log(that._requests);
            if (convoId != null){
                //@TODO: This is a dict, so can check directly?
                for (key in that._requests){
                    if (key === convoId){
                        oldMsg = that._requests[key][0];
                        callback = that._requests[key][1];
                        callback(msg, oldMsg);
                        // Remove from the requests, unless asked for a permanent feed
                        if (oldMsg.getSpeechAct() !== Messaging.REQUEST_WHENEVER_ACT){
                            delete that._requests[key];
                        }
                    }
                }
            }
        };
		
		// Pack/Unpack Messages
        that.messageToString = function messageToString(msg){
            return Serialization.makeSerialized(Serialization.tokenizeObject(msg));
        };
        
        that.stringToMessage = function stringToMessage(msg){
            if (CATCH_BAD_MESSAGES){
                try {
                    msg = Serialization.untokenizeObject(Serialization.makeNative(msg));
                } catch (err) {
                    console.log("ERROR: Could not process message data received.  Received:");
                    console.log(msg);
                    msg = undefined;
                }
            } else {
                msg = Serialization.untokenizeObject(Serialization.makeNative(msg));
            }
            return msg;
        };
    }
});
 
        
Zet.declare('MessagingGateway', {
    // Base class for messaging gateways
    superclass : BaseMessagingNode,
    defineBody : function(that){
        // Public Properties
        
        that.construct = function construct(id, nodes, gateway){
            // Should check to make sure parent gateway is not a child node also
            that.inherited(construct, [id, gateway]);
            that._nodes = {};
            that.addNodes(nodes);
		};
           
        // Receive Messages
        that.receiveMessage = function receiveMessage(msg){
            /** When gateway receives a message, it distributes it to child nodes **/
            //console.log(" RECIEVE MSG (" + that.getId() + "):" + Serialization.makeSerialized(Serialization.tokenizeObject(msg)));
			that.inherited(receiveMessage, [msg]);
            that.distributeMessage(msg, null);
        };
        
        // Relay Messages
        that.dispatchMessage = function dispatchMessage(msg, senderId){
            /** Send a message from a child node to parent and sibling nodes **/
            //console.log(" DISPATCH MSG (" + that.getId() + "):" + Serialization.makeSerialized(Serialization.tokenizeObject(msg)));
            that.sendMessage(msg);
            that._distributeMessage(that._nodes, msg, senderId);
        };
        
        that.distributeMessage = function distributeMessage(msg, senderId){
            /** Pass a message down all interested children (except sender) **/
            that._distributeMessage(that._nodes, msg, senderId);
        };
        
        that._distributeMessage = function _distributeMessage(nodes, msg, senderId){
            var nodeId, node, condition;
            for(nodeId in nodes){
                condition = nodes[nodeId][0];
                node = nodes[nodeId][1];
                if (nodeId !== senderId && (condition == null || condition(msg))){
                    node.receiveMessage(msg);
                }
            }
        };

        // Manage Child Nodes
        that.addNodes = function addNodes(nodes){
            var i;
            if (nodes == null) {nodes = [];}
            for (i=0; i<nodes.length; i++){
                nodes[i].bindToGateway(that);
            }
        };
        
        that.register = function register(node){
            /** Register the signatures of messages that the node is interested in **/
            that._nodes[node.getId()] = [node.getMessageConditions(), node];
        };
        
        that.unregister = function unregister(node){
            /** Take actions to remove the node from the list **/
            if (node.getId() in that._nodes){
                delete that._nodes[node.getId()];
            }
        };
        
        that.addContextDataToMsg = function addContextDataToMsg(msg){
        };
    }
});


Zet.declare('PostMessageGatewayStub', {
    // Messaging Gateway Node Stub for Cross-Domain Page Communication
    superclass : BaseMessagingNode,
    defineBody : function(that){
        // Private Properties
        var ANY_ORIGIN = '*';
        
        // Public Properties
        
        that.construct = function construct(id, gateway, origin, element){
            that.inherited(construct, [id, gateway]);
            if (origin == null) {origin = ANY_ORIGIN;}
            if (element == null) {element = parent;}
            if (element === window){
                element = null;
            }
            that._origin = origin;
            that._element = element;
		};
        
        that.getOrigin = function getOrigin(){
            return that._origin;
        };
        
        that.getElement = function getElement(){
            return that._element;
        };
		
		that.register = function register(node){
            /** Register the signatures of messages that the node is interested in **/
        };
        
        that.unregister = function unregister(node){
            /** Take actions to remove the node from the list **/
        };
    }
});
        
        
Zet.declare('PostMessageGateway', {
    /** Messaging Gateway for Cross-Domain Page Communication 
        Note: This should not directly take other PostMessageGateways as nodes.
        PostMessageGatewayStub objects must be used instead.
    **/
    superclass : MessagingGateway,
    defineBody : function(that){
        // Private Properties
        var ANY_ORIGIN = '*';
        
        // Public Properties
        
        that.construct = function construct(id, nodes, gateway, origin){
			/**
			@param origin: The origin for this PostMessage window. 
			**/
            if (origin == null) {origin = ANY_ORIGIN;}
            that._origin = origin;
            // Get these ready before adding nodes in base constructor
            that._postNodes = {};
            that._validOrigins = {};
            that._anyOriginValid = true;
            // Construct
            that.inherited(construct, [id, nodes, gateway]);
            that.validatePostingHierarchy();
			if (window){
				that.bindToWindow(window);
			}
		};

        that.getOrigin = function getOrigin(){
            return that._origin;
        };
        
        that.getStub = function getStub(){
            return PostMessageGatewayStub(that._id, that._gateway, that._origin);
        };
        
        that.validatePostingHierarchy = function validatePostingHierarchy(){
            /** Check that the posting hierarchy is valid.
                Valid neighbors can have no PostMessageGateway nodes,
                and only the parent OR the children can be of the
                PostMessageGatewayStub class
            **/
            var isGatewayPost, key; 
            if (PostMessageGateway.isInstance(that._gateway)){
                throw TypeError("Error: Cannot directly connect PostMessageGateways");
            }
            isGatewayPost = PostMessageGatewayStub.isInstance(that._gateway);
            for (key in that._nodes){
                if (PostMessageGateway.isInstance(that._nodes[key])){
                    throw TypeError("Error: Cannot directly connect PostMessageGateways");
                }
                if (isGatewayPost && PostMessageGatewayStub.isInstance(that._nodes[key])){
                    throw TypeError("Error: Both gateway and child nodes for PostMessageGateway were PostMessageGatewayStubs.");
                }
            }
        };
        
        that.bindToGateway = function bindToGateway(gateway){
            that.inherited(bindToGateway, [gateway]);
            that._onAttachNode(gateway);
        };
        
        that.unbindToGateway = function unbindToGateway(){
            that._onDetachNode(that._gateway);
            that.inherited(unbindToGateway);
        };
        
        that._onAttachNode = function _onAttachNode(node){
            // Should check if already attached and raise error
            if (PostMessageGatewayStub.isInstance(node)){
                if (that._validOrigins[node.getOrigin()] != null){
                    that._validOrigins[node.getOrigin()] = 1;
                } else {
                    that._validOrigins[node.getOrigin()] += 1;
                }
                if (node.getOrigin() === ANY_ORIGIN){
                    that._anyOriginValid = true;
                }
                that._postNodes[node.getId()] = node;
            }
        };
        
        that._onDetachNode = function _onDetachNode(node){
            if (PostMessageGatewayStub.isInstance(node)){
                that._validOrigins[node.getOrigin()] += -1;

                if (that._validOrigins[node.getOrigin()] === 0){
                    delete that._validOrigins[node.getOrigin()];
                    if (node.getOrigin() === ANY_ORIGIN){
                        that._anyOriginValid = false;
                    }
                }
                delete that._postNodes[node.getId()];
            }
        };
        
        that.register = function register(node){
            /** Register the signatures of messages that the node is interested in **/
            that.inherited(register, [node]);
            that._onAttachNode(node);
            that.validatePostingHierarchy();
        };
        
        that.unregister = function unregister(node){
            /** Take actions to remove the node from the list **/
            if ((node.getId()) in that._nodes){
                delete that._nodes[node.getId()];
                that._onDetachNode(node);
            }
        };
        
        that.bindToWindow = function bindToWindow(aWindow){
            var eventMethod, eventer, messageEvent;
            eventMethod = aWindow.addEventListener ? "addEventListener" : "attachEvent";
            eventer = aWindow[eventMethod];
            messageEvent = eventMethod == "attachEvent" ? "onmessage" : "message";
            eventer(messageEvent, function(event) {that.receivePostMessage(event);});
        };
        
        // Messaging
        that.sendMessage = function sendMessage(msg){
            if (that._gateway != null){
                if (PostMessageGatewayStub.isInstance(that._gateway)){
                    that.sendPostMessage(msg);
                } else {
                    that._gateway.dispatchMessage(msg, that.getId());
                }
            }
        };
        
        that._distributeMessage = function _distributeMessage(nodes, msg, senderId){
            /** Pass a message to all interested children (except sender) **/
            var nodeId, node, condition;
            for(nodeId in nodes){
                condition = nodes[nodeId][0];
                node = nodes[nodeId][1];
                if (nodeId !== senderId && (condition == null || condition(msg))){
                     if (PostMessageGatewayStub.isInstance(node)){
                        that.distributePostMessage(msg, node);
                     } else {
                        node.receiveMessage(msg);
                    }
                }
            }
        };
        
        // HTML5 PostMessage Commands
        that.sendPostMessage = function sendPostMessage(msg){
            var postMsg, element;
            postMsg = JSON.stringify({'senderId' : that.getId(), 'msg' : that.messageToString(msg)});
			//console.log(that._id + " POSTED UP " + that.messageToString(msg));
            element = that._gateway.getElement();
            if (element != null){
                element.postMessage(postMsg, that._gateway.getOrigin());
            }
        };
        
        that.distributePostMessage = function distributePostMessage(msg, node){
			//console.log(that._id + " DISTRIBUTED POST " + that.messageToString(msg));
            var element = node.getElement();
            if (element != null){
                element.postMessage(JSON.stringify({'msg' : that.messageToString(msg)}), node.getOrigin());
            }
        };
        
        that.receivePostMessage = function receivePostMessage(event){
            var senderId, message;
			//console.log(that._id + " RECEIVED POST " + JSON.parse(event.data));
            if (that.isValidOrigin(event.origin)){
                try{
                    message = JSON.parse(event.data);
                } catch (err){
                    console.log("Post Message Gateway did not understand: " + event.data);
                    return;
                }
                if (typeof message.senderId === "undefined"){
                    // Handle as a message from a parent gateway
                    message = that.stringToMessage(message.msg);
                    if (Messaging.Message.isInstance(message)){
                        that.distributeMessage(message, null);
                    }
                } else {
                    // Handle as a message from a child node
                    senderId = message.senderId;
                    message = that.stringToMessage(message.msg);
                    if (Messaging.Message.isInstance(message)){
                        that.dispatchMessage(message, senderId);
                    }
                }
            }
        };
        
        that.isValidOrigin = function isValidOrigin(url){
            if (that._anyOriginValid){
                return true;
            } else {
                return url in that._validOrigins;
            }
        };
    }
});
      
      
Zet.declare('HTTPMessagingGateway', {
    // Base class for messaging gateways
	// This uses socket.io.js and UUID.js
    superclass : MessagingGateway,
    defineBody : function(that){
        // Public Properties
        // Events: connecting, connect, disconnect, connect_failed, error, 
        //         message, anything, reconnecting, reconnect, reconnect_failed
        // Listed At: github.com/LearnBoost/socket.io/wiki/Exposed-events
		var MESSAGING_NAMESPACE = '/messaging';
        
        that.construct = function construct(id, nodes, url, sessionId){
            that.inherited(construct, [id, nodes, null]);      // Classifier not used here, as messages are exact responses.
            if (typeof url === "undefined") {url = null;}
			if (typeof sessionId === "undefined") {sessionId = UUID.genV4().toString();}
            that._url = url;
			that._socket = io.connect(that._url + MESSAGING_NAMESPACE);
			that._isConnected = false;
			that._sessionId = sessionId;
			that._socket.on('message', that.receiveWebsocketMessage);
		};
        
        that.bindToGateway = function bindToGateway(gateway){
            throw new Error("Cannot bind a HTTPMessagingGateway to a parent gateway.  It is a stub for the server gateway.");
        };
        
        that.bindToConnectEvent = function bindToConnectEvent(funct){
            that._socket.on('connect', funct);
        };
        
        that.bindToCloseEvent = function bindToCloseEvent(funct){
            that._socket.on('disconnect', funct);
        };
        
        that.addSessionData = function addSessionData(msg){
            msg.setContextValue(SESSION_ID_KEY, that._sessionId);
            return msg;
        };
        
        that.sendMessage = function sendMessage(msg){
            if (that._url != null){
                msg = that.addSessionData(msg);
                that.sendWebsocketMessage(msg);
            }
        };
        
        that.sendWebsocketMessage = function sendWebsocketMessage(msg){
            msg = that.messageToString(msg);
            that._socket.emit('message', {data: msg, sessionId : that._sessionId});
        };
        
		that.receiveWebsocketMessage = function receiveWebsocketMessage(msg){
			var sessionId;
			sessionId = msg.sessionId;
			msg = msg.data;
            msg = that.stringToMessage(msg);
            // console.log("GOT THIS:" + sessionId);
            // console.log("Real Sess: " + that._sessionId);
			if (Messaging.Message.isInstance(msg) && (sessionId == null || sessionId == that._sessionId)){
				that.distributeMessage(msg);
            }
        };
    }
});      
    

Zet.declare('BaseService', {
    // Base class for messaging gateways
    superclass : BaseMessagingNode,
    defineBody : function(that){
        // Public Properties
    }
});

Zet.declare('TestService', {
    // Base class for messaging gateways
    superclass : BaseService,
    defineBody : function(that){
        // Public Properties
		that.receiveMessage = function receiveMessage(msg){
			console.log("TEST SERVICE <" + that.getId() + "> GOT: \n" + that.messageToString(msg));
            that.inherited(receiveMessage, [msg]);
        };
		
		that.sendTestString = function sendTestString(aStr){
			console.log("Test Service is Sending: " + aStr);
            that.sendMessage(Messaging.Message("TestService", "Sent Test", "To Server", aStr));
        };
		
		that.sendTestMessage = function sendTestMessage(actor, verb, object, result, speechAct, context){
            if (context == null){context={};}
			that.sendMessage(Messaging.Message(actor, verb, object, result, speechAct));
		};
        
        that.sendTestRequest = function sendTestRequest(callback, actor, verb, object, result, speechAct, context){
            if (context == null){context={};}
            that._makeRequest(Messaging.Message(actor, verb, object, result, speechAct, context),
                              callback);
        };
	}
});

namespace.SESSION_ID_KEY = SESSION_ID_KEY;
namespace.BaseService = BaseService;
namespace.MessagingGateway = MessagingGateway;
namespace.PostMessageGatewayStub = PostMessageGatewayStub;
namespace.PostMessageGateway = PostMessageGateway;
namespace.HTTPMessagingGateway = HTTPMessagingGateway;
namespace.TestService = TestService;

})(window.Client_Messaging_Gateway = window.Client_Messaging_Gateway || {});