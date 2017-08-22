/**FUNCTION StringSet() creates a set object that takes in strings.

METHOD add(str), adds a string to the set object.
METHOD contains(str), checks for string key in set object.
METHOD remove(str), removes string key and value from set object.
METHOD values(), iterates and adds 

*/

function StringSet() {
    var setObj = {}, val = {};

    this.add = function(str) {
        setObj[str] = val;
    };

    this.contains = function(str) {
        return setObj[str] === val;
    };

    this.remove = function(str) {
        delete setObj[str];
    };

}