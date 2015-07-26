//////////////////////////////////////////////////////
// File Name: Serialization.js
//
// Description: 
//   Serialization Package
//   -----------------------------------
//   This package is intended to allow serializing and unserializing
//   between JavaScript objects and various serial/string representations (e.g., JSON, XML).
//   The following objects are included:
//     * Serializable: Base class for serializable objects, needed for custom serialization
//     * StorageToken: Intermediate representation of a serializable object
//     * TokenRWFormats: Serializes and recovers storage tokens and primatives to specific formats (e.g., JSON)
//
/////////////////////////////////////////////////////////

// Requires UUID,js and Zet.js
if (typeof window === "undefined") {
    var window = this;
}


// Module Declaration
(function (Serialization, undefined) {

    var MAP_STRING = "map",
        LIST_STRING = 'list';
    
    var NAME_KEY = 'name';

	// Utility functions
	var updateObjProps = function(targetObj, sourceObj){
		for (var key in sourceObj){
			targetObj[key] = sourceObj[key];
		}
	};

	// Format Constants
	var JSON_FORMAT = 'json',
		XML_FORMAT = 'xml',
		VALID_SERIAL_FORMATS = [JSON_FORMAT, XML_FORMAT];
	
    // Base classes for serializable objects
    //---------------------------------------------

    // Class Serializable
    // A serializable object, that can be saved to token and opened from token
    Zet.declare('Serializable', {
        superclass : null,
        defineBody : function(that){
			// Constructor Function
            
            that.construct = function construct(id){
            /** Constructor for serializable
            *   @param id (optional): GUID for this object.  If none given, a V4 random GUID is used.
            */
                if (id == null) {
                    that._id = UUID.genV4().toString();
                } else {
                    that._id = id;
                }
                
                //A factory mapping that is used when unpacking serialized objects. 
                //if (that.CLASS_ID){
                //    _addFactoryClass(that.className, that.constructor);
                //} else {
                //    throw new TypeError("Serializable class did not have a class id.");
                //}
            };
            // Public Functions 
            that.eq = function eq(other){
				return ((that.getClassId() == other.getClassId()) && (that.getId() == other.getId()));
            };

            that.ne = function ne(other){
                return !(that.eq(other));
            };

            that.getId = function getId(){
                return that._id;
            };
            
            that.updateId = function updateId(id){
                if (id === undefined) {
                    that._id = UUID.genV4().toString();
                } else {
                    that._id = id;
                }
            };

            that.getClassId = function getClassId(){
                return that.className;
            };

            that.initializeFromToken = function initializeFromToken(token, context){
            /** Initialize serializable from token.
                @param context (optional): Mutable context for the loading process. Defaults to null. 
            */
				that._id = token.getId();
            };

            that.saveToToken = function saveToToken(){
				var token = StorageToken(that.getId(), that.getClassId());
                return token;
            };
            
            that.saveToSerialized = function saveToSerialized(){
                return makeSerialized(that.saveToToken());
            };
            
            that.clone = function clone(){
                var s = makeSerialized(that.saveToToken());
                return untokenizeObject(makeNative(s));
            };
        }
    });

    Zet.declare('NamedSerializable' , {
        superclass : Serializable,
        defineBody : function(that){
			// Constructor Function
            that.NAME_KEY = NAME_KEY;
            
            that.construct = function construct(id, name){
                if (name == null) { name=null;}
                that.inherited(construct, [id]);
                that._name = name;
            };
            
            that.getName = function getName(){
                return that._name;
            };
            
            that.setName = function setName(name){
                if (name == null){
                    name = null; 
                } else if (name instanceof String || typeof name === 'string'){
                    that._name = name;
                } else {
                    throw new Error("Set name failed, was not a string.");
                }
            };
            
            that.eq = function eq(other){
                return (that.inherited(eq, [other]) && (that._name === other._name));
            };
            
            that.initializeFromToken = function initializeFromToken(token, context){
                that.inherited(initializeFromToken, [token, context]);
                that._name = untokenizeObject(token.getitem(that.NAME_KEY, true, null), context);
            };
            
            that.saveToToken = function saveToToken(){
                var token = that.inherited(saveToToken);
                if (that._name != null){
                    token.setitem(that.NAME_KEY, tokenizeObject(that._name));
                }
                return token;
            };
        }
    });
    
    // Class StorageToken
    // An object that stores data in a form that can be serialized
    Zet.declare('StorageToken', {
        superclass : null,
        defineBody : function(that){
            // -- Class fields
            that.ID_KEY = 'id';
            that.CLASS_ID_KEY = 'classId';
            
            // Constructor
            that.construct = function construct(id, classId, data) {
            /** Create a storage token, which can be directly serialized into a string
                @param id (optional): A GUID for the storage token.  If none given, uses a V4 random GUID.
                @param classId (optional): Id for the class that this StorageToken should create.  Defaults to null.
                @param data (optional): Starting data for the token.  Either a map {} for an array of map pairs [[key, val]].
            */
                var i;
                that._data = {};
                if (data !== undefined) {
                    //we are assuming that the data will either already
                    //be in a dictionary form ({key: value, key2: value2, ...}) 
                    //or is in a sequence form ([[key, value], [key2, value2], ...])
                    if (data instanceof Array){ //[[key, value], [key2, value2], ...]
                        for (i in data){
                            if ((data[i] instanceof Array) && (data[i].length == 2)){
                                  that._data[data[i][0]] = data[i][1];
                            } else {
                                throw new TypeError("Input array doesn't follow the format of [[key, value], [key2, value2], ...]");
                            }
                        }
                    } else {// {key: value, key2: value2, ...}
                        that._data = data;
                    }
                }else {
                    that._data = {};
                }                
                if (id !== undefined){
                    that.setId(id);
                } else if ((that.getId() === undefined)){
                    that.setId(UUID.genV4().toString());
                }                
                if (classId !== undefined) {
                    that.setClassId(classId);
                }
            };
        
            // -- Instance methods
            that.getId = function getId(){
                return that._data[that.ID_KEY];
            };

            that.setId = function setId(value){
                that._data[that.ID_KEY] = value;
            };

            that.getClassId = function getClassId(){
                return that._data[that.CLASS_ID_KEY];
            };

            that.setClassId = function setClassId(value){
                that._data[that.CLASS_ID_KEY] = value;
            };
            
            // Convenience Accessor for Named Serializables
            that.getName = function getName(){
                if (NAME_KEY in that._data){
                    return that._data[NAME_KEY];
                } else {
                    return null;
                }
            };

            that.setName = function setName(value){
                that._data[NAME_KEY] = value;
            };

            // -- ##Generic Accessors
            that.len = function len(){
                return that._data.length;
            };

            that.contains = function contains(key){
                return key in that._data;
            };

            that.getitem = function getitem(key, hasDefault, defaults){
            /** Get an item from the data dictionary
                @param key: Key for the item
                @param hasDefault (optional): If True, give a default value.  Else, raise an error if key not found.
                @param defaults (optional): The optional value for this item.
            */
                if (!(key in that._data) && (hasDefault)){
                    return defaults;
                }else {
                    return that._data[key];
                }
            };

            that.setitem = function setitem(key, value){
                that._data[key] = value;
            };

            that.delitem = function delitem(key){
                delete that._data[key];
            };

            that.__iterator__ = function __iterator__(){
                var keys = Object.keys(that._data).sort();
                var keys_pos = 0;
                return {
                    next: function(){
                        if (keys_pos >= keys.length){
                            throw StopIteration;
                        }
                        return keys[keys_pos++];
                    }
                };
            };

            that.keys = function keys(){
                var k, aKeys;
                aKeys = [];
                for (k in that._data){
                    aKeys.push(k);
                }
                return aKeys;
            };

            // -- ##Comparison
            that.eq = function eq(other){
                return (typeof(that) == typeof(other)) && (that._data == other._data);
            };

            that.ne = function ne(other){
                return !(that.eq(other));
            };

            // -- ##Validation
            that.isValidKey = function isValidKey(key){
                return typeof(key) in that.VALID_KEY_TYPES;
            };

            that.isValidValue = function isValidValue(value){
                return typeof(value) in that.VALID_VALUE_TYPES;
            };

            that.isValid = function isValid(){
                var idKey;
                var classIdKey;
                
                //Check that ID is valid
                if ((that._data[that.ID_KEY] == null) ||
                    ((typeof(that._data[that.ID_KEY]) !== 'string') &&
                     (typeof(that._data[that.ID_KEY]) !== 'number'))) {
                  return false;
                }
                //Check that class name is valid
                if ((that._data[that.CLASS_ID_KEY] == null) ||
                    (typeof(that._data[that.CLASS_ID_KEY]) !== 'string')) {
                  return false;
                }
                // Check that the name (if it exists) is valid
                if ((that._data[NAME_KEY] != null) && 
                    (typeof(that._data[NAME_KEY]) !== 'string')) {
                  return false;
                }
                return true;      
            };
        }
    });

    //-------------------------------------------
    // Packing and Unpacking from Serial Formats
    //-------------------------------------------
    // Generic RW Format
    Zet.declare('TokenRWFormat', {
        superclass : null,
        defineBody : function(that){
            // Public Class Properties
            
            // Valid Types in Storage Token
            that.VALID_KEY_TYPES = {'string': true};
            that.VALID_ATOMIC_VALUE_TYPES = {'number': true, 'string': true, 'boolean': true, 'undefined': true};
            that.VALID_SEQUENCE_VALUE_TYPES = {'list': true, 'tuple' : true};
            that.VALID_MAPPING_VALUE_TYPES = {'map': true};
            that.VALID_VALUE_TYPES = {};

            // Setup for Class Properties
            updateObjProps(that.VALID_VALUE_TYPES, that.VALID_ATOMIC_VALUE_TYPES);
            updateObjProps(that.VALID_VALUE_TYPES, that.VALID_SEQUENCE_VALUE_TYPES);
            updateObjProps(that.VALID_VALUE_TYPES, that.VALID_MAPPING_VALUE_TYPES);
            that.VALID_VALUE_TYPES.StorageToken = true;
            
            // Constructor method
            that.construct = function construct(){};
            
            // Public methods
            that.parse = function parse(string) {
                // Parse a string into javascript objects
                throw new Error("NotImplementedError");
            };

            that.serialize = function serialize(data) {
                // Serialize javascript objects into a string form
                throw new Error("NotImplementedError");
            };
        }
    });


    //JSON Formatting: Use JSONEncoder/JSONDecoder
    Zet.declare('JSONRWFormat', {
        superclass : TokenRWFormat,
        defineBody : function(that){
            
            // Constructor method
            that.construct = function construct(){};
            
            // Public methods
            that.parse = function parse(String) {//Parse a JSON string into javascript objects
                var decoded = JSON.parse(String);
                return that.makeNative(decoded);
            };

            that.serialize = function serialize(data) {//Serialize javascript objects into a JSON string form
                var serializable = that.makeSerializable(data);
                return JSON.stringify(serializable);
            };

            that.makeSerializable = function makeSerializable(x){
                var i, key, keys, rt, temp, xType;
                xType = typeof(x);
                rt = null;
				if ((xType in that.VALID_ATOMIC_VALUE_TYPES) || (x === null)){// Primitive variables
                    rt = x;
                } else if (x instanceof Array){ // Array
                    rt = {};
                    temp = [];
                    for (i=0; i<x.length; i++) {
                        temp[i] = that.makeSerializable(x[i]);
                    }
                    rt[LIST_STRING] = temp;
                } else if ((x instanceof Object) && 
                            !(StorageToken.isInstance(x))){ // Object
                    rt = {};
                    temp = {};
                    for (key in x){
						temp[key] = that.makeSerializable(x[key]);
                    }
                    rt[MAP_STRING] = temp;
                } else if (StorageToken.isInstance(x)){ // StorageToken
                    rt = {};
                    temp = {};
                    keys = x.keys();
                    for (i=0; i<keys.length; i++) {
						temp[that.makeSerializable(keys[i])] = that.makeSerializable(x.getitem(keys[i]));
                    }
                    rt[x.getClassId()] = temp;
                } else { //Error
                    throw new TypeError("Tried to serialize unserializable object of type (" + xType + "): " + x);
                }
                return rt;
            };

            that.makeNative = function makeNative(x){
                var i, key, rt, temp, xType, dataTypeName;
                xType = typeof(x);
                rt = null;
                if ((that.VALID_ATOMIC_VALUE_TYPES[xType]) || (x == null)){// Primitive variables
                  rt = x;
                  return rt;
                }
                for (dataTypeName in x){
                    break;
                }
                if (dataTypeName in that.VALID_SEQUENCE_VALUE_TYPES){ // Array
                    rt = [];
                    for (i=0; i<x[dataTypeName].length; i++) {
                        rt[i] = that.makeNative(x[dataTypeName][i]);
                    }
                } else if (dataTypeName in that.VALID_MAPPING_VALUE_TYPES) { // Object
                    rt = {};
                    for (key in x[dataTypeName]) {
                        rt[key] = that.makeNative(x[dataTypeName][key]);
                    }
                } else { //Default StorageToken
                    rt = {};
                    rt[MAP_STRING] = x[dataTypeName];
                    rt = that.makeNative(rt);
                    rt = StorageToken(undefined, undefined, rt);
                }
                return rt;
            };
        }
    });
    
    var JSONRWFormatter = JSONRWFormat(),
		XMLRWFormat = null,
		XMLRWFormatter = null;
	
	// Function to Create an Object From a Token
	var createFromToken = function(token, context, onMissingClass){
	/** Create a serializable instance from an arbitrary storage token
		@param token: Storage token
		@param context (optional): Mutable context for the loading process. Defaults to null. 
        @param onMissingClass (optional): Function to transform/error on token if class missing
	*/
		var id = token.getId();
		var instance = {};
		if ((context != null) && (id in context)){
			instance = context[id];
		} else {
			//Need to import the right class
			var classId = token.getClassId();
			var AClass = Zet.getFactoryClass(classId);
			if (typeof AClass !== "undefined"){
                instance = AClass();
                instance.initializeFromToken(token, context);
            } else {
                if (onMissingClass == null){
                    onMissingClass = defaultOnMissing;
                }
                instance = onMissingClass(token);
            }	
		}
		return instance;
	};
	
    var defaultOnMissing = function(token, errorOnMissing){
        if (!(errorOnMissing)){
            console.log("ERROR: Couldn't make class from factory: " + token.getClassId());
            return token;
        } else {
            throw new Error("Class Factory failed to import " + token.getClassId());
        }
    };
    
    // Convenience Function to Serialize and Un-Serialize Objects
    //----------------------------------------------------------
    var serializeObject = function serializeObject(obj, sFormat){
        /** A function that will attempt to turn any valid object 
            (Serializable, StorageToken, map, list, atomic) into 
            its string serialized equivalent.
            @param obj: Any object that can be serialized, i.e., Serializable, StorageToken, TokenRWFormat.VALID_VALUE_TYPES
            @type obj: object
            @param sFormat: Serializable format to pack things as
            @type sFormat: string
            @return: Serialized object
            @rtype: string
        **/
        return makeSerialized(tokenizeObject(obj), sFormat);
    };
    
    var nativizeObject = function nativizeObject(obj, context, sFormat){
        /** A function that will attempt to turn any valid object 
            (Serializable, StorageToken, map, list, atomic) into 
            its highest native equivalent (Serializable > StorageToken > list/map > atomic).
            @param obj: Any object that can be serialized, i.e., Serializable, StorageToken, TokenRWFormat.VALID_VALUE_TYPES
            @type obj: object
            @param sFormat: Serializable format to unpack things as
            @type sFormat: string
            @return: Least serialized form of this object
            @rtype: string
        **/ 
        if (Serializable.isInstance(obj)){
            return obj;
        } else if (StorageToken.isInstance(obj)){
            return createFromToken(obj, context);
        } else if (typeof obj === "string" || obj instanceof String){
            obj = makeNative(obj, sFormat);
            return untokenizeObject(obj);
        } else {
            return obj;
        }
    };
    
    // Convenience Function to Tokenize and Un-Tokenize Objects
    //----------------------------------------------------------
    var tokenizeObject = function (obj) {
        var i, key, rt;
        rt = null;
        //Generic function to tokenize an object
        if (Serializable.isInstance(obj)) {// Serializable
            rt = obj.saveToToken();  
        } else if (obj instanceof Array){ // Array
            rt = [];
            for (i=0; i<obj.length; i++) {
                rt[i] = tokenizeObject(obj[i]);  
            }
        } else if ((obj instanceof Object) &&
                  !(obj instanceof Array)){ // Object
            rt = {};
            for (key in obj) {
                rt[tokenizeObject(key)] = tokenizeObject(obj[key]);  
            }
        } else {
            rt = obj;
        }
        return rt;
    };

    var untokenizeObject = function(obj, context){
    /** Generic function to create an object from a token 
        @param obj: Object to turn from tokens into object
        @param context (optional): Mutable context for the loading process. Defaults to null. 
    */
        var rt = null;
        if (StorageToken.isInstance(obj)) {// StorageToken
            rt = createFromToken(obj, context);
        } else if (obj instanceof Array) { // Array
            rt = [];
            for (var i in obj) { 
                rt[i] = untokenizeObject(obj[i], context);
            }
        } else if ((obj instanceof Object) &&
                  !(obj instanceof Array)){ // Object
            rt = {};
            for (var key in obj) {
                rt[untokenizeObject(key, context)] = untokenizeObject(obj[key], context);
            }
        } else {
            rt = obj;
        }
        return rt;
    };
    
    // Convenience functions to serialize and unserialize tokens and raw data
    //---------------------------------------------
    var makeSerialized = function makeSerialized(obj, sFormat){
    /** Generic function to turn a tokenized object into serialized form
        @param obj: Tokenized object
        @param sFormat (optional): Serialization format.  Defaults to JSON_FORMAT
    */
        if (sFormat === undefined){ // Default format is JSON_FORMAT
            sFormat = JSON_FORMAT;
        }
        if (sFormat == JSON_FORMAT){
            return JSONRWFormatter.serialize(obj);
        }else if (sFormat == XML_FORMAT){
            return XMLRWFormatter.serialize(obj);
        } else {
            throw new TypeError("No serialization format of type: " + sFormat);
        }
    };

    var makeNative = function makeNative(String, sFormat){
    /** Generic function to turn a serialized string into a tokenized object
    *   @param String: Serialized object, as a string
    *   @param sFormat (optional): Serialization format.  Defaults to JSON_FORMAT
    */
        if (sFormat === undefined){ // Default format is JSON_FORMAT
            sFormat = JSON_FORMAT;
        }
        if (sFormat == JSON_FORMAT){
            return JSONRWFormatter.parse(String);
        }else if (sFormat == XML_FORMAT){
            // Not currently implemented
            return XMLRWFormatter.parse(String);
        } else {
            throw new TypeError("No unserialization format of type: " + sFormat);
        }
    };
    
    // Expose Variables Publicly
    Serialization.JSON_FORMAT = JSON_FORMAT;
    Serialization.XML_FORMAT = XML_FORMAT;
    Serialization.VALID_SERIAL_FORMATS = VALID_SERIAL_FORMATS;
    
    // Expose Functions Publicly
	Serialization.createFromToken = createFromToken;
    Serialization.serializeObject = serializeObject;
    Serialization.nativizeObject = nativizeObject;
    Serialization.makeSerialized = makeSerialized;
    Serialization.makeNative = makeNative;
    Serialization.tokenizeObject = tokenizeObject;
    Serialization.untokenizeObject = untokenizeObject;
    
    // Expose Classes Publicly
    Serialization.Serializable = Serializable;
    Serialization.NamedSerializable = NamedSerializable;
    Serialization.StorageToken = StorageToken;
    Serialization.TokenRWFormat = TokenRWFormat;
    Serialization.JSONRWFormat = JSONRWFormat;
	//Serialization.XMLRWFormat = XMLRWFormat;
	
	// Expose Instances Publicly
	Serialization.JSONRWFormatter = JSONRWFormatter;
	//Serialization.XMLRWFormatter = XMLRWFormatter;
})(window.Serialization = window.Serialization || {});

// Basic Test Debug Code: To see that things work
if (false) {
    print("Create The Serializable");
    x = Serialization.Serializable();
    print("Is Serializable: " + Zet(x).instanceOf(Serializable));
    print("Is Token: " + Zet(x).instanceOf(StorageToken));
    print("ID: " + x.getId());
    print("ClassID: " + x.getClassId());
    print("");
    
    print("Create the Storage Token");
    token = x.saveToToken();
    print("Is Serializable: " + Zet(token).instanceOf(Serializable));
    print("Is Token: " + Zet(token).instanceOf(StorageToken));
    print("ID: " + token.getId());
    print("ClassID: " + token.getClassId());
    print("Keys: " + token.keys());
}