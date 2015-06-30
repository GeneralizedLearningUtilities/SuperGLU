if (typeof window === "undefined") {
    var window = this;
}

(function(namespace, undefined) {

var SEGMENTERS = '\\.!\\?';
var SENTENCE_REGEX ='['+SEGMENTERS+']\\s+(?=\\S)';

var splitAtRegex = function splitAtRegex(text, regex){
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

var splitSentences = function splitSentences(text){
    var regex = new RegExp(SENTENCE_REGEX, 'g');
    return splitAtRegex(text, regex);
};

var escapeXML = function escapeXML(text){
    return text.replace(/&/g, '&amp;')
               .replace(/</g, '&lt;')
               .replace(/>/g, '&gt;')
               .replace(/"/g, '&quot;')
               .replace(/'/g, '&apos;');
};

var escapeBubble = function escapeBubble(text){
    return text.replace(/"/g, "''");
};

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