// Requires Java and Rhino's js.jar
var filePaths = [["Util", "zet.js"],
                 ["Util", "serialization.js"],
                 ["Util", "uuid.js"],
                 ["Util", "Tests", "SerializationTestClass.js"]];
var depth = 2;
var sep = String.fromCharCode(java.io.File.separatorChar);
if (arguments.length > 0){
    path = arguments[0].split(sep);
} else {
    path = [];
    for (var i=0; i<depth; i++){
        path.push("..");
    }
}
for (var i=0; i<filePaths.length; i++) {
    load(path.concat(filePaths[i]).join(sep));
}
print(Serialization.makeSerialized(serializableObj.saveToToken()));