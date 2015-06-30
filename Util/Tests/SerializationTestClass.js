// Requires Java and Rhino's js.jar
Zet.declare('TestClass', {
	superclass : Serialization.Serializable,
    defineBody : function(self){
		// Public Properties
		
		// Constructor
		self.construct = function construct(value){
			self.inherited(construct);
			self._value = value;
		};
		
		// Public Methods
		self.initializeFromToken = function initializeFromToken(token, context){
			self.inherited(initializeFromToken, [token, context]);
			self._value = token.getitem('value');
		};

		self.saveToToken = function saveToToken(){
			token = self.inherited(saveToToken);
			token.setitem('value', self._value);
			return token;
		};
	}
});

Zet.declare('TestClass2', {
	superclass : Serialization.Serializable,
    defineBody : function(self){
		// Public Properties
		// Constructor
		self.construct = function construct(statement){
			self.inherited(construct);
			self._statement = statement;
		};
		
		// Public Methods
		self.initializeFromToken = function initializeFromToken(token, context){
			self.inherited(initializeFromToken, [token, context]);
			self._statement = token.getitem('statement');
		};

		self.saveToToken = function saveToToken(){
			token = self.inherited(saveToToken);
			token.setitem('statement', self._statement);
			return token;
		};
	}
});


var serializableObj = Serialization.Serializable();
var aTestObj = TestClass(10);
var aTestObj2 = TestClass2("AAA");
var aTestObjNull = TestClass(null);
var aTestObjUndef = TestClass(undefined);
	
if (false){
	var st = serializableObj.saveToToken();
	print("ST for Serializable");
	var t1 = aTestObj.saveToToken();
	print("ST for T1");
	print("VALUE: "+ t1._data.value);
	print("getitem VALUE: "+ t1.getitem('value'));
	var t2 = aTestObj2.saveToToken();
	print("ST for T2");

	var rSerializableObj = Serialization.createFromToken(st);

	print("MAKE SERIALIZED");
	print(Serialization.makeSerialized(st));
	print(Serialization.makeSerialized(t1));
	print(Serialization.makeSerialized(t2));

	print(StorageToken.isInstance(st));
	var rSerializableObj = Serialization.createFromToken(st);
	var rTestObj = Serialization.createFromToken(t1);
	var rTestObj2 = Serialization.createFromToken(t2);

	print("Serializable: " + rSerializableObj.CLASS_ID + " / " + serializableObj.eq(rSerializableObj));
	print("Test Obj: " + rTestObj.CLASS_ID + " / " + aTestObj.eq(rTestObj));
	print("Test Obj 2: " + rTestObj2.CLASS_ID + " / " + aTestObj2.eq(rTestObj2));
	print("Test Obj 2: " + rTestObj.CLASS_ID + " / " + rTestObj2.eq(rTestObj));
}