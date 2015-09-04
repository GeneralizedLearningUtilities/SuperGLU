/** Simple text processing utilities 
    Package: SuperGLU
    Author: Benjamin D. Nye
    License: APL 2.0
**/

if (typeof window === "undefined") {
    var window = this;
}

(function(namespace, undefined) {

var SEGMENTERS = '\\.!\\?';
var SENTENCE_REGEX ='['+SEGMENTERS+']\\s+(?=\\S)';

/** Split the given text at every regex match 
    @param text: The text to split
    @type text: str
    @param regex: The regex value
    @type regex: Regular expression or string
    @return: Array of string fragments
    @rtype: array of str
 **/
var splitAtRegex = function splitAtRegex(text, regex){
    var match;
    var matches = [];
    var lastIndex = 0;
    while((match = regex.exec(text)) !== null){
        matches.push(text.slice(lastIndex, regex.lastIndex));
        lastIndex = regex.lastIndex;
    }
    if (text.slice(lastIndex, text.length).length > 0){
        matches.push(text.slice(lastIndex, text.length));
    }
    return matches;
};


/** Split the given text into sentences (end punctuation followed by space).
    @param text: The text to split
    @type text: str
    @return: Array of sentences
    @rtype: array of str
 **/
var splitSentences = function splitSentences(text){
    var regex = new RegExp(SENTENCE_REGEX, 'g');
    return splitAtRegex(text, regex);
};

/** Escape XML symbols into the appropriate HTML display characters.
    @param text: The text to escape
    @type text: str
    @return: escaped string
    @rtype: str
 **/
var escapeXML = function escapeXML(text){
    return text.replace(/&/g, '&amp;')
               .replace(/</g, '&lt;')
               .replace(/>/g, '&gt;')
               .replace(/"/g, '&quot;')
               .replace(/'/g, '&apos;');
};

/** Escape text intended to be inside an HTML key-value pair,
    by changing all normal double-quotes into double single-quotes
    @param text: The text to escape
    @type text: str
    @return: escaped string
    @rtype: str
 **/
var escapeBubble = function escapeBubble(text){
    return text.replace(/"/g, "''");
};

/** Escape text intended to have no HTML tags inside of it,
    by clearing out any bare < or > characters.
    @param text: The text to escape
    @type text: str
    @return: escaped string
    @rtype: str
 **/
var escapeVoice = function escapeVoice(text){
    return text.replace(/</g, "")
               .replace(/>/g, "");
};

namespace.splitAtRegex = splitAtRegex;
namespace.splitSentences = splitSentences;
namespace.escapeXML = escapeXML;
namespace.escapeBubble = escapeBubble;
namespace.escapeVoice = escapeVoice;
})(window.Text_Utils = window.Text_Utils || {});