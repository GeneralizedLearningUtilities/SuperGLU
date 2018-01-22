/** Polyfill patches for non-compliant browsers for EMACS5
 Package: SuperGLU
 Author: Benjamin Nye
 License: APL 2.0
 **/

/** Fix for IE8 and under, where arrays have no indexOf... **/
var indexOf = function(needle) {
    if(typeof Array.prototype.indexOf === 'function') {
        indexOf = Array.prototype.indexOf;
    } else {
        indexOf = function(needle) {
            var i = -1, index = -1;
            for(i = 0; i < this.length; i++) {
                if(this[i] === needle) {
                    index = i;
                    break;
                }
            }
            return index;
        };
    }
    return indexOf.call(this, needle);
};

/** Fix for IE8 and under, where arrays have no indexOf... **/
Object.values = function(obj){
    return (Object.keys(obj)).map(function(key){return obj[key];});
};

/** Fill in toISOString if not defined (Thanks, IE8) **/
if ( !Date.prototype.toISOString ) {
    ( function() {

        function pad(number) {
            var r = String(number);
            if ( r.length === 1 ) {
                r = '0' + r;
            }
            return r;
        }

        Date.prototype.toISOString = function() {
            return (this.getUTCFullYear() +
                '-' + pad( this.getUTCMonth() + 1 ) +
                '-' + pad( this.getUTCDate() ) +
                'T' + pad( this.getUTCHours() ) +
                ':' + pad( this.getUTCMinutes() ) +
                ':' + pad( this.getUTCSeconds() )  +
                '.' + String( (this.getUTCMilliseconds()/1000).toFixed(3) ).slice( 2, 5 ) +
                'Z');
        };

    }() );
}

/** Object.create polyfill **/
if (!Object.create) {
    Object.create = (function(){
        function F(){}

        return function(o){
            if (arguments.length != 1) {
                throw new Error('Object.create implementation only accepts one parameter.');
            }
            F.prototype = o;
            return new F();
        };
    })();
}

/** Console-polyfill. MIT license.
 Attribution: Paul Miller
 https://github.com/paulmillr/console-polyfill
 Make it safe to do console.log() always.
 **/
(function(con) {
    'use strict';
    var prop, method;
    var empty = {};
    var dummy = function() {};
    var properties = 'memory'.split(',');
    var methods = ('assert,clear,count,debug,dir,dirxml,error,exception,group,' +
        'groupCollapsed,groupEnd,info,log,markTimeline,profile,profileEnd,' +
        'table,time,timeEnd,timeStamp,trace,warn').split(',');
    while (prop = properties.pop()) con[prop] = con[prop] || empty;
    while (method = methods.pop()) con[method] = con[method] || dummy;
})(this.console = this.console || {}); // Using `this` for web workers.

/**
 * A Javascript object to encode and/or decode html characters using HTML or Numeric entities that handles double or partial encoding
 * Author: R Reid
 * source: http://www.strictly-software.com/htmlencode
 * Licences: GPL, The MIT License (MIT)
 * Copyright: (c) 2011 Robert Reid - Strictly-Software.com
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 *
 * Revision:
 *  2011-07-14, Jacques-Yves Bleau:
 *       - fixed conversion error with capitalized accentuated characters
 *       + converted arr1 and arr2 to object property to remove redundancy
 *
 * Revision:
 *  2011-11-10, Ce-Yi Hio:
 *       - fixed conversion error with a number of capitalized entity characters
 *
 * Revision:
 *  2011-11-10, Rob Reid:
 *		 - changed array format
 *
 * Revision:
 *  2012-09-23, Alex Oss:
 *		 - replaced string concatonation in numEncode with string builder, push and join for peformance with ammendments by Rob Reid
 */

Encoder = {

    // When encoding do we convert characters into html or numerical entities
    EncodeType : "entity",  // entity OR numerical

    isEmpty : function(val){
        if(val){
            return ((val===null) || val.length==0 || /^\s+$/.test(val));
        }else{
            return true;
        }
    },

    // arrays for conversion from HTML Entities to Numerical values
    arr1: ['&nbsp;','&iexcl;','&cent;','&pound;','&curren;','&yen;','&brvbar;','&sect;','&uml;','&copy;','&ordf;','&laquo;','&not;','&shy;','&reg;','&macr;','&deg;','&plusmn;','&sup2;','&sup3;','&acute;','&micro;','&para;','&middot;','&cedil;','&sup1;','&ordm;','&raquo;','&frac14;','&frac12;','&frac34;','&iquest;','&Agrave;','&Aacute;','&Acirc;','&Atilde;','&Auml;','&Aring;','&AElig;','&Ccedil;','&Egrave;','&Eacute;','&Ecirc;','&Euml;','&Igrave;','&Iacute;','&Icirc;','&Iuml;','&ETH;','&Ntilde;','&Ograve;','&Oacute;','&Ocirc;','&Otilde;','&Ouml;','&times;','&Oslash;','&Ugrave;','&Uacute;','&Ucirc;','&Uuml;','&Yacute;','&THORN;','&szlig;','&agrave;','&aacute;','&acirc;','&atilde;','&auml;','&aring;','&aelig;','&ccedil;','&egrave;','&eacute;','&ecirc;','&euml;','&igrave;','&iacute;','&icirc;','&iuml;','&eth;','&ntilde;','&ograve;','&oacute;','&ocirc;','&otilde;','&ouml;','&divide;','&oslash;','&ugrave;','&uacute;','&ucirc;','&uuml;','&yacute;','&thorn;','&yuml;','&quot;','&amp;','&lt;','&gt;','&OElig;','&oelig;','&Scaron;','&scaron;','&Yuml;','&circ;','&tilde;','&ensp;','&emsp;','&thinsp;','&zwnj;','&zwj;','&lrm;','&rlm;','&ndash;','&mdash;','&lsquo;','&rsquo;','&sbquo;','&ldquo;','&rdquo;','&bdquo;','&dagger;','&Dagger;','&permil;','&lsaquo;','&rsaquo;','&euro;','&fnof;','&Alpha;','&Beta;','&Gamma;','&Delta;','&Epsilon;','&Zeta;','&Eta;','&Theta;','&Iota;','&Kappa;','&Lambda;','&Mu;','&Nu;','&Xi;','&Omicron;','&Pi;','&Rho;','&Sigma;','&Tau;','&Upsilon;','&Phi;','&Chi;','&Psi;','&Omega;','&alpha;','&beta;','&gamma;','&delta;','&epsilon;','&zeta;','&eta;','&theta;','&iota;','&kappa;','&lambda;','&mu;','&nu;','&xi;','&omicron;','&pi;','&rho;','&sigmaf;','&sigma;','&tau;','&upsilon;','&phi;','&chi;','&psi;','&omega;','&thetasym;','&upsih;','&piv;','&bull;','&hellip;','&prime;','&Prime;','&oline;','&frasl;','&weierp;','&image;','&real;','&trade;','&alefsym;','&larr;','&uarr;','&rarr;','&darr;','&harr;','&crarr;','&lArr;','&uArr;','&rArr;','&dArr;','&hArr;','&forall;','&part;','&exist;','&empty;','&nabla;','&isin;','&notin;','&ni;','&prod;','&sum;','&minus;','&lowast;','&radic;','&prop;','&infin;','&ang;','&and;','&or;','&cap;','&cup;','&int;','&there4;','&sim;','&cong;','&asymp;','&ne;','&equiv;','&le;','&ge;','&sub;','&sup;','&nsub;','&sube;','&supe;','&oplus;','&otimes;','&perp;','&sdot;','&lceil;','&rceil;','&lfloor;','&rfloor;','&lang;','&rang;','&loz;','&spades;','&clubs;','&hearts;','&diams;'],
    arr2: ['&#160;','&#161;','&#162;','&#163;','&#164;','&#165;','&#166;','&#167;','&#168;','&#169;','&#170;','&#171;','&#172;','&#173;','&#174;','&#175;','&#176;','&#177;','&#178;','&#179;','&#180;','&#181;','&#182;','&#183;','&#184;','&#185;','&#186;','&#187;','&#188;','&#189;','&#190;','&#191;','&#192;','&#193;','&#194;','&#195;','&#196;','&#197;','&#198;','&#199;','&#200;','&#201;','&#202;','&#203;','&#204;','&#205;','&#206;','&#207;','&#208;','&#209;','&#210;','&#211;','&#212;','&#213;','&#214;','&#215;','&#216;','&#217;','&#218;','&#219;','&#220;','&#221;','&#222;','&#223;','&#224;','&#225;','&#226;','&#227;','&#228;','&#229;','&#230;','&#231;','&#232;','&#233;','&#234;','&#235;','&#236;','&#237;','&#238;','&#239;','&#240;','&#241;','&#242;','&#243;','&#244;','&#245;','&#246;','&#247;','&#248;','&#249;','&#250;','&#251;','&#252;','&#253;','&#254;','&#255;','&#34;','&#38;','&#60;','&#62;','&#338;','&#339;','&#352;','&#353;','&#376;','&#710;','&#732;','&#8194;','&#8195;','&#8201;','&#8204;','&#8205;','&#8206;','&#8207;','&#8211;','&#8212;','&#8216;','&#8217;','&#8218;','&#8220;','&#8221;','&#8222;','&#8224;','&#8225;','&#8240;','&#8249;','&#8250;','&#8364;','&#402;','&#913;','&#914;','&#915;','&#916;','&#917;','&#918;','&#919;','&#920;','&#921;','&#922;','&#923;','&#924;','&#925;','&#926;','&#927;','&#928;','&#929;','&#931;','&#932;','&#933;','&#934;','&#935;','&#936;','&#937;','&#945;','&#946;','&#947;','&#948;','&#949;','&#950;','&#951;','&#952;','&#953;','&#954;','&#955;','&#956;','&#957;','&#958;','&#959;','&#960;','&#961;','&#962;','&#963;','&#964;','&#965;','&#966;','&#967;','&#968;','&#969;','&#977;','&#978;','&#982;','&#8226;','&#8230;','&#8242;','&#8243;','&#8254;','&#8260;','&#8472;','&#8465;','&#8476;','&#8482;','&#8501;','&#8592;','&#8593;','&#8594;','&#8595;','&#8596;','&#8629;','&#8656;','&#8657;','&#8658;','&#8659;','&#8660;','&#8704;','&#8706;','&#8707;','&#8709;','&#8711;','&#8712;','&#8713;','&#8715;','&#8719;','&#8721;','&#8722;','&#8727;','&#8730;','&#8733;','&#8734;','&#8736;','&#8743;','&#8744;','&#8745;','&#8746;','&#8747;','&#8756;','&#8764;','&#8773;','&#8776;','&#8800;','&#8801;','&#8804;','&#8805;','&#8834;','&#8835;','&#8836;','&#8838;','&#8839;','&#8853;','&#8855;','&#8869;','&#8901;','&#8968;','&#8969;','&#8970;','&#8971;','&#9001;','&#9002;','&#9674;','&#9824;','&#9827;','&#9829;','&#9830;'],

    // Convert HTML entities into numerical entities
    HTML2Numerical : function(s){
        return this.swapArrayVals(s,this.arr1,this.arr2);
    },

    // Convert Numerical entities into HTML entities
    NumericalToHTML : function(s){
        return this.swapArrayVals(s,this.arr2,this.arr1);
    },


    // Numerically encodes all unicode characters
    numEncode : function(s){
        if(this.isEmpty(s)) return "";

        var a = [],
            l = s.length;

        for (var i=0;i<l;i++){
            var c = s.charAt(i);
            if (c < " " || c > "~"){
                a.push("&#");
                a.push(c.charCodeAt()); //numeric value of code point
                a.push(";");
            }else{
                a.push(c);
            }
        }

        return a.join("");
    },

    // HTML Decode numerical and HTML entities back to original values
    htmlDecode : function(s){

        var c,m,d = s;

        if(this.isEmpty(d)) return "";

        // convert HTML entites back to numerical entites first
        d = this.HTML2Numerical(d);

        // look for numerical entities &#34;
        arr=d.match(/&#[0-9]{1,5};/g);

        // if no matches found in string then skip
        if(arr!=null){
            for(var x=0;x<arr.length;x++){
                m = arr[x];
                c = m.substring(2,m.length-1); //get numeric part which is refernce to unicode character
                // if its a valid number we can decode
                if(c >= -32768 && c <= 65535){
                    // decode every single match within string
                    d = d.replace(m, String.fromCharCode(c));
                }else{
                    d = d.replace(m, ""); //invalid so replace with nada
                }
            }
        }

        return d;
    },

    // encode an input string into either numerical or HTML entities
    htmlEncode : function(s,dbl){

        if(this.isEmpty(s)) return "";

        // do we allow double encoding? E.g will &amp; be turned into &amp;amp;
        dbl = dbl || false; //default to prevent double encoding

        // if allowing double encoding we do ampersands first
        if(dbl){
            if(this.EncodeType=="numerical"){
                s = s.replace(/&/g, "&#38;");
            }else{
                s = s.replace(/&/g, "&amp;");
            }
        }

        // convert the xss chars to numerical entities ' " < >
        s = this.XSSEncode(s,false);

        if(this.EncodeType=="numerical" || !dbl){
            // Now call function that will convert any HTML entities to numerical codes
            s = this.HTML2Numerical(s);
        }

        // Now encode all chars above 127 e.g unicode
        s = this.numEncode(s);

        // now we know anything that needs to be encoded has been converted to numerical entities we
        // can encode any ampersands & that are not part of encoded entities
        // to handle the fact that I need to do a negative check and handle multiple ampersands &&&
        // I am going to use a placeholder

        // if we don't want double encoded entities we ignore the & in existing entities
        if(!dbl){
            s = s.replace(/&#/g,"##AMPHASH##");

            if(this.EncodeType=="numerical"){
                s = s.replace(/&/g, "&#38;");
            }else{
                s = s.replace(/&/g, "&amp;");
            }

            s = s.replace(/##AMPHASH##/g,"&#");
        }

        // replace any malformed entities
        s = s.replace(/&#\d*([^\d;]|$)/g, "$1");

        if(!dbl){
            // safety check to correct any double encoded &amp;
            s = this.correctEncoding(s);
        }

        // now do we need to convert our numerical encoded string into entities
        if(this.EncodeType=="entity"){
            s = this.NumericalToHTML(s);
        }

        return s;
    },

    // Encodes the basic 4 characters used to malform HTML in XSS hacks
    XSSEncode : function(s,en){
        if(!this.isEmpty(s)){
            en = en || true;
            // do we convert to numerical or html entity?
            if(en){
                s = s.replace(/\'/g,"&#39;"); //no HTML equivalent as &apos is not cross browser supported
                s = s.replace(/\"/g,"&quot;");
                s = s.replace(/</g,"&lt;");
                s = s.replace(/>/g,"&gt;");
            }else{
                s = s.replace(/\'/g,"&#39;"); //no HTML equivalent as &apos is not cross browser supported
                s = s.replace(/\"/g,"&#34;");
                s = s.replace(/</g,"&#60;");
                s = s.replace(/>/g,"&#62;");
            }
            return s;
        }else{
            return "";
        }
    },

    // returns true if a string contains html or numerical encoded entities
    hasEncoded : function(s){
        if(/&#[0-9]{1,5};/g.test(s)){
            return true;
        }else if(/&[A-Z]{2,6};/gi.test(s)){
            return true;
        }else{
            return false;
        }
    },

    // will remove any unicode characters
    stripUnicode : function(s){
        return s.replace(/[^\x20-\x7E]/g,"");

    },

    // corrects any double encoded &amp; entities e.g &amp;amp;
    correctEncoding : function(s){
        return s.replace(/(&amp;)(amp;)+/,"$1");
    },


    // Function to loop through an array swaping each item with the value from another array e.g swap HTML entities with Numericals
    swapArrayVals : function(s,arr1,arr2){
        if(this.isEmpty(s)) return "";
        var re;
        if(arr1 && arr2){
            //ShowDebug("in swapArrayVals arr1.length = " + arr1.length + " arr2.length = " + arr2.length)
            // array lengths must match
            if(arr1.length == arr2.length){
                for(var x=0,i=arr1.length;x<i;x++){
                    re = new RegExp(arr1[x], 'g');
                    s = s.replace(re,arr2[x]); //swap arr1 item with matching item from arr2
                }
            }
        }
        return s;
    },

    inArray : function( item, arr ) {
        for ( var i = 0, x = arr.length; i < x; i++ ){
            if ( arr[i] === item ){
                return i;
            }
        }
        return -1;
    }

}
/**
 * uuid.js: The RFC-compliant UUID generator for JavaScript.
 *
 * @fileOverview
 * @author  LiosK
 * @version 3.2
 * @license The MIT License: Copyright (c) 2010-2012 LiosK.
 */

/** @constructor */
var UUID;

UUID = (function(overwrittenUUID) {

// Core Component {{{

    /** @lends UUID */
    function UUID() {}

    /**
     * The simplest function to get an UUID string.
     * @returns {string} A version 4 UUID string.
     */
    UUID.generate = function() {
        var rand = UUID._getRandomInt, hex = UUID._hexAligner;
        return  hex(rand(32), 8)          // time_low
            + "-"
            + hex(rand(16), 4)          // time_mid
            + "-"
            + hex(0x4000 | rand(12), 4) // time_hi_and_version
            + "-"
            + hex(0x8000 | rand(14), 4) // clock_seq_hi_and_reserved clock_seq_low
            + "-"
            + hex(rand(48), 12);        // node
    };

    /**
     * Returns an unsigned x-bit random integer.
     * @param {int} x A positive integer ranging from 0 to 53, inclusive.
     * @returns {int} An unsigned x-bit random integer (0 <= f(x) < 2^x).
     */
    UUID._getRandomInt = function(x) {
        if (x <   0) return NaN;
        if (x <= 30) return (0 | Math.random() * (1 <<      x));
        if (x <= 53) return (0 | Math.random() * (1 <<     30))
            + (0 | Math.random() * (1 << x - 30)) * (1 << 30);
        return NaN;
    };

    /**
     * Returns a function that converts an integer to a zero-filled string.
     * @param {int} radix
     * @returns {function(num&#44; length)}
     */
    UUID._getIntAligner = function(radix) {
        return function(num, length) {
            var str = num.toString(radix), i = length - str.length, z = "0";
            for (; i > 0; i >>>= 1, z += z) { if (i & 1) { str = z + str; } }
            return str;
        };
    };

    UUID._hexAligner = UUID._getIntAligner(16);

// }}}

// UUID Object Component {{{

    /**
     * Names of each UUID field.
     * @type string[]
     * @constant
     * @since 3.0
     */
    UUID.FIELD_NAMES = ["timeLow", "timeMid", "timeHiAndVersion",
        "clockSeqHiAndReserved", "clockSeqLow", "node"];

    /**
     * Sizes of each UUID field.
     * @type int[]
     * @constant
     * @since 3.0
     */
    UUID.FIELD_SIZES = [32, 16, 16, 8, 8, 48];

    /**
     * Generates a version 4 {@link UUID}.
     * @returns {UUID} A version 4 {@link UUID} object.
     * @since 3.0
     */
    UUID.genV4 = function() {
        var rand = UUID._getRandomInt;
        return new UUID()._init(rand(32), rand(16), // time_low time_mid
            0x4000 | rand(12),  // time_hi_and_version
            0x80   | rand(6),   // clock_seq_hi_and_reserved
            rand(8), rand(48)); // clock_seq_low node
    };

    /**
     * Converts hexadecimal UUID string to an {@link UUID} object.
     * @param {string} strId UUID hexadecimal string representation ("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx").
     * @returns {UUID} {@link UUID} object or null.
     * @since 3.0
     */
    UUID.parse = function(strId) {
        var r, p = /^\s*(urn:uuid:|\{)?([0-9a-f]{8})-([0-9a-f]{4})-([0-9a-f]{4})-([0-9a-f]{2})([0-9a-f]{2})-([0-9a-f]{12})(\})?\s*$/i;
        if (r = p.exec(strId)) {
            var l = r[1] || "", t = r[8] || "";
            if (((l + t) === "") ||
                (l === "{" && t === "}") ||
                (l.toLowerCase() === "urn:uuid:" && t === "")) {
                return new UUID()._init(parseInt(r[2], 16), parseInt(r[3], 16),
                    parseInt(r[4], 16), parseInt(r[5], 16),
                    parseInt(r[6], 16), parseInt(r[7], 16));
            }
        }
        return null;
    };

    /**
     * Initializes {@link UUID} object.
     * @param {uint32} [timeLow=0] time_low field (octet 0-3).
     * @param {uint16} [timeMid=0] time_mid field (octet 4-5).
     * @param {uint16} [timeHiAndVersion=0] time_hi_and_version field (octet 6-7).
     * @param {uint8} [clockSeqHiAndReserved=0] clock_seq_hi_and_reserved field (octet 8).
     * @param {uint8} [clockSeqLow=0] clock_seq_low field (octet 9).
     * @param {uint48} [node=0] node field (octet 10-15).
     * @returns {UUID} this.
     */
    UUID.prototype._init = function() {
        var names = UUID.FIELD_NAMES, sizes = UUID.FIELD_SIZES;
        var bin = UUID._binAligner, hex = UUID._hexAligner;

        /**
         * List of UUID field values (as integer values).
         * @type int[]
         */
        this.intFields = new Array(6);

        /**
         * List of UUID field values (as binary bit string values).
         * @type string[]
         */
        this.bitFields = new Array(6);

        /**
         * List of UUID field values (as hexadecimal string values).
         * @type string[]
         */
        this.hexFields = new Array(6);

        for (var i = 0; i < 6; i++) {
            var intValue = parseInt(arguments[i] || 0);
            this.intFields[i] = this.intFields[names[i]] = intValue;
            this.bitFields[i] = this.bitFields[names[i]] = bin(intValue, sizes[i]);
            this.hexFields[i] = this.hexFields[names[i]] = hex(intValue, sizes[i] / 4);
        }

        /**
         * UUID version number defined in RFC 4122.
         * @type int
         */
        this.version = (this.intFields.timeHiAndVersion >> 12) & 0xF;

        /**
         * 128-bit binary bit string representation.
         * @type string
         */
        this.bitString = this.bitFields.join("");

        /**
         * UUID hexadecimal string representation ("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx").
         * @type string
         */
        this.hexString = this.hexFields[0] + "-" + this.hexFields[1] + "-" + this.hexFields[2]
            + "-" + this.hexFields[3] + this.hexFields[4] + "-" + this.hexFields[5];

        /**
         * UUID string representation as a URN ("urn:uuid:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx").
         * @type string
         */
        this.urn = "urn:uuid:" + this.hexString;

        return this;
    };

    UUID._binAligner = UUID._getIntAligner(2);

    /**
     * Returns UUID string representation.
     * @returns {string} {@link UUID#hexString}.
     */
    UUID.prototype.toString = function() { return this.hexString; };

    /**
     * Tests if two {@link UUID} objects are equal.
     * @param {UUID} uuid
     * @returns {bool} True if two {@link UUID} objects are equal.
     */
    UUID.prototype.equals = function(uuid) {
        if (!(uuid instanceof UUID)) { return false; }
        for (var i = 0; i < 6; i++) {
            if (this.intFields[i] !== uuid.intFields[i]) { return false; }
        }
        return true;
    };

// }}}

// UUID Version 1 Component {{{

    /**
     * Generates a version 1 {@link UUID}.
     * @returns {UUID} A version 1 {@link UUID} object.
     * @since 3.0
     */
    UUID.genV1 = function() {
        var now = new Date().getTime(), st = UUID._state;
        if (now != st.timestamp) {
            if (now < st.timestamp) { st.sequence++; }
            st.timestamp = now;
            st.tick = UUID._getRandomInt(4);
        } else if (Math.random() < UUID._tsRatio && st.tick < 9984) {
            // advance the timestamp fraction at a probability
            // to compensate for the low timestamp resolution
            st.tick += 1 + UUID._getRandomInt(4);
        } else {
            st.sequence++;
        }

        // format time fields
        var tf = UUID._getTimeFieldValues(st.timestamp);
        var tl = tf.low + st.tick;
        var thav = (tf.hi & 0xFFF) | 0x1000;  // set version '0001'

        // format clock sequence
        st.sequence &= 0x3FFF;
        var cshar = (st.sequence >>> 8) | 0x80; // set variant '10'
        var csl = st.sequence & 0xFF;

        return new UUID()._init(tl, tf.mid, thav, cshar, csl, st.node);
    };

    /**
     * Re-initializes version 1 UUID state.
     * @since 3.0
     */
    UUID.resetState = function() {
        UUID._state = new UUID._state.constructor();
    };

    /**
     * Probability to advance the timestamp fraction: the ratio of tick movements to sequence increments.
     * @type float
     */
    UUID._tsRatio = 1 / 4;

    /**
     * Persistent state for UUID version 1.
     * @type UUIDState
     */
    UUID._state = new function UUIDState() {
        var rand = UUID._getRandomInt;
        this.timestamp = 0;
        this.sequence = rand(14);
        this.node = (rand(8) | 1) * 0x10000000000 + rand(40); // set multicast bit '1'
        this.tick = rand(4);  // timestamp fraction smaller than a millisecond
    };

    /**
     * @param {Date|int} time ECMAScript Date Object or milliseconds from 1970-01-01.
     * @returns {object}
     */
    UUID._getTimeFieldValues = function(time) {
        var ts = time - Date.UTC(1582, 9, 15);
        var hm = ((ts / 0x100000000) * 10000) & 0xFFFFFFF;
        return  { low: ((ts & 0xFFFFFFF) * 10000) % 0x100000000,
            mid: hm & 0xFFFF, hi: hm >>> 16, timestamp: ts };
    };

// }}}

// Misc. Component {{{

    /**
     * Reinstalls {@link UUID.generate} method to emulate the interface of uuid.js version 2.x.
     * @since 3.1
     * @deprecated Version 2.x. compatible interface is not recommended.
     */
    UUID.makeBackwardCompatible = function() {
        var f = UUID.generate;
        UUID.generate = function(o) {
            return (o && o.version == 1) ? UUID.genV1().hexString : f.call(UUID);
        };
        UUID.makeBackwardCompatible = function() {};
    };

    /**
     * Preserves the value of 'UUID' global variable set before the load of uuid.js.
     * @since 3.2
     * @type object
     */
    UUID.overwrittenUUID = overwrittenUUID;

// }}}

    return UUID;

})(UUID);

// vim: et ts=2 sw=2 fdm=marker fmr&
/** Zet.js Module from https://github.com/nemisj/Zet.js
 Handles inheritance and factory function registration/creation/type-checking
 This is a fork from the original, with updates and enhancements as noted.
 Revised by: Benjamin Nye
 Package: SuperGLU
 License: APL 2.0

 Notes:
 - Fixes to update it to newer versions of JS (was outdated).
 - Added class factory function for automatically registering and creating Zet objects
 - Expanded isInstance functionality for type-checking of class
 - Fixed function inheritance functionality for newer JS versions
 */
if (typeof SuperGLU === "undefined"){
    var SuperGLU = {};
    if (typeof window === "undefined") {
        var window = this;
    }
    window.SuperGLU = SuperGLU;
}

(function(){
    // GLOBAL is the reference in nodejs implementation to the global scope
    // node.js supports Modules specs, so, Zet will go into separate scope
    var globalscope = (typeof(GLOBAL) == "undefined") ? window : GLOBAL;

    // Scope which is the entry point for Classes declaration;
    var declarescope = globalscope;

    // support for CommonJS Modules 1.0 API
    // Zet.js can be include as CommonJS module, by calling
    // var Zet = require('Zet.js');
    var _c = (typeof(exports) != "undefined") ? exports : (globalscope.Zet = function Zet(){
        if(arguments.length == 1){
            var sub = arguments[0];
            return sub.instanceOf ? sub : {
                instanceOf : function(superclass){
                    return (typeof sub == "string") ? superclass == String : sub instanceof superclass;
                }
            };
        }else if(arguments.length == 2){
            return Zet.declare(arguments[0], arguments[1]);
        }
    });

    // cache for undefined
    var undef;

    //logger provider
    var logger;


    // Factory Map (in form ClassId : Class Factory)
    var _FACTORY_MAP = {};

    // Utility Functions
    function prepareArgs(args){
        var i;
        var result = [];
        if(args && args.length){
            for(i=0;i < args.length;i++){
                result.push(args[i]);
            }
        }
        return result;
    }

    function mixin(obj, prop){
        var key;
        if(typeof(prop) == "object"){
            for(key in prop){
                if(prop.hasOwnProperty(key)){
                    obj[key] = prop[key];
                }
            }
        }

        return obj;
    }

    function inherited(currentFnc, args){
        var inheritedFnc = currentFnc.__chain;
        if(inheritedFnc && (typeof(inheritedFnc) == "function")){
            var a = prepareArgs(args);
            return inheritedFnc.apply(globalscope, a);
        }
    }

    function runConstruct(instance, params){
        var construct = instance.construct;
        if(construct && typeof(construct) == "function"){
            construct.apply(globalscope, params);
        }
        return instance;
    }

    _c.declare = function(className, kwArgs) {

        // className ommited for anonymous declaration
        if(arguments.length == 1){
            kwArgs    = className;
            className = null;
        }

        var superclass = kwArgs.superclass;
        var defineBody = kwArgs.defineBody;
        var CLASS_ID = kwArgs.CLASS_ID;
        if (CLASS_ID == null) { CLASS_ID = className; }

        if (superclass && typeof(superclass) != "function") {
            throw new Error("Zet.declare : Superclass of " + className + " is not a constructor.");
        } else if (defineBody !== undef && (typeof(defineBody) != "function")) {
            throw new Error("Zet.declare : defineBody of " + className + " is not a function.");
        } else if (CLASS_ID !== undef && (typeof(CLASS_ID) != 'string')) {
            throw new Error("Zet.declare : CLASS_ID of " + className + " is not a string.");
        }

        var instanceOf = function instanceOf(clazz){
            if(clazz == create){
                return true;
            }else if(superclass){
                //one level deep
                if (superclass.instanceOf){
                    return superclass.instanceOf(clazz);
                } else {
                    return superclass == clazz;
                }
            } else {
                return false;
            }
        };

        var isInstance = function isInstance(instance) {
            var constructor;
            if (instance == null){
                return false;
            }
            constructor = instance.constructor;
            if ((typeof constructor === "undefined") ||
                (!((constructor instanceof Function) ||
                    (constructor instanceof Object))) ||
                (instance.__zet__makeNew == null)){
                return false;
                // Exact Match
            } else if (instance.constructor == create){
                return true;
            } else if (instance.instanceOf instanceof Function) {
                return instance.instanceOf(create);
            } else {
                return false;
            }
        };

        // Function that makes a new (uninitialized) instance
        var __zet__makeNew = function __zet__makeNew(){
            var params = prepareArgs(arguments);

            var superStore  = null;
            var self        = null;

            if(superclass){
                // protection against outside calls
                var superi = superclass.__zet__makeNew(create);
                if(superi === null){
                    //throw or warning
                    throw new Error("Zet.declare : Superclass of " + className + " should return object.");
                }

                // mixin all functions into superStore, for inheritance
                superStore = mixin({}, superi);
                self = superi;
            }

            self  = self || {}; // testing if the object already exists;

            if(defineBody){
                var proto = null;
                try{
                    proto = defineBody(self);
                }catch(e){
                    if(e.__publicbody){
                        proto = e.__seeding;
                    }else{
                        throw e;
                    }
                }

                if(proto){
                    //some extra arguments are here
                    mixin(self, proto);
                }
            }

            // doing inheritance stuff
            if(superStore){
                for(var i in superStore){
                    if((self[i] != superStore[i]) && (typeof(superStore[i]) == "function" && typeof(self[i]) == "function")){
                        //name collisions, apply __chain trick
                        self[i].__chain = superStore[i];
                    }
                }
            }

            // adding helper functions
            mixin(self, {
                className   : className,
                CLASS_ID	: CLASS_ID,
                inherited   : inherited,
                instanceOf  : instanceOf,
                isInstance  : isInstance,
                __zet__makeNew : __zet__makeNew,
                public      : _c.public,
                constructor : create // for var self = bla.constructor();
            });
            return self;
        };

        // Factory function that creates initialized instances
        var create = function create(){
            var params = prepareArgs(arguments);
            var self = __zet__makeNew(params);
            self = runConstruct(self, params);
            return self;
        };

        // Data available on the Class Factory function
        create.instanceOf = instanceOf;
        create.isInstance = isInstance;
        create.__zet__makeNew = __zet__makeNew;
        create.className = className;
        create.CLASS_ID	= CLASS_ID;
        // If CLASS_ID given, add class to factory
        if (CLASS_ID){
            _c.setFactoryClass(CLASS_ID, create);
        }
        // in case for anonymous Classes declaration check for className
        return className ? _c.setClass(className, create) : create;
    };

    // Zet Public Module Functions
    _c.public = function(body){
        var error = new Error('');
        error.__seeding = body;
        error.__publicbody = true;
        throw error;
    };

    _c.profile = function(kwArgs){
        if(kwArgs.scope){
            declarescope = kwArgs.scope;
        }

        if(kwArgs.logger){
            logger = kwArgs.logger;
        }
    };

    // Zet Class Factory for Module-Based Access
    _c.getClass = function(className){
        var curr  = declarescope;

        var split = className.split(".");
        for(var i=0; i < split.length; i++){
            if(curr[split[i]]){
                curr =  curr[split[i]];
            } else {
                throw new Error("Zet.getClass: Can't find class: " + className);
            }
        }

        return curr;
    };

    _c.setClass = function(className, constructor){
        var curr  = declarescope;
        var split = className.split(".");
        for(var i=0;i<split.length-1;i++){
            curr = curr[split[i]] ? curr[split[i]] : (curr[split[i]] = {});
        }

        return (curr[split[split.length-1]] = constructor);
    };

    _c.hasFactoryClass = function(classId){
        return (classId in _FACTORY_MAP);
    };

    _c.getFactoryClass = function(classId){
        return _FACTORY_MAP[classId];
    };

    _c.setFactoryClass = function(classId, classRef){
        // print("ADD TO FACTORY: " + classId + " / " + classRef.className + " / "+ classRef);
        if (classId in _FACTORY_MAP){
            throw new Error("Error: Factory Map already contains class id: " + classId);
        }
        _FACTORY_MAP[classId] = classRef;
        // print("FACTORY MAP:" + Object.keys(_FACTORY_MAP));
    };

    //
    // Logging facilities
    //

    // default logger
    logger = {
        log : function(){
            if(globalscope.console && console.log){
                console.log.apply(console, arguments);
            }else if(window && window.document){
                var div= document.createElement("div");
                document.body.appendChild(div);
                var str = '';
                for(var i=0;i< arguments.length;i++){
                    str += (arguments[i] + ' ');
                }
                div.innerHTML = str;
            }
        },

        error : function(){
            if(globalscope.console && console.error){
                console.error.apply(console, arguments);
            }else if(window && window.document){
                var div= document.createElement("div");
                document.body.appendChild(div);
                var str = '';
                for(var i=0;i< arguments.length;i++){
                    str += (arguments[i] + ' ');
                }
                div.innerHTML = str;
                div.style.color = 'red';
            }
        }
    };

    _c.level = function(lvl){
        if(logger && logger.level){
            logger.level(lvl);
        }
    };

    _c.log = function(){
        if(logger && logger.log){
            logger.log.apply(logger,arguments);
        }
    };

    _c.error = function(){
        if(logger && logger.error){
            logger.error.apply(logger,arguments);
        }
    };

})();
SuperGLU.Zet = Zet;
/** SuperGLU (Generalized Learning Utilities) Standard API
 This manages all versioning within the core libraries.

 Package: SuperGLU (Generalized Learning Utilities)
 Author: Benjamin Nye
 License: APL 2.0

 Requires:
 - Util\uuid.js
 - Util\zet.js
 - Util\serializable.js
 - Core\messaging.js
 - Core\messaging-gateways.js
 **/

if (typeof window === "undefined") {
    var window = this;
}

(function(namespace, undefined) {
    namespace.version = "0.1.9";

// Core API Modules
    if ((namespace.Zet == null) && typeof Zet !== 'undefined'){
        namespace.Zet = Zet;
    }
    if ((namespace.Serialization == null) && typeof Serialization !== 'undefined'){
        namespace.Serialization = Serialization;
    }
    if ((namespace.Messaging == null) && typeof Messaging !== 'undefined'){
        namespace.Messaging = Messaging;
    }
    if ((namespace.Messaging_Gateway == null) && typeof Messaging_Gateway !== 'undefined'){
        namespace.Messaging_Gateway = Messaging_Gateway;
    }

// Sets to monitor registered verbs and context keys in this context
    if (namespace.VERBS == null){ namespace.VERBS = {}; }
    if (namespace.CONTEXT_KEYS == null){ namespace.CONTEXT_KEYS = {}; }

})(window.SuperGLU = window.SuperGLU || {});
/** Serialization Package for recursively serializing objects in a canonical format
 intended for class factory instantiation across different languages and systems.
 Package: SuperGLU
 Authors: Benjamin Nye and Daqi Dong
 License: APL 2.0
 Requires:
 - uuid.js
 - zet.js

 Description:
 -----------------------------------
 This package is intended to allow serializing and unserializing
 between JavaScript objects and various serial/string representations (e.g., JSON, XML).
 The following objects are included:
 * Serializable: Base class for serializable objects, needed for custom serialization
 * StorageToken: Intermediate representation of a serializable object
 * TokenRWFormats: Serializes and recovers storage tokens and primatives to specific formats (e.g., JSON)
 **/

if (typeof SuperGLU === "undefined"){
    var SuperGLU = {};
    if (typeof window === "undefined") {
        var window = this;
    }
    window.SuperGLU = SuperGLU;
}

// Module Declaration
(function (namespace, undefined) {

    var MAP_STRING = "map",
        LIST_STRING = 'list';

    var NAME_KEY = 'name';

    // Format Constants
    var JSON_FORMAT = 'json',
        XML_FORMAT = 'xml',
        VALID_SERIAL_FORMATS = [JSON_FORMAT, XML_FORMAT];

    /** Utility function to merge two mappings
     @param targetObj: Object to have key-value pairs added
     @param sourceObj: Object to take keys from
     @return: Modified version of the targetObj
     **/
    var updateObjProps = function(targetObj, sourceObj){
        var key;
        for (key in sourceObj){
            targetObj[key] = sourceObj[key];
        }
        return targetObj;
    };

    // Base classes for serializable objects
    //---------------------------------------------

    /** Class Serializable
     A serializable object, that can be saved to token and opened from token
     **/
    Zet.declare('Serializable', {
        superclass : null,
        defineBody : function(self){
            // Constructor Function

            /** Constructor for serializable
             *   @param id (optional): GUID for this object.  If none given, a V4 random GUID is used.
             **/
            self.construct = function construct(id){
                if (id == null) {
                    self._id = UUID.genV4().toString();
                } else {
                    self._id = id;
                }
            };

            // Public Functions 
            /** Equality operator **/
            self.eq = function eq(other){
                return ((self.getClassId() == other.getClassId()) && (self.getId() == other.getId()));
            };

            /** Not-equal operator **/
            self.ne = function ne(other){
                return !(self.eq(other));
            };

            /** Get the ID for the serializable. Ideally unique. **/
            self.getId = function getId(){
                return self._id;
            };

            /** Update the id, either by setting a new one or generating a new random UUID
             @param id: The new id for the serializable.  If null/undefined, generates new random UUID
             **/
            self.updateId = function updateId(id){
                if (id === undefined) {
                    self._id = UUID.genV4().toString();
                } else {
                    self._id = id;
                }
            };

            /** Get the class name for this serializable **/
            self.getClassId = function getClassId(){
                return self.className;
            };

            /** Initialize serializable from token.
             @param token: The token form of the object.
             @param context (optional): Mutable context for the loading process. Defaults to null.
             */
            self.initializeFromToken = function initializeFromToken(token, context){
                self._id = token.getId();
            };

            /** Create and return a token form of the object that is valid to serialize **/
            self.saveToToken = function saveToToken(){
                var token = StorageToken(self.getId(), self.getClassId());
                return token;
            };

            /** Create a serialized version of this object **/
            self.saveToSerialized = function saveToSerialized(){
                return makeSerialized(self.saveToToken());
            };

            /** Create a clone of the object
             @param newId: Unless false or 0, give the new clone a different UUID
             @return: A new serializable object of the right class type.
             **/
            self.clone = function clone(newId){
                if (newId == null){ newId = true; }
                var s = makeSerialized(self.saveToToken());
                s = untokenizeObject(makeNative(s));
                if (newId){
                    s.updateId();
                }
                return s;
            };
        }
    });

    /** A Serializable with a given name that will be stored with it **/
    Zet.declare('NamedSerializable' , {
        superclass : Serializable,
        defineBody : function(self){
            // Constructor Function
            self.NAME_KEY = NAME_KEY;

            /** Constructor for named serializable
             *   @param id (optional): GUID for this object.  If none given, a V4 random GUID is used.
             *   @param name: The name for the object
             **/
            self.construct = function construct(id, name){
                if (name == null) { name=null;}
                self.inherited(construct, [id]);
                self._name = name;
            };

            /** Get the name for the object **/
            self.getName = function getName(){
                return self._name;
            };

            /** Set the name for the object **/
            self.setName = function setName(name){
                if (name == null){
                    name = null;
                } else if (name instanceof String || typeof name === 'string'){
                    self._name = name;
                } else {
                    throw new Error("Set name failed, was not a string.");
                }
            };

            /** Equality operator **/
            self.eq = function eq(other){
                return (self.inherited(eq, [other]) && (self._name === other._name));
            };

            self.initializeFromToken = function initializeFromToken(token, context){
                self.inherited(initializeFromToken, [token, context]);
                self._name = untokenizeObject(token.getitem(self.NAME_KEY, true, null), context);
            };

            self.saveToToken = function saveToToken(){
                var token = self.inherited(saveToToken);
                if (self._name != null){
                    token.setitem(self.NAME_KEY, tokenizeObject(self._name));
                }
                return token;
            };
        }
    });

    /** Class StorageToken
     An object that stores data in a form that can be serialized
     **/
    Zet.declare('StorageToken', {
        superclass : null,
        defineBody : function(self){
            // -- Class fields
            self.ID_KEY = 'id';
            self.CLASS_ID_KEY = 'classId';

            /** Constructor for storage token
             @param id (optional): GUID for this object.  If none given, a V4 random GUID is used.
             @param classId: The name of the class, as known by the class factory
             @param data: Object of key-value pairs to store for this token
             **/
            self.construct = function construct(id, classId, data) {
                /** Create a storage token, which can be directly serialized into a string
                 @param id (optional): A GUID for the storage token.  If none given, uses a V4 random GUID.
                 @param classId (optional): Id for the class that this StorageToken should create.  Defaults to null.
                 @param data (optional): Starting data for the token.  Either a map {} for an array of map pairs [[key, val]].
                 */
                var i;
                self._data = {};
                if (data !== undefined) {
                    //we are assuming that the data will either already
                    //be in a dictionary form ({key: value, key2: value2, ...}) 
                    //or is in a sequence form ([[key, value], [key2, value2], ...])
                    if (data instanceof Array){ //[[key, value], [key2, value2], ...]
                        for (i in data){
                            if ((data[i] instanceof Array) && (data[i].length == 2)){
                                self._data[data[i][0]] = data[i][1];
                            } else {
                                throw new TypeError("Input array doesn't follow the format of [[key, value], [key2, value2], ...]");
                            }
                        }
                    } else {// {key: value, key2: value2, ...}
                        self._data = data;
                    }
                }else {
                    self._data = {};
                }
                if (id !== undefined){
                    self.setId(id);
                } else if ((self.getId() === undefined)){
                    self.setId(UUID.genV4().toString());
                }
                if (classId !== undefined) {
                    self.setClassId(classId);
                }
            };

            // -- Instance methods

            /** Get the ID for the storage token **/
            self.getId = function getId(){
                return self._data[self.ID_KEY];
            };

            /** Set the ID for the storage token **/
            self.setId = function setId(value){
                self._data[self.ID_KEY] = value;
            };

            /** Get the class name for the storage token **/
            self.getClassId = function getClassId(){
                return self._data[self.CLASS_ID_KEY];
            };

            /** Set the class name for the storage token **/
            self.setClassId = function setClassId(value){
                self._data[self.CLASS_ID_KEY] = value;
            };

            // Convenience Accessor for Named Serializables

            /** Get the name for the storage token (might be null) **/
            self.getName = function getName(){
                if (NAME_KEY in self._data){
                    return self._data[NAME_KEY];
                } else {
                    return null;
                }
            };

            /** Set a name for the storage token **/
            self.setName = function setName(value){
                self._data[NAME_KEY] = value;
            };

            // -- ##Generic Accessors

            /** Get the number of data values in the storage token **/
            self.len = function len(){
                return self._data.length;
            };

            /** Check if a given key is contained in the storage token **/
            self.contains = function contains(key){
                return key in self._data;
            };

            /** Get an item from the data dictionary
             @param key: Key for the item
             @param hasDefault (optional): If True, give a default value.  Else, raise an error if key not found.
             @param defaults (optional): The optional value for this item.
             */
            self.getitem = function getitem(key, hasDefault, defaults){

                if (!(key in self._data) && (hasDefault)){
                    return defaults;
                }else {
                    return self._data[key];
                }
            };

            /** Set an item in the data dictionary **/
            self.setitem = function setitem(key, value){
                self._data[key] = value;
            };

            /** Delete an item in the data dictionary **/
            self.delitem = function delitem(key){
                delete self._data[key];
            };

            /** Return an iterator over the data keys **/
            self.__iterator__ = function __iterator__(){
                var keys = Object.keys(self._data).sort();
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

            /** Return the data keys **/
            self.keys = function keys(){
                var k, aKeys;
                aKeys = [];
                for (k in self._data){
                    aKeys.push(k);
                }
                return aKeys;
            };

            // -- ##Comparison
            /** Equality operator **/
            self.eq = function eq(other){
                return (typeof(self) == typeof(other)) && (self._data == other._data);
            };

            /** Not equal operator **/
            self.ne = function ne(other){
                return !(self.eq(other));
            };

            // -- ##Validation
            /** Check if a key would be a valid data key **/
            self.isValidKey = function isValidKey(key){
                return typeof(key) in self.VALID_KEY_TYPES;
            };

            /** Check if a value would be a valid data value **/
            self.isValidValue = function isValidValue(value){
                return typeof(value) in self.VALID_VALUE_TYPES;
            };

            /** Check that the ID, Class Name, and any Name are valid types **/
            self.isValid = function isValid(){
                var idKey;
                var classIdKey;

                //Check that ID is valid
                if ((self._data[self.ID_KEY] == null) ||
                    ((typeof(self._data[self.ID_KEY]) !== 'string') &&
                        (typeof(self._data[self.ID_KEY]) !== 'number'))) {
                    return false;
                }
                //Check that class name is valid
                if ((self._data[self.CLASS_ID_KEY] == null) ||
                    (typeof(self._data[self.CLASS_ID_KEY]) !== 'string')) {
                    return false;
                }
                // Check that the name (if it exists) is valid
                if ((self._data[NAME_KEY] != null) &&
                    (typeof(self._data[NAME_KEY]) !== 'string')) {
                    return false;
                }
                return true;
            };
        }
    });

    //-------------------------------------------
    // Packing and Unpacking from Serial Formats
    //-------------------------------------------
    /** Base class for serializing or unserializing a token to a string **/
    Zet.declare('TokenRWFormat', {
        superclass : null,
        defineBody : function(self){
            // Public Class Properties

            // Valid Types in Storage Token
            self.VALID_KEY_TYPES = {'string': true};
            self.VALID_ATOMIC_VALUE_TYPES = {'number': true, 'string': true, 'boolean': true, 'undefined': true};
            self.VALID_SEQUENCE_VALUE_TYPES = {'list': true, 'tuple' : true};
            self.VALID_MAPPING_VALUE_TYPES = {'map': true};
            self.VALID_VALUE_TYPES = {};

            // Setup for Class Properties
            self.VALID_VALUE_TYPES = updateObjProps(self.VALID_VALUE_TYPES, self.VALID_ATOMIC_VALUE_TYPES);
            self.VALID_VALUE_TYPES = updateObjProps(self.VALID_VALUE_TYPES, self.VALID_SEQUENCE_VALUE_TYPES);
            self.VALID_VALUE_TYPES = updateObjProps(self.VALID_VALUE_TYPES, self.VALID_MAPPING_VALUE_TYPES);
            self.VALID_VALUE_TYPES.StorageToken = true;

            // Constructor method
            self.construct = function construct(){};

            // Public methods
            self.parse = function parse(string) {
                // Parse a string into javascript objects
                throw new Error("NotImplementedError");
            };

            self.serialize = function serialize(data) {
                // Serialize javascript objects into a string form
                throw new Error("NotImplementedError");
            };
        }
    });


    /** JSON Formatted String: Uses JSON.stringify/JSON.parse **/
    Zet.declare('JSONRWFormat', {
        superclass : TokenRWFormat,
        defineBody : function(self){

            // Constructor method
            self.construct = function construct(){};

            // Public methods

            /** Parse a JSON-formatted string into basic javascript objects
             (e.g., strings, numeric, arrays, objects)
             **/
            self.parse = function parse(String) {//Parse a JSON string into javascript objects
                var decoded = JSON.parse(String);
                return self.makeNative(decoded);
            };

            /** Turn basic javascript objects into a JSON string **/
            self.serialize = function serialize(data) {
                var serializable = self.makeSerializable(data);
                return JSON.stringify(serializable);
            };

            /** Recursively make all objects serializable into JSON,
             turning any lists, dicts, or StorageTokens into canonical forms
             **/
            self.makeSerializable = function makeSerializable(x){
                var i, key, keys, rt, temp, xType;
                xType = typeof(x);
                rt = null;
                // Primitive variables
                if ((xType in self.VALID_ATOMIC_VALUE_TYPES) || (x === null)){
                    rt = x;
                    // Array
                } else if (x instanceof Array){
                    rt = {};
                    temp = [];
                    for (i=0; i<x.length; i++) {
                        temp[i] = self.makeSerializable(x[i]);
                    }
                    rt[LIST_STRING] = temp;
                    // Object
                } else if ((x instanceof Object) &&
                    !(StorageToken.isInstance(x))){
                    rt = {};
                    temp = {};
                    for (key in x){
                        temp[key] = self.makeSerializable(x[key]);
                    }
                    rt[MAP_STRING] = temp;
                    // StorageToken
                } else if (StorageToken.isInstance(x)){
                    rt = {};
                    temp = {};
                    keys = x.keys();
                    for (i=0; i<keys.length; i++) {
                        temp[self.makeSerializable(keys[i])] = self.makeSerializable(x.getitem(keys[i]));
                    }
                    rt[x.getClassId()] = temp;
                    //Error
                } else {
                    throw new TypeError("Tried to serialize unserializable object of type (" + xType + "): " + x);
                }
                return rt;
            };

            /** Recursively turn raw javascript objects in a canonical format into
             primitives, arrays, mappings, and StorageTokens.
             **/
            self.makeNative = function makeNative(x){
                var i, key, rt, temp, xType, dataTypeName;
                xType = typeof(x);
                rt = null;
                // Primitive variables
                if ((self.VALID_ATOMIC_VALUE_TYPES[xType]) || (x == null)){
                    rt = x;
                    return rt;
                }
                for (dataTypeName in x){
                    break;
                }
                // Array
                if (dataTypeName in self.VALID_SEQUENCE_VALUE_TYPES){
                    rt = [];
                    for (i=0; i<x[dataTypeName].length; i++) {
                        rt[i] = self.makeNative(x[dataTypeName][i]);
                    }
                    // Object
                } else if (dataTypeName in self.VALID_MAPPING_VALUE_TYPES) {
                    rt = {};
                    for (key in x[dataTypeName]) {
                        rt[key] = self.makeNative(x[dataTypeName][key]);
                    }
                    // StorageToken (by default)
                } else {
                    rt = {};
                    rt[MAP_STRING] = x[dataTypeName];
                    rt = self.makeNative(rt);
                    rt = StorageToken(undefined, undefined, rt);
                }
                return rt;
            };
        }
    });

    var JSONRWFormatter = JSONRWFormat(),
        XMLRWFormat = null,
        XMLRWFormatter = null;

    /** Create a serializable instance from an arbitrary storage token
     @param token: Storage token
     @param context (optional): Mutable context for the loading process. Defaults to null.
     @param onMissingClass (optional): Function to transform/error on token if class missing
     */
    var createFromToken = function(token, context, onMissingClass){
        var classId, AClass;
        var id = token.getId();
        var instance = {};
        if ((context != null) && (id in context)){
            instance = context[id];
        } else {
            //Need to import the right class
            classId = token.getClassId();
            AClass = Zet.getFactoryClass(classId);
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

    /** What to do if a class is missing (error or console message) **/
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
    var serializeObject = function serializeObject(obj, sFormat){
        return makeSerialized(tokenizeObject(obj), sFormat);
    };

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
    var nativizeObject = function nativizeObject(obj, context, sFormat){
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

    /** Generic function to tokenize an object, recursively **/
    var tokenizeObject = function (obj) {
        var i, key, rt;
        rt = null;
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

    /** Generic function to create an object from a token
     @param obj: Object to turn from tokens into object
     @param context (optional): Mutable context for the loading process. Defaults to null.
     */
    var untokenizeObject = function(obj, context){
        var i, key;
        var rt = null;
        if (StorageToken.isInstance(obj)) {// StorageToken
            rt = createFromToken(obj, context);
        } else if (obj instanceof Array) { // Array
            rt = [];
            for (i in obj) {
                rt[i] = untokenizeObject(obj[i], context);
            }
        } else if ((obj instanceof Object) &&
            !(obj instanceof Array)){ // Object
            rt = {};
            for (key in obj) {
                rt[untokenizeObject(key, context)] = untokenizeObject(obj[key], context);
            }
        } else {
            rt = obj;
        }
        return rt;
    };

    // Convenience functions to serialize and unserialize tokens and raw data
    //---------------------------------------------
    /** Generic function to turn a tokenized object into serialized form
     @param obj: Tokenized object
     @param sFormat (optional): Serialization format.  Defaults to JSON_FORMAT
     */
    var makeSerialized = function makeSerialized(obj, sFormat){
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

    /** Generic function to turn a serialized string into a tokenized object
     *   @param String: Serialized object, as a string
     *   @param sFormat (optional): Serialization format.  Defaults to JSON_FORMAT
     */
    var makeNative = function makeNative(String, sFormat){
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
    namespace.JSON_FORMAT = JSON_FORMAT;
    namespace.XML_FORMAT = XML_FORMAT;
    namespace.VALID_SERIAL_FORMATS = VALID_SERIAL_FORMATS;

    // Expose Functions Publicly
    namespace.createFromToken = createFromToken;
    namespace.serializeObject = serializeObject;
    namespace.nativizeObject = nativizeObject;
    namespace.makeSerialized = makeSerialized;
    namespace.makeNative = makeNative;
    namespace.tokenizeObject = tokenizeObject;
    namespace.untokenizeObject = untokenizeObject;

    // Expose Classes Publicly
    namespace.Serializable = Serializable;
    namespace.NamedSerializable = NamedSerializable;
    namespace.StorageToken = StorageToken;
    namespace.TokenRWFormat = TokenRWFormat;
    namespace.JSONRWFormat = JSONRWFormat;
    //namespace.XMLRWFormat = XMLRWFormat;

    // Expose Instances Publicly
    namespace.JSONRWFormatter = JSONRWFormatter;
    //namespace.XMLRWFormatter = XMLRWFormatter;

    SuperGLU.Serialization = namespace;
})(window.Serialization = window.Serialization || {});

!function (e) {
    if ("object" == typeof exports && "undefined" != typeof module) module.exports = e(); else if ("function" == typeof define && define.amd) define([], e); else {
        var f;
        "undefined" != typeof window ? f = window : "undefined" != typeof global ? f = global : "undefined" != typeof self && (f = self), f.io = e()
    }
}(function () {
    var define, module, exports;
    return function e(t, n, r) {
        function s(o, u) {
            if (!n[o]) {
                if (!t[o]) {
                    var a = typeof require == "function" && require;
                    if (!u && a) return a(o, !0);
                    if (i) return i(o, !0);
                    throw new Error("Cannot find module '" + o + "'")
                }
                var f = n[o] = {exports: {}};
                t[o][0].call(f.exports, function (e) {
                    var n = t[o][1][e];
                    return s(n ? n : e)
                }, f, f.exports, e, t, n, r)
            }
            return n[o].exports
        }

        var i = typeof require == "function" && require;
        for (var o = 0; o < r.length; o++) s(r[o]);
        return s
    }({
        1: [function (_dereq_, module, exports) {
            module.exports = _dereq_("./lib/")
        }, {"./lib/": 2}],
        2: [function (_dereq_, module, exports) {
            var url = _dereq_("./url");
            var parser = _dereq_("socket.io-parser");
            var Manager = _dereq_("./manager");
            var debug = _dereq_("debug")("socket.io-client");
            module.exports = exports = lookup;
            var cache = exports.managers = {};

            function lookup(uri, opts) {
                if (typeof uri == "object") {
                    opts = uri;
                    uri = undefined
                }
                opts = opts || {};
                var parsed = url(uri);
                var source = parsed.source;
                var id = parsed.id;
                var io;
                if (opts.forceNew || opts["force new connection"] || false === opts.multiplex) {
                    debug("ignoring socket cache for %s", source);
                    io = Manager(source, opts)
                } else {
                    if (!cache[id]) {
                        debug("new io instance for %s", source);
                        cache[id] = Manager(source, opts)
                    }
                    io = cache[id]
                }
                return io.socket(parsed.path)
            }

            exports.protocol = parser.protocol;
            exports.connect = lookup;
            exports.Manager = _dereq_("./manager");
            exports.Socket = _dereq_("./socket")
        }, {"./manager": 3, "./socket": 5, "./url": 6, debug: 9, "socket.io-parser": 40}],
        3: [function (_dereq_, module, exports) {
            var url = _dereq_("./url");
            var eio = _dereq_("engine.io-client");
            var Socket = _dereq_("./socket");
            var Emitter = _dereq_("component-emitter");
            var parser = _dereq_("socket.io-parser");
            var on = _dereq_("./on");
            var bind = _dereq_("component-bind");
            var object = _dereq_("object-component");
            var debug = _dereq_("debug")("socket.io-client:manager");
            module.exports = Manager;

            function Manager(uri, opts) {
                if (!(this instanceof Manager)) return new Manager(uri, opts);
                if (uri && "object" == typeof uri) {
                    opts = uri;
                    uri = undefined
                }
                opts = opts || {};
                opts.path = opts.path || "/socket.io";
                this.nsps = {};
                this.subs = [];
                this.opts = opts;
                this.reconnection(opts.reconnection !== false);
                this.reconnectionAttempts(opts.reconnectionAttempts || Infinity);
                this.reconnectionDelay(opts.reconnectionDelay || 1e3);
                this.reconnectionDelayMax(opts.reconnectionDelayMax || 5e3);
                this.timeout(null == opts.timeout ? 2e4 : opts.timeout);
                this.readyState = "closed";
                this.uri = uri;
                this.connected = 0;
                this.attempts = 0;
                this.encoding = false;
                this.packetBuffer = [];
                this.encoder = new parser.Encoder;
                this.decoder = new parser.Decoder;
                this.autoConnect = opts.autoConnect !== false;
                if (this.autoConnect) this.open()
            }

            Manager.prototype.emitAll = function () {
                this.emit.apply(this, arguments);
                for (var nsp in this.nsps) {
                    this.nsps[nsp].emit.apply(this.nsps[nsp], arguments)
                }
            };
            Emitter(Manager.prototype);
            Manager.prototype.reconnection = function (v) {
                if (!arguments.length) return this._reconnection;
                this._reconnection = !!v;
                return this
            };
            Manager.prototype.reconnectionAttempts = function (v) {
                if (!arguments.length) return this._reconnectionAttempts;
                this._reconnectionAttempts = v;
                return this
            };
            Manager.prototype.reconnectionDelay = function (v) {
                if (!arguments.length) return this._reconnectionDelay;
                this._reconnectionDelay = v;
                return this
            };
            Manager.prototype.reconnectionDelayMax = function (v) {
                if (!arguments.length) return this._reconnectionDelayMax;
                this._reconnectionDelayMax = v;
                return this
            };
            Manager.prototype.timeout = function (v) {
                if (!arguments.length) return this._timeout;
                this._timeout = v;
                return this
            };
            Manager.prototype.maybeReconnectOnOpen = function () {
                if (!this.openReconnect && !this.reconnecting && this._reconnection && this.attempts === 0) {
                    this.openReconnect = true;
                    this.reconnect()
                }
            };
            Manager.prototype.open = Manager.prototype.connect = function (fn) {
                debug("readyState %s", this.readyState);
                if (~this.readyState.indexOf("open")) return this;
                debug("opening %s", this.uri);
                this.engine = eio(this.uri, this.opts);
                var socket = this.engine;
                var self = this;
                this.readyState = "opening";
                var openSub = on(socket, "open", function () {
                    self.onopen();
                    fn && fn()
                });
                var errorSub = on(socket, "error", function (data) {
                    debug("connect_error");
                    self.cleanup();
                    self.readyState = "closed";
                    self.emitAll("connect_error", data);
                    if (fn) {
                        var err = new Error("Connection error");
                        err.data = data;
                        fn(err)
                    }
                    self.maybeReconnectOnOpen()
                });
                if (false !== this._timeout) {
                    var timeout = this._timeout;
                    debug("connect attempt will timeout after %d", timeout);
                    var timer = setTimeout(function () {
                        debug("connect attempt timed out after %d", timeout);
                        openSub.destroy();
                        socket.close();
                        socket.emit("error", "timeout");
                        self.emitAll("connect_timeout", timeout)
                    }, timeout);
                    this.subs.push({
                        destroy: function () {
                            clearTimeout(timer)
                        }
                    })
                }
                this.subs.push(openSub);
                this.subs.push(errorSub);
                return this
            };
            Manager.prototype.onopen = function () {
                debug("open");
                this.cleanup();
                this.readyState = "open";
                this.emit("open");
                var socket = this.engine;
                this.subs.push(on(socket, "data", bind(this, "ondata")));
                this.subs.push(on(this.decoder, "decoded", bind(this, "ondecoded")));
                this.subs.push(on(socket, "error", bind(this, "onerror")));
                this.subs.push(on(socket, "close", bind(this, "onclose")))
            };
            Manager.prototype.ondata = function (data) {
                this.decoder.add(data)
            };
            Manager.prototype.ondecoded = function (packet) {
                this.emit("packet", packet)
            };
            Manager.prototype.onerror = function (err) {
                debug("error", err);
                this.emitAll("error", err)
            };
            Manager.prototype.socket = function (nsp) {
                var socket = this.nsps[nsp];
                if (!socket) {
                    socket = new Socket(this, nsp);
                    this.nsps[nsp] = socket;
                    var self = this;
                    socket.on("connect", function () {
                        self.connected++
                    })
                }
                return socket
            };
            Manager.prototype.destroy = function (socket) {
                --this.connected || this.close()
            };
            Manager.prototype.packet = function (packet) {
                debug("writing packet %j", packet);
                var self = this;
                if (!self.encoding) {
                    self.encoding = true;
                    this.encoder.encode(packet, function (encodedPackets) {
                        for (var i = 0; i < encodedPackets.length; i++) {
                            self.engine.write(encodedPackets[i])
                        }
                        self.encoding = false;
                        self.processPacketQueue()
                    })
                } else {
                    self.packetBuffer.push(packet)
                }
            };
            Manager.prototype.processPacketQueue = function () {
                if (this.packetBuffer.length > 0 && !this.encoding) {
                    var pack = this.packetBuffer.shift();
                    this.packet(pack)
                }
            };
            Manager.prototype.cleanup = function () {
                var sub;
                while (sub = this.subs.shift()) sub.destroy();
                this.packetBuffer = [];
                this.encoding = false;
                this.decoder.destroy()
            };
            Manager.prototype.close = Manager.prototype.disconnect = function () {
                this.skipReconnect = true;
                this.engine.close()
            };
            Manager.prototype.onclose = function (reason) {
                debug("close");
                this.cleanup();
                this.readyState = "closed";
                this.emit("close", reason);
                if (this._reconnection && !this.skipReconnect) {
                    this.reconnect()
                }
            };
            Manager.prototype.reconnect = function () {
                if (this.reconnecting) return this;
                var self = this;
                this.attempts++;
                if (this.attempts > this._reconnectionAttempts) {
                    debug("reconnect failed");
                    this.emitAll("reconnect_failed");
                    this.reconnecting = false
                } else {
                    var delay = this.attempts * this.reconnectionDelay();
                    delay = Math.min(delay, this.reconnectionDelayMax());
                    debug("will wait %dms before reconnect attempt", delay);
                    this.reconnecting = true;
                    var timer = setTimeout(function () {
                        debug("attempting reconnect");
                        self.emitAll("reconnect_attempt", self.attempts);
                        self.emitAll("reconnecting", self.attempts);
                        self.open(function (err) {
                            if (err) {
                                debug("reconnect attempt error");
                                self.reconnecting = false;
                                self.reconnect();
                                self.emitAll("reconnect_error", err.data)
                            } else {
                                debug("reconnect success");
                                self.onreconnect()
                            }
                        })
                    }, delay);
                    this.subs.push({
                        destroy: function () {
                            clearTimeout(timer)
                        }
                    })
                }
            };
            Manager.prototype.onreconnect = function () {
                var attempt = this.attempts;
                this.attempts = 0;
                this.reconnecting = false;
                this.emitAll("reconnect", attempt)
            }
        }, {
            "./on": 4,
            "./socket": 5,
            "./url": 6,
            "component-bind": 7,
            "component-emitter": 8,
            debug: 9,
            "engine.io-client": 10,
            "object-component": 37,
            "socket.io-parser": 40
        }],
        4: [function (_dereq_, module, exports) {
            module.exports = on;

            function on(obj, ev, fn) {
                obj.on(ev, fn);
                return {
                    destroy: function () {
                        obj.removeListener(ev, fn)
                    }
                }
            }
        }, {}],
        5: [function (_dereq_, module, exports) {
            var parser = _dereq_("socket.io-parser");
            var Emitter = _dereq_("component-emitter");
            var toArray = _dereq_("to-array");
            var on = _dereq_("./on");
            var bind = _dereq_("component-bind");
            var debug = _dereq_("debug")("socket.io-client:socket");
            var hasBin = _dereq_("has-binary");
            var indexOf = _dereq_("indexof");
            module.exports = exports = Socket;
            var events = {
                connect: 1,
                connect_error: 1,
                connect_timeout: 1,
                disconnect: 1,
                error: 1,
                reconnect: 1,
                reconnect_attempt: 1,
                reconnect_failed: 1,
                reconnect_error: 1,
                reconnecting: 1
            };
            var emit = Emitter.prototype.emit;

            function Socket(io, nsp) {
                this.io = io;
                this.nsp = nsp;
                this.json = this;
                this.ids = 0;
                this.acks = {};
                if (this.io.autoConnect) this.open();
                this.receiveBuffer = [];
                this.sendBuffer = [];
                this.connected = false;
                this.disconnected = true;
                this.subEvents()
            }

            Emitter(Socket.prototype);
            Socket.prototype.subEvents = function () {
                var io = this.io;
                this.subs = [on(io, "open", bind(this, "onopen")), on(io, "packet", bind(this, "onpacket")), on(io, "close", bind(this, "onclose"))]
            };
            Socket.prototype.open = Socket.prototype.connect = function () {
                if (this.connected) return this;
                this.io.open();
                if ("open" == this.io.readyState) this.onopen();
                return this
            };
            Socket.prototype.send = function () {
                var args = toArray(arguments);
                args.unshift("message");
                this.emit.apply(this, args);
                return this
            };
            Socket.prototype.emit = function (ev) {
                if (events.hasOwnProperty(ev)) {
                    emit.apply(this, arguments);
                    return this
                }
                var args = toArray(arguments);
                var parserType = parser.EVENT;
                if (hasBin(args)) {
                    parserType = parser.BINARY_EVENT
                }
                var packet = {type: parserType, data: args};
                if ("function" == typeof args[args.length - 1]) {
                    debug("emitting packet with ack id %d", this.ids);
                    this.acks[this.ids] = args.pop();
                    packet.id = this.ids++
                }
                if (this.connected) {
                    this.packet(packet)
                } else {
                    this.sendBuffer.push(packet)
                }
                return this
            };
            Socket.prototype.packet = function (packet) {
                packet.nsp = this.nsp;
                this.io.packet(packet)
            };
            Socket.prototype.onopen = function () {
                debug("transport is open - connecting");
                if ("/" != this.nsp) {
                    this.packet({type: parser.CONNECT})
                }
            };
            Socket.prototype.onclose = function (reason) {
                debug("close (%s)", reason);
                this.connected = false;
                this.disconnected = true;
                this.emit("disconnect", reason)
            };
            Socket.prototype.onpacket = function (packet) {
                if (packet.nsp != this.nsp) return;
                switch (packet.type) {
                    case parser.CONNECT:
                        this.onconnect();
                        break;
                    case parser.EVENT:
                        this.onevent(packet);
                        break;
                    case parser.BINARY_EVENT:
                        this.onevent(packet);
                        break;
                    case parser.ACK:
                        this.onack(packet);
                        break;
                    case parser.BINARY_ACK:
                        this.onack(packet);
                        break;
                    case parser.DISCONNECT:
                        this.ondisconnect();
                        break;
                    case parser.ERROR:
                        this.emit("error", packet.data);
                        break
                }
            };
            Socket.prototype.onevent = function (packet) {
                var args = packet.data || [];
                debug("emitting event %j", args);
                if (null != packet.id) {
                    debug("attaching ack callback to event");
                    args.push(this.ack(packet.id))
                }
                if (this.connected) {
                    emit.apply(this, args)
                } else {
                    this.receiveBuffer.push(args)
                }
            };
            Socket.prototype.ack = function (id) {
                var self = this;
                var sent = false;
                return function () {
                    if (sent) return;
                    sent = true;
                    var args = toArray(arguments);
                    debug("sending ack %j", args);
                    var type = hasBin(args) ? parser.BINARY_ACK : parser.ACK;
                    self.packet({type: type, id: id, data: args})
                }
            };
            Socket.prototype.onack = function (packet) {
                debug("calling ack %s with %j", packet.id, packet.data);
                var fn = this.acks[packet.id];
                fn.apply(this, packet.data);
                delete this.acks[packet.id]
            };
            Socket.prototype.onconnect = function () {
                this.connected = true;
                this.disconnected = false;
                this.emit("connect");
                this.emitBuffered()
            };
            Socket.prototype.emitBuffered = function () {
                var i;
                for (i = 0; i < this.receiveBuffer.length; i++) {
                    emit.apply(this, this.receiveBuffer[i])
                }
                this.receiveBuffer = [];
                for (i = 0; i < this.sendBuffer.length; i++) {
                    this.packet(this.sendBuffer[i])
                }
                this.sendBuffer = []
            };
            Socket.prototype.ondisconnect = function () {
                debug("server disconnect (%s)", this.nsp);
                this.destroy();
                this.onclose("io server disconnect")
            };
            Socket.prototype.destroy = function () {
                for (var i = 0; i < this.subs.length; i++) {
                    this.subs[i].destroy()
                }
                this.io.destroy(this)
            };
            Socket.prototype.close = Socket.prototype.disconnect = function () {
                if (!this.connected) return this;
                debug("performing disconnect (%s)", this.nsp);
                this.packet({type: parser.DISCONNECT});
                this.destroy();
                this.onclose("io client disconnect");
                return this
            }
        }, {
            "./on": 4,
            "component-bind": 7,
            "component-emitter": 8,
            debug: 9,
            "has-binary": 32,
            indexof: 36,
            "socket.io-parser": 40,
            "to-array": 44
        }],
        6: [function (_dereq_, module, exports) {
            (function (global) {
                var parseuri = _dereq_("parseuri");
                var debug = _dereq_("debug")("socket.io-client:url");
                module.exports = url;

                function url(uri, loc) {
                    var obj = uri;
                    var loc = loc || global.location;
                    if (null == uri) uri = loc.protocol + "//" + loc.hostname;
                    if ("string" == typeof uri) {
                        if ("/" == uri.charAt(0)) {
                            if ("undefined" != typeof loc) {
                                uri = loc.hostname + uri
                            }
                        }
                        if (!/^(https?|wss?):\/\//.test(uri)) {
                            debug("protocol-less url %s", uri);
                            if ("undefined" != typeof loc) {
                                uri = loc.protocol + "//" + uri
                            } else {
                                uri = "https://" + uri
                            }
                        }
                        debug("parse %s", uri);
                        obj = parseuri(uri)
                    }
                    if (!obj.port) {
                        if (/^(http|ws)$/.test(obj.protocol)) {
                            obj.port = "80"
                        } else if (/^(http|ws)s$/.test(obj.protocol)) {
                            obj.port = "443"
                        }
                    }
                    obj.path = obj.path || "/";
                    obj.id = obj.protocol + "://" + obj.host + ":" + obj.port;
                    obj.href = obj.protocol + "://" + obj.host + (loc && loc.port == obj.port ? "" : ":" + obj.port);
                    return obj
                }
            }).call(this, typeof self !== "undefined" ? self : typeof window !== "undefined" ? window : {})
        }, {debug: 9, parseuri: 38}],
        7: [function (_dereq_, module, exports) {
            var slice = [].slice;
            module.exports = function (obj, fn) {
                if ("string" == typeof fn) fn = obj[fn];
                if ("function" != typeof fn) throw new Error("bind() requires a function");
                var args = slice.call(arguments, 2);
                return function () {
                    return fn.apply(obj, args.concat(slice.call(arguments)))
                }
            }
        }, {}],
        8: [function (_dereq_, module, exports) {
            module.exports = Emitter;

            function Emitter(obj) {
                if (obj) return mixin(obj)
            }

            function mixin(obj) {
                for (var key in Emitter.prototype) {
                    obj[key] = Emitter.prototype[key]
                }
                return obj
            }

            Emitter.prototype.on = Emitter.prototype.addEventListener = function (event, fn) {
                this._callbacks = this._callbacks || {};
                (this._callbacks[event] = this._callbacks[event] || []).push(fn);
                return this
            };
            Emitter.prototype.once = function (event, fn) {
                var self = this;
                this._callbacks = this._callbacks || {};

                function on() {
                    self.off(event, on);
                    fn.apply(this, arguments)
                }

                on.fn = fn;
                this.on(event, on);
                return this
            };
            Emitter.prototype.off = Emitter.prototype.removeListener = Emitter.prototype.removeAllListeners = Emitter.prototype.removeEventListener = function (event, fn) {
                this._callbacks = this._callbacks || {};
                if (0 == arguments.length) {
                    this._callbacks = {};
                    return this
                }
                var callbacks = this._callbacks[event];
                if (!callbacks) return this;
                if (1 == arguments.length) {
                    delete this._callbacks[event];
                    return this
                }
                var cb;
                for (var i = 0; i < callbacks.length; i++) {
                    cb = callbacks[i];
                    if (cb === fn || cb.fn === fn) {
                        callbacks.splice(i, 1);
                        break
                    }
                }
                return this
            };
            Emitter.prototype.emit = function (event) {
                this._callbacks = this._callbacks || {};
                var args = [].slice.call(arguments, 1), callbacks = this._callbacks[event];
                if (callbacks) {
                    callbacks = callbacks.slice(0);
                    for (var i = 0, len = callbacks.length; i < len; ++i) {
                        callbacks[i].apply(this, args)
                    }
                }
                return this
            };
            Emitter.prototype.listeners = function (event) {
                this._callbacks = this._callbacks || {};
                return this._callbacks[event] || []
            };
            Emitter.prototype.hasListeners = function (event) {
                return !!this.listeners(event).length
            }
        }, {}],
        9: [function (_dereq_, module, exports) {
            module.exports = debug;

            function debug(name) {
                if (!debug.enabled(name)) return function () {
                };
                return function (fmt) {
                    fmt = coerce(fmt);
                    var curr = new Date;
                    var ms = curr - (debug[name] || curr);
                    debug[name] = curr;
                    fmt = name + " " + fmt + " +" + debug.humanize(ms);
                    window.console && console.log && Function.prototype.apply.call(console.log, console, arguments)
                }
            }

            debug.names = [];
            debug.skips = [];
            debug.enable = function (name) {
                try {
                    localStorage.debug = name
                } catch (e) {
                }
                var split = (name || "").split(/[\s,]+/), len = split.length;
                for (var i = 0; i < len; i++) {
                    name = split[i].replace("*", ".*?");
                    if (name[0] === "-") {
                        debug.skips.push(new RegExp("^" + name.substr(1) + "$"))
                    } else {
                        debug.names.push(new RegExp("^" + name + "$"))
                    }
                }
            };
            debug.disable = function () {
                debug.enable("")
            };
            debug.humanize = function (ms) {
                var sec = 1e3, min = 60 * 1e3, hour = 60 * min;
                if (ms >= hour) return (ms / hour).toFixed(1) + "h";
                if (ms >= min) return (ms / min).toFixed(1) + "m";
                if (ms >= sec) return (ms / sec | 0) + "s";
                return ms + "ms"
            };
            debug.enabled = function (name) {
                for (var i = 0, len = debug.skips.length; i < len; i++) {
                    if (debug.skips[i].test(name)) {
                        return false
                    }
                }
                for (var i = 0, len = debug.names.length; i < len; i++) {
                    if (debug.names[i].test(name)) {
                        return true
                    }
                }
                return false
            };

            function coerce(val) {
                if (val instanceof Error) return val.stack || val.message;
                return val
            }

            try {
                if (window.localStorage) debug.enable(localStorage.debug)
            } catch (e) {
            }
        }, {}],
        10: [function (_dereq_, module, exports) {
            module.exports = _dereq_("./lib/")
        }, {"./lib/": 11}],
        11: [function (_dereq_, module, exports) {
            module.exports = _dereq_("./socket");
            module.exports.parser = _dereq_("engine.io-parser")
        }, {"./socket": 12, "engine.io-parser": 21}],
        12: [function (_dereq_, module, exports) {
            (function (global) {
                var transports = _dereq_("./transports");
                var Emitter = _dereq_("component-emitter");
                var debug = _dereq_("debug")("engine.io-client:socket");
                var index = _dereq_("indexof");
                var parser = _dereq_("engine.io-parser");
                var parseuri = _dereq_("parseuri");
                var parsejson = _dereq_("parsejson");
                var parseqs = _dereq_("parseqs");
                module.exports = Socket;

                function noop() {
                }

                function Socket(uri, opts) {
                    if (!(this instanceof Socket)) return new Socket(uri, opts);
                    opts = opts || {};
                    if (uri && "object" == typeof uri) {
                        opts = uri;
                        uri = null
                    }
                    if (uri) {
                        uri = parseuri(uri);
                        opts.host = uri.host;
                        opts.secure = uri.protocol == "https" || uri.protocol == "wss";
                        opts.port = uri.port;
                        if (uri.query) opts.query = uri.query
                    }
                    this.secure = null != opts.secure ? opts.secure : global.location && "https:" == location.protocol;
                    if (opts.host) {
                        var pieces = opts.host.split(":");
                        opts.hostname = pieces.shift();
                        if (pieces.length) opts.port = pieces.pop()
                    }
                    this.agent = opts.agent || false;
                    this.hostname = opts.hostname || (global.location ? location.hostname : "localhost");
                    this.port = opts.port || (global.location && location.port ? location.port : this.secure ? 443 : 80);
                    this.query = opts.query || {};
                    if ("string" == typeof this.query) this.query = parseqs.decode(this.query);
                    this.upgrade = false !== opts.upgrade;
                    this.path = (opts.path || "/engine.io").replace(/\/$/, "") + "/";
                    this.forceJSONP = !!opts.forceJSONP;
                    this.jsonp = false !== opts.jsonp;
                    this.forceBase64 = !!opts.forceBase64;
                    this.enablesXDR = !!opts.enablesXDR;
                    this.timestampParam = opts.timestampParam || "t";
                    this.timestampRequests = opts.timestampRequests;
                    this.transports = opts.transports || ["polling", "websocket"];
                    this.readyState = "";
                    this.writeBuffer = [];
                    this.callbackBuffer = [];
                    this.policyPort = opts.policyPort || 843;
                    this.rememberUpgrade = opts.rememberUpgrade || false;
                    this.open();
                    this.binaryType = null;
                    this.onlyBinaryUpgrades = opts.onlyBinaryUpgrades
                }

                Socket.priorWebsocketSuccess = false;
                Emitter(Socket.prototype);
                Socket.protocol = parser.protocol;
                Socket.Socket = Socket;
                Socket.Transport = _dereq_("./transport");
                Socket.transports = _dereq_("./transports");
                Socket.parser = _dereq_("engine.io-parser");
                Socket.prototype.createTransport = function (name) {
                    debug('creating transport "%s"', name);
                    var query = clone(this.query);
                    query.EIO = parser.protocol;
                    query.transport = name;
                    if (this.id) query.sid = this.id;
                    var transport = new transports[name]({
                        agent: this.agent,
                        hostname: this.hostname,
                        port: this.port,
                        secure: this.secure,
                        path: this.path,
                        query: query,
                        forceJSONP: this.forceJSONP,
                        jsonp: this.jsonp,
                        forceBase64: this.forceBase64,
                        enablesXDR: this.enablesXDR,
                        timestampRequests: this.timestampRequests,
                        timestampParam: this.timestampParam,
                        policyPort: this.policyPort,
                        socket: this
                    });
                    return transport
                };

                function clone(obj) {
                    var o = {};
                    for (var i in obj) {
                        if (obj.hasOwnProperty(i)) {
                            o[i] = obj[i]
                        }
                    }
                    return o
                }

                Socket.prototype.open = function () {
                    var transport;
                    if (this.rememberUpgrade && Socket.priorWebsocketSuccess && this.transports.indexOf("websocket") != -1) {
                        transport = "websocket"
                    } else if (0 == this.transports.length) {
                        var self = this;
                        setTimeout(function () {
                            self.emit("error", "No transports available")
                        }, 0);
                        return
                    } else {
                        transport = this.transports[0]
                    }
                    this.readyState = "opening";
                    var transport;
                    try {
                        transport = this.createTransport(transport)
                    } catch (e) {
                        this.transports.shift();
                        this.open();
                        return
                    }
                    transport.open();
                    this.setTransport(transport)
                };
                Socket.prototype.setTransport = function (transport) {
                    debug("setting transport %s", transport.name);
                    var self = this;
                    if (this.transport) {
                        debug("clearing existing transport %s", this.transport.name);
                        this.transport.removeAllListeners()
                    }
                    this.transport = transport;
                    transport.on("drain", function () {
                        self.onDrain()
                    }).on("packet", function (packet) {
                        self.onPacket(packet)
                    }).on("error", function (e) {
                        self.onError(e)
                    }).on("close", function () {
                        self.onClose("transport close")
                    })
                };
                Socket.prototype.probe = function (name) {
                    debug('probing transport "%s"', name);
                    var transport = this.createTransport(name, {probe: 1}), failed = false, self = this;
                    Socket.priorWebsocketSuccess = false;

                    function onTransportOpen() {
                        if (self.onlyBinaryUpgrades) {
                            var upgradeLosesBinary = !this.supportsBinary && self.transport.supportsBinary;
                            failed = failed || upgradeLosesBinary
                        }
                        if (failed) return;
                        debug('probe transport "%s" opened', name);
                        transport.send([{type: "ping", data: "probe"}]);
                        transport.once("packet", function (msg) {
                            if (failed) return;
                            if ("pong" == msg.type && "probe" == msg.data) {
                                debug('probe transport "%s" pong', name);
                                self.upgrading = true;
                                self.emit("upgrading", transport);
                                Socket.priorWebsocketSuccess = "websocket" == transport.name;
                                debug('pausing current transport "%s"', self.transport.name);
                                self.transport.pause(function () {
                                    if (failed) return;
                                    if ("closed" == self.readyState || "closing" == self.readyState) {
                                        return
                                    }
                                    debug("changing transport and sending upgrade packet");
                                    cleanup();
                                    self.setTransport(transport);
                                    transport.send([{type: "upgrade"}]);
                                    self.emit("upgrade", transport);
                                    transport = null;
                                    self.upgrading = false;
                                    self.flush()
                                })
                            } else {
                                debug('probe transport "%s" failed', name);
                                var err = new Error("probe error");
                                err.transport = transport.name;
                                self.emit("upgradeError", err)
                            }
                        })
                    }

                    function freezeTransport() {
                        if (failed) return;
                        failed = true;
                        cleanup();
                        transport.close();
                        transport = null
                    }

                    function onerror(err) {
                        var error = new Error("probe error: " + err);
                        error.transport = transport.name;
                        freezeTransport();
                        debug('probe transport "%s" failed because of error: %s', name, err);
                        self.emit("upgradeError", error)
                    }

                    function onTransportClose() {
                        onerror("transport closed")
                    }

                    function onclose() {
                        onerror("socket closed")
                    }

                    function onupgrade(to) {
                        if (transport && to.name != transport.name) {
                            debug('"%s" works - aborting "%s"', to.name, transport.name);
                            freezeTransport()
                        }
                    }

                    function cleanup() {
                        transport.removeListener("open", onTransportOpen);
                        transport.removeListener("error", onerror);
                        transport.removeListener("close", onTransportClose);
                        self.removeListener("close", onclose);
                        self.removeListener("upgrading", onupgrade)
                    }

                    transport.once("open", onTransportOpen);
                    transport.once("error", onerror);
                    transport.once("close", onTransportClose);
                    this.once("close", onclose);
                    this.once("upgrading", onupgrade);
                    transport.open()
                };
                Socket.prototype.onOpen = function () {
                    debug("socket open");
                    this.readyState = "open";
                    Socket.priorWebsocketSuccess = "websocket" == this.transport.name;
                    this.emit("open");
                    this.flush();
                    if ("open" == this.readyState && this.upgrade && this.transport.pause) {
                        debug("starting upgrade probes");
                        for (var i = 0, l = this.upgrades.length; i < l; i++) {
                            this.probe(this.upgrades[i])
                        }
                    }
                };
                Socket.prototype.onPacket = function (packet) {
                    if ("opening" == this.readyState || "open" == this.readyState) {
                        debug('socket receive: type "%s", data "%s"', packet.type, packet.data);
                        this.emit("packet", packet);
                        this.emit("heartbeat");
                        switch (packet.type) {
                            case"open":
                                this.onHandshake(parsejson(packet.data));
                                break;
                            case"pong":
                                this.setPing();
                                break;
                            case"error":
                                var err = new Error("server error");
                                err.code = packet.data;
                                this.emit("error", err);
                                break;
                            case"message":
                                this.emit("data", packet.data);
                                this.emit("message", packet.data);
                                break
                        }
                    } else {
                        debug('packet received with socket readyState "%s"', this.readyState)
                    }
                };
                Socket.prototype.onHandshake = function (data) {
                    this.emit("handshake", data);
                    this.id = data.sid;
                    this.transport.query.sid = data.sid;
                    this.upgrades = this.filterUpgrades(data.upgrades);
                    this.pingInterval = data.pingInterval;
                    this.pingTimeout = data.pingTimeout;
                    this.onOpen();
                    if ("closed" == this.readyState) return;
                    this.setPing();
                    this.removeListener("heartbeat", this.onHeartbeat);
                    this.on("heartbeat", this.onHeartbeat)
                };
                Socket.prototype.onHeartbeat = function (timeout) {
                    clearTimeout(this.pingTimeoutTimer);
                    var self = this;
                    self.pingTimeoutTimer = setTimeout(function () {
                        if ("closed" == self.readyState) return;
                        self.onClose("ping timeout")
                    }, timeout || self.pingInterval + self.pingTimeout)
                };
                Socket.prototype.setPing = function () {
                    var self = this;
                    clearTimeout(self.pingIntervalTimer);
                    self.pingIntervalTimer = setTimeout(function () {
                        debug("writing ping packet - expecting pong within %sms", self.pingTimeout);
                        self.ping();
                        self.onHeartbeat(self.pingTimeout)
                    }, self.pingInterval)
                };
                Socket.prototype.ping = function () {
                    this.sendPacket("ping")
                };
                Socket.prototype.onDrain = function () {
                    for (var i = 0; i < this.prevBufferLen; i++) {
                        if (this.callbackBuffer[i]) {
                            this.callbackBuffer[i]()
                        }
                    }
                    this.writeBuffer.splice(0, this.prevBufferLen);
                    this.callbackBuffer.splice(0, this.prevBufferLen);
                    this.prevBufferLen = 0;
                    if (this.writeBuffer.length == 0) {
                        this.emit("drain")
                    } else {
                        this.flush()
                    }
                };
                Socket.prototype.flush = function () {
                    if ("closed" != this.readyState && this.transport.writable && !this.upgrading && this.writeBuffer.length) {
                        debug("flushing %d packets in socket", this.writeBuffer.length);
                        this.transport.send(this.writeBuffer);
                        this.prevBufferLen = this.writeBuffer.length;
                        this.emit("flush")
                    }
                };
                Socket.prototype.write = Socket.prototype.send = function (msg, fn) {
                    this.sendPacket("message", msg, fn);
                    return this
                };
                Socket.prototype.sendPacket = function (type, data, fn) {
                    var packet = {type: type, data: data};
                    this.emit("packetCreate", packet);
                    this.writeBuffer.push(packet);
                    this.callbackBuffer.push(fn);
                    this.flush()
                };
                Socket.prototype.close = function () {
                    if ("opening" == this.readyState || "open" == this.readyState) {
                        this.onClose("forced close");
                        debug("socket closing - telling transport to close");
                        this.transport.close()
                    }
                    return this
                };
                Socket.prototype.onError = function (err) {
                    debug("socket error %j", err);
                    Socket.priorWebsocketSuccess = false;
                    this.emit("error", err);
                    this.onClose("transport error", err)
                };
                Socket.prototype.onClose = function (reason, desc) {
                    if ("opening" == this.readyState || "open" == this.readyState) {
                        debug('socket close with reason: "%s"', reason);
                        var self = this;
                        clearTimeout(this.pingIntervalTimer);
                        clearTimeout(this.pingTimeoutTimer);
                        setTimeout(function () {
                            self.writeBuffer = [];
                            self.callbackBuffer = [];
                            self.prevBufferLen = 0
                        }, 0);
                        this.transport.removeAllListeners("close");
                        this.transport.close();
                        this.transport.removeAllListeners();
                        this.readyState = "closed";
                        this.id = null;
                        this.emit("close", reason, desc)
                    }
                };
                Socket.prototype.filterUpgrades = function (upgrades) {
                    var filteredUpgrades = [];
                    for (var i = 0, j = upgrades.length; i < j; i++) {
                        if (~index(this.transports, upgrades[i])) filteredUpgrades.push(upgrades[i])
                    }
                    return filteredUpgrades
                }
            }).call(this, typeof self !== "undefined" ? self : typeof window !== "undefined" ? window : {})
        }, {
            "./transport": 13,
            "./transports": 14,
            "component-emitter": 8,
            debug: 9,
            "engine.io-parser": 21,
            indexof: 36,
            parsejson: 28,
            parseqs: 29,
            parseuri: 30
        }],
        13: [function (_dereq_, module, exports) {
            var parser = _dereq_("engine.io-parser");
            var Emitter = _dereq_("component-emitter");
            module.exports = Transport;

            function Transport(opts) {
                this.path = opts.path;
                this.hostname = opts.hostname;
                this.port = opts.port;
                this.secure = opts.secure;
                this.query = opts.query;
                this.timestampParam = opts.timestampParam;
                this.timestampRequests = opts.timestampRequests;
                this.readyState = "";
                this.agent = opts.agent || false;
                this.socket = opts.socket;
                this.enablesXDR = opts.enablesXDR
            }

            Emitter(Transport.prototype);
            Transport.timestamps = 0;
            Transport.prototype.onError = function (msg, desc) {
                var err = new Error(msg);
                err.type = "TransportError";
                err.description = desc;
                this.emit("error", err);
                return this
            };
            Transport.prototype.open = function () {
                if ("closed" == this.readyState || "" == this.readyState) {
                    this.readyState = "opening";
                    this.doOpen()
                }
                return this
            };
            Transport.prototype.close = function () {
                if ("opening" == this.readyState || "open" == this.readyState) {
                    this.doClose();
                    this.onClose()
                }
                return this
            };
            Transport.prototype.send = function (packets) {
                if ("open" == this.readyState) {
                    this.write(packets)
                } else {
                    throw new Error("Transport not open")
                }
            };
            Transport.prototype.onOpen = function () {
                this.readyState = "open";
                this.writable = true;
                this.emit("open")
            };
            Transport.prototype.onData = function (data) {
                var packet = parser.decodePacket(data, this.socket.binaryType);
                this.onPacket(packet)
            };
            Transport.prototype.onPacket = function (packet) {
                this.emit("packet", packet)
            };
            Transport.prototype.onClose = function () {
                this.readyState = "closed";
                this.emit("close")
            }
        }, {"component-emitter": 8, "engine.io-parser": 21}],
        14: [function (_dereq_, module, exports) {
            (function (global) {
                var XMLHttpRequest = _dereq_("xmlhttprequest");
                var XHR = _dereq_("./polling-xhr");
                var JSONP = _dereq_("./polling-jsonp");
                var websocket = _dereq_("./websocket");
                exports.polling = polling;
                exports.websocket = websocket;

                function polling(opts) {
                    var xhr;
                    var xd = false;
                    var xs = false;
                    var jsonp = false !== opts.jsonp;
                    if (global.location) {
                        var isSSL = "https:" == location.protocol;
                        var port = location.port;
                        if (!port) {
                            port = isSSL ? 443 : 80
                        }
                        xd = opts.hostname != location.hostname || port != opts.port;
                        xs = opts.secure != isSSL
                    }
                    opts.xdomain = xd;
                    opts.xscheme = xs;
                    xhr = new XMLHttpRequest(opts);
                    if ("open" in xhr && !opts.forceJSONP) {
                        return new XHR(opts)
                    } else {
                        if (!jsonp) throw new Error("JSONP disabled");
                        return new JSONP(opts)
                    }
                }
            }).call(this, typeof self !== "undefined" ? self : typeof window !== "undefined" ? window : {})
        }, {"./polling-jsonp": 15, "./polling-xhr": 16, "./websocket": 18, xmlhttprequest: 19}],
        15: [function (_dereq_, module, exports) {
            (function (global) {
                var Polling = _dereq_("./polling");
                var inherit = _dereq_("component-inherit");
                module.exports = JSONPPolling;
                var rNewline = /\n/g;
                var rEscapedNewline = /\\n/g;
                var callbacks;
                var index = 0;

                function empty() {
                }

                function JSONPPolling(opts) {
                    Polling.call(this, opts);
                    this.query = this.query || {};
                    if (!callbacks) {
                        if (!global.___eio) global.___eio = [];
                        callbacks = global.___eio
                    }
                    this.index = callbacks.length;
                    var self = this;
                    callbacks.push(function (msg) {
                        self.onData(msg)
                    });
                    this.query.j = this.index;
                    if (global.document && global.addEventListener) {
                        global.addEventListener("beforeunload", function () {
                            if (self.script) self.script.onerror = empty
                        })
                    }
                }

                inherit(JSONPPolling, Polling);
                JSONPPolling.prototype.supportsBinary = false;
                JSONPPolling.prototype.doClose = function () {
                    if (this.script) {
                        this.script.parentNode.removeChild(this.script);
                        this.script = null
                    }
                    if (this.form) {
                        this.form.parentNode.removeChild(this.form);
                        this.form = null
                    }
                    Polling.prototype.doClose.call(this)
                };
                JSONPPolling.prototype.doPoll = function () {
                    var self = this;
                    var script = document.createElement("script");
                    if (this.script) {
                        this.script.parentNode.removeChild(this.script);
                        this.script = null
                    }
                    script.async = true;
                    script.src = this.uri();
                    script.onerror = function (e) {
                        self.onError("jsonp poll error", e)
                    };
                    var insertAt = document.getElementsByTagName("script")[0];
                    insertAt.parentNode.insertBefore(script, insertAt);
                    this.script = script;
                    var isUAgecko = "undefined" != typeof navigator && /gecko/i.test(navigator.userAgent);
                    if (isUAgecko) {
                        setTimeout(function () {
                            var iframe = document.createElement("iframe");
                            document.body.appendChild(iframe);
                            document.body.removeChild(iframe)
                        }, 100)
                    }
                };
                JSONPPolling.prototype.doWrite = function (data, fn) {
                    var self = this;
                    if (!this.form) {
                        var form = document.createElement("form");
                        var area = document.createElement("textarea");
                        var id = this.iframeId = "eio_iframe_" + this.index;
                        var iframe;
                        form.className = "socketio";
                        form.style.position = "absolute";
                        form.style.top = "-1000px";
                        form.style.left = "-1000px";
                        form.target = id;
                        form.method = "POST";
                        form.setAttribute("accept-charset", "utf-8");
                        area.name = "d";
                        form.appendChild(area);
                        document.body.appendChild(form);
                        this.form = form;
                        this.area = area
                    }
                    this.form.action = this.uri();

                    function complete() {
                        initIframe();
                        fn()
                    }

                    function initIframe() {
                        if (self.iframe) {
                            try {
                                self.form.removeChild(self.iframe)
                            } catch (e) {
                                self.onError("jsonp polling iframe removal error", e)
                            }
                        }
                        try {
                            var html = '<iframe src="javascript:0" name="' + self.iframeId + '">';
                            iframe = document.createElement(html)
                        } catch (e) {
                            iframe = document.createElement("iframe");
                            iframe.name = self.iframeId;
                            iframe.src = "javascript:0"
                        }
                        iframe.id = self.iframeId;
                        self.form.appendChild(iframe);
                        self.iframe = iframe
                    }

                    initIframe();
                    data = data.replace(rEscapedNewline, "\\\n");
                    this.area.value = data.replace(rNewline, "\\n");
                    try {
                        this.form.submit()
                    } catch (e) {
                    }
                    if (this.iframe.attachEvent) {
                        this.iframe.onreadystatechange = function () {
                            if (self.iframe.readyState == "complete") {
                                complete()
                            }
                        }
                    } else {
                        this.iframe.onload = complete
                    }
                }
            }).call(this, typeof self !== "undefined" ? self : typeof window !== "undefined" ? window : {})
        }, {"./polling": 17, "component-inherit": 20}],
        16: [function (_dereq_, module, exports) {
            (function (global) {
                var XMLHttpRequest = _dereq_("xmlhttprequest");
                var Polling = _dereq_("./polling");
                var Emitter = _dereq_("component-emitter");
                var inherit = _dereq_("component-inherit");
                var debug = _dereq_("debug")("engine.io-client:polling-xhr");
                module.exports = XHR;
                module.exports.Request = Request;

                function empty() {
                }

                function XHR(opts) {
                    Polling.call(this, opts);
                    if (global.location) {
                        var isSSL = "https:" == location.protocol;
                        var port = location.port;
                        if (!port) {
                            port = isSSL ? 443 : 80
                        }
                        this.xd = opts.hostname != global.location.hostname || port != opts.port;
                        this.xs = opts.secure != isSSL
                    }
                }

                inherit(XHR, Polling);
                XHR.prototype.supportsBinary = true;
                XHR.prototype.request = function (opts) {
                    opts = opts || {};
                    opts.uri = this.uri();
                    opts.xd = this.xd;
                    opts.xs = this.xs;
                    opts.agent = this.agent || false;
                    opts.supportsBinary = this.supportsBinary;
                    opts.enablesXDR = this.enablesXDR;
                    return new Request(opts)
                };
                XHR.prototype.doWrite = function (data, fn) {
                    var isBinary = typeof data !== "string" && data !== undefined;
                    var req = this.request({method: "POST", data: data, isBinary: isBinary});
                    var self = this;
                    req.on("success", fn);
                    req.on("error", function (err) {
                        self.onError("xhr post error", err)
                    });
                    this.sendXhr = req
                };
                XHR.prototype.doPoll = function () {
                    debug("xhr poll");
                    var req = this.request();
                    var self = this;
                    req.on("data", function (data) {
                        self.onData(data)
                    });
                    req.on("error", function (err) {
                        self.onError("xhr poll error", err)
                    });
                    this.pollXhr = req
                };

                function Request(opts) {
                    this.method = opts.method || "GET";
                    this.uri = opts.uri;
                    this.xd = !!opts.xd;
                    this.xs = !!opts.xs;
                    this.async = false !== opts.async;
                    this.data = undefined != opts.data ? opts.data : null;
                    this.agent = opts.agent;
                    this.isBinary = opts.isBinary;
                    this.supportsBinary = opts.supportsBinary;
                    this.enablesXDR = opts.enablesXDR;
                    this.create()
                }

                Emitter(Request.prototype);
                Request.prototype.create = function () {
                    var xhr = this.xhr = new XMLHttpRequest({
                        agent: this.agent,
                        xdomain: this.xd,
                        xscheme: this.xs,
                        enablesXDR: this.enablesXDR
                    });
                    var self = this;
                    try {
                        debug("xhr open %s: %s", this.method, this.uri);
                        xhr.open(this.method, this.uri, this.async);
                        if (this.supportsBinary) {
                            xhr.responseType = "arraybuffer"
                        }
                        if ("POST" == this.method) {
                            try {
                                if (this.isBinary) {
                                    xhr.setRequestHeader("Content-type", "application/octet-stream")
                                } else {
                                    xhr.setRequestHeader("Content-type", "text/plain;charset=UTF-8")
                                }
                            } catch (e) {
                            }
                        }
                        if ("withCredentials" in xhr) {
                            xhr.withCredentials = true
                        }
                        if (this.hasXDR()) {
                            xhr.onload = function () {
                                self.onLoad()
                            };
                            xhr.onerror = function () {
                                self.onError(xhr.responseText)
                            }
                        } else {
                            xhr.onreadystatechange = function () {
                                if (4 != xhr.readyState) return;
                                if (200 == xhr.status || 1223 == xhr.status) {
                                    self.onLoad()
                                } else {
                                    setTimeout(function () {
                                        self.onError(xhr.status)
                                    }, 0)
                                }
                            }
                        }
                        debug("xhr data %s", this.data);
                        xhr.send(this.data)
                    } catch (e) {
                        setTimeout(function () {
                            self.onError(e)
                        }, 0);
                        return
                    }
                    if (global.document) {
                        this.index = Request.requestsCount++;
                        Request.requests[this.index] = this
                    }
                };
                Request.prototype.onSuccess = function () {
                    this.emit("success");
                    this.cleanup()
                };
                Request.prototype.onData = function (data) {
                    this.emit("data", data);
                    this.onSuccess()
                };
                Request.prototype.onError = function (err) {
                    this.emit("error", err);
                    this.cleanup()
                };
                Request.prototype.cleanup = function () {
                    if ("undefined" == typeof this.xhr || null === this.xhr) {
                        return
                    }
                    if (this.hasXDR()) {
                        this.xhr.onload = this.xhr.onerror = empty
                    } else {
                        this.xhr.onreadystatechange = empty
                    }
                    try {
                        this.xhr.abort()
                    } catch (e) {
                    }
                    if (global.document) {
                        delete Request.requests[this.index]
                    }
                    this.xhr = null
                };
                Request.prototype.onLoad = function () {
                    var data;
                    try {
                        var contentType;
                        try {
                            contentType = this.xhr.getResponseHeader("Content-Type")
                        } catch (e) {
                        }
                        if (contentType === "application/octet-stream") {
                            data = this.xhr.response
                        } else {
                            if (!this.supportsBinary) {
                                data = this.xhr.responseText
                            } else {
                                data = "ok"
                            }
                        }
                    } catch (e) {
                        this.onError(e)
                    }
                    if (null != data) {
                        this.onData(data)
                    }
                };
                Request.prototype.hasXDR = function () {
                    return "undefined" !== typeof global.XDomainRequest && !this.xs && this.enablesXDR
                };
                Request.prototype.abort = function () {
                    this.cleanup()
                };
                if (global.document) {
                    Request.requestsCount = 0;
                    Request.requests = {};
                    if (global.attachEvent) {
                        global.attachEvent("onunload", unloadHandler)
                    } else if (global.addEventListener) {
                        global.addEventListener("beforeunload", unloadHandler)
                    }
                }

                function unloadHandler() {
                    for (var i in Request.requests) {
                        if (Request.requests.hasOwnProperty(i)) {
                            Request.requests[i].abort()
                        }
                    }
                }
            }).call(this, typeof self !== "undefined" ? self : typeof window !== "undefined" ? window : {})
        }, {"./polling": 17, "component-emitter": 8, "component-inherit": 20, debug: 9, xmlhttprequest: 19}],
        17: [function (_dereq_, module, exports) {
            var Transport = _dereq_("../transport");
            var parseqs = _dereq_("parseqs");
            var parser = _dereq_("engine.io-parser");
            var inherit = _dereq_("component-inherit");
            var debug = _dereq_("debug")("engine.io-client:polling");
            module.exports = Polling;
            var hasXHR2 = function () {
                var XMLHttpRequest = _dereq_("xmlhttprequest");
                var xhr = new XMLHttpRequest({agent: this.agent, xdomain: false});
                return null != xhr.responseType
            }();

            function Polling(opts) {
                var forceBase64 = opts && opts.forceBase64;
                if (!hasXHR2 || forceBase64) {
                    this.supportsBinary = false
                }
                Transport.call(this, opts)
            }

            inherit(Polling, Transport);
            Polling.prototype.name = "polling";
            Polling.prototype.doOpen = function () {
                this.poll()
            };
            Polling.prototype.pause = function (onPause) {
                var pending = 0;
                var self = this;
                this.readyState = "pausing";

                function pause() {
                    debug("paused");
                    self.readyState = "paused";
                    onPause()
                }

                if (this.polling || !this.writable) {
                    var total = 0;
                    if (this.polling) {
                        debug("we are currently polling - waiting to pause");
                        total++;
                        this.once("pollComplete", function () {
                            debug("pre-pause polling complete");
                            --total || pause()
                        })
                    }
                    if (!this.writable) {
                        debug("we are currently writing - waiting to pause");
                        total++;
                        this.once("drain", function () {
                            debug("pre-pause writing complete");
                            --total || pause()
                        })
                    }
                } else {
                    pause()
                }
            };
            Polling.prototype.poll = function () {
                debug("polling");
                this.polling = true;
                this.doPoll();
                this.emit("poll")
            };
            Polling.prototype.onData = function (data) {
                var self = this;
                debug("polling got data %s", data);
                var callback = function (packet, index, total) {
                    if ("opening" == self.readyState) {
                        self.onOpen()
                    }
                    if ("close" == packet.type) {
                        self.onClose();
                        return false
                    }
                    self.onPacket(packet)
                };
                parser.decodePayload(data, this.socket.binaryType, callback);
                if ("closed" != this.readyState) {
                    this.polling = false;
                    this.emit("pollComplete");
                    if ("open" == this.readyState) {
                        this.poll()
                    } else {
                        debug('ignoring poll - transport state "%s"', this.readyState)
                    }
                }
            };
            Polling.prototype.doClose = function () {
                var self = this;

                function close() {
                    debug("writing close packet");
                    self.write([{type: "close"}])
                }

                if ("open" == this.readyState) {
                    debug("transport open - closing");
                    close()
                } else {
                    debug("transport not open - deferring close");
                    this.once("open", close)
                }
            };
            Polling.prototype.write = function (packets) {
                var self = this;
                this.writable = false;
                var callbackfn = function () {
                    self.writable = true;
                    self.emit("drain")
                };
                var self = this;
                parser.encodePayload(packets, this.supportsBinary, function (data) {
                    self.doWrite(data, callbackfn)
                })
            };
            Polling.prototype.uri = function () {
                var query = this.query || {};
                var schema = this.secure ? "https" : "http";
                var port = "";
                if (false !== this.timestampRequests) {
                    query[this.timestampParam] = +new Date + "-" + Transport.timestamps++
                }
                if (!this.supportsBinary && !query.sid) {
                    query.b64 = 1
                }
                query = parseqs.encode(query);
                if (this.port && ("https" == schema && this.port != 443 || "http" == schema && this.port != 80)) {
                    port = ":" + this.port
                }
                if (query.length) {
                    query = "?" + query
                }
                return schema + "://" + this.hostname + port + this.path + query
            }
        }, {
            "../transport": 13,
            "component-inherit": 20,
            debug: 9,
            "engine.io-parser": 21,
            parseqs: 29,
            xmlhttprequest: 19
        }],
        18: [function (_dereq_, module, exports) {
            var Transport = _dereq_("../transport");
            var parser = _dereq_("engine.io-parser");
            var parseqs = _dereq_("parseqs");
            var inherit = _dereq_("component-inherit");
            var debug = _dereq_("debug")("engine.io-client:websocket");
            var WebSocket = _dereq_("ws");
            module.exports = WS;

            function WS(opts) {
                var forceBase64 = opts && opts.forceBase64;
                if (forceBase64) {
                    this.supportsBinary = false
                }
                Transport.call(this, opts)
            }

            inherit(WS, Transport);
            WS.prototype.name = "websocket";
            WS.prototype.supportsBinary = true;
            WS.prototype.doOpen = function () {
                if (!this.check()) {
                    return
                }
                var self = this;
                var uri = this.uri();
                var protocols = void 0;
                var opts = {agent: this.agent};
                this.ws = new WebSocket(uri, protocols, opts);
                if (this.ws.binaryType === undefined) {
                    this.supportsBinary = false
                }
                this.ws.binaryType = "arraybuffer";
                this.addEventListeners()
            };
            WS.prototype.addEventListeners = function () {
                var self = this;
                this.ws.onopen = function () {
                    self.onOpen()
                };
                this.ws.onclose = function () {
                    self.onClose()
                };
                this.ws.onmessage = function (ev) {
                    self.onData(ev.data)
                };
                this.ws.onerror = function (e) {
                    self.onError("websocket error", e)
                }
            };
            if ("undefined" != typeof navigator && /iPad|iPhone|iPod/i.test(navigator.userAgent)) {
                WS.prototype.onData = function (data) {
                    var self = this;
                    setTimeout(function () {
                        Transport.prototype.onData.call(self, data)
                    }, 0)
                }
            }
            WS.prototype.write = function (packets) {
                var self = this;
                this.writable = false;
                for (var i = 0, l = packets.length; i < l; i++) {
                    parser.encodePacket(packets[i], this.supportsBinary, function (data) {
                        try {
                            self.ws.send(data)
                        } catch (e) {
                            debug("websocket closed before onclose event")
                        }
                    })
                }

                function ondrain() {
                    self.writable = true;
                    self.emit("drain")
                }

                setTimeout(ondrain, 0)
            };
            WS.prototype.onClose = function () {
                Transport.prototype.onClose.call(this)
            };
            WS.prototype.doClose = function () {
                if (typeof this.ws !== "undefined") {
                    this.ws.close()
                }
            };
            WS.prototype.uri = function () {
                var query = this.query || {};
                var schema = this.secure ? "wss" : "ws";
                var port = "";
                if (this.port && ("wss" == schema && this.port != 443 || "ws" == schema && this.port != 80)) {
                    port = ":" + this.port
                }
                if (this.timestampRequests) {
                    query[this.timestampParam] = +new Date
                }
                if (!this.supportsBinary) {
                    query.b64 = 1
                }
                query = parseqs.encode(query);
                if (query.length) {
                    query = "?" + query
                }
                return schema + "://" + this.hostname + port + this.path + query
            };
            WS.prototype.check = function () {
                return !!WebSocket && !("__initialize" in WebSocket && this.name === WS.prototype.name)
            }
        }, {"../transport": 13, "component-inherit": 20, debug: 9, "engine.io-parser": 21, parseqs: 29, ws: 31}],
        19: [function (_dereq_, module, exports) {
            var hasCORS = _dereq_("has-cors");
            module.exports = function (opts) {
                var xdomain = opts.xdomain;
                var xscheme = opts.xscheme;
                var enablesXDR = opts.enablesXDR;
                try {
                    if ("undefined" != typeof XDomainRequest && !xscheme && enablesXDR) {
                        return new XDomainRequest
                    }
                } catch (e) {
                }
                try {
                    if ("undefined" != typeof XMLHttpRequest && (!xdomain || hasCORS)) {
                        return new XMLHttpRequest
                    }
                } catch (e) {
                }
                if (!xdomain) {
                    try {
                        return new ActiveXObject("Microsoft.XMLHTTP")
                    } catch (e) {
                    }
                }
            }
        }, {"has-cors": 34}],
        20: [function (_dereq_, module, exports) {
            module.exports = function (a, b) {
                var fn = function () {
                };
                fn.prototype = b.prototype;
                a.prototype = new fn;
                a.prototype.constructor = a
            }
        }, {}],
        21: [function (_dereq_, module, exports) {
            (function (global) {
                var keys = _dereq_("./keys");
                var sliceBuffer = _dereq_("arraybuffer.slice");
                var base64encoder = _dereq_("base64-arraybuffer");
                var after = _dereq_("after");
                var utf8 = _dereq_("utf8");
                var isAndroid = navigator.userAgent.match(/Android/i);
                exports.protocol = 3;
                var packets = exports.packets = {open: 0, close: 1, ping: 2, pong: 3, message: 4, upgrade: 5, noop: 6};
                var packetslist = keys(packets);
                var err = {type: "error", data: "parser error"};
                var Blob = _dereq_("blob");
                exports.encodePacket = function (packet, supportsBinary, utf8encode, callback) {
                    if ("function" == typeof supportsBinary) {
                        callback = supportsBinary;
                        supportsBinary = false
                    }
                    if ("function" == typeof utf8encode) {
                        callback = utf8encode;
                        utf8encode = null
                    }
                    var data = packet.data === undefined ? undefined : packet.data.buffer || packet.data;
                    if (global.ArrayBuffer && data instanceof ArrayBuffer) {
                        return encodeArrayBuffer(packet, supportsBinary, callback)
                    } else if (Blob && data instanceof global.Blob) {
                        return encodeBlob(packet, supportsBinary, callback)
                    }
                    var encoded = packets[packet.type];
                    if (undefined !== packet.data) {
                        encoded += utf8encode ? utf8.encode(String(packet.data)) : String(packet.data)
                    }
                    return callback("" + encoded)
                };

                function encodeArrayBuffer(packet, supportsBinary, callback) {
                    if (!supportsBinary) {
                        return exports.encodeBase64Packet(packet, callback)
                    }
                    var data = packet.data;
                    var contentArray = new Uint8Array(data);
                    var resultBuffer = new Uint8Array(1 + data.byteLength);
                    resultBuffer[0] = packets[packet.type];
                    for (var i = 0; i < contentArray.length; i++) {
                        resultBuffer[i + 1] = contentArray[i]
                    }
                    return callback(resultBuffer.buffer)
                }

                function encodeBlobAsArrayBuffer(packet, supportsBinary, callback) {
                    if (!supportsBinary) {
                        return exports.encodeBase64Packet(packet, callback)
                    }
                    var fr = new FileReader;
                    fr.onload = function () {
                        packet.data = fr.result;
                        exports.encodePacket(packet, supportsBinary, true, callback)
                    };
                    return fr.readAsArrayBuffer(packet.data)
                }

                function encodeBlob(packet, supportsBinary, callback) {
                    if (!supportsBinary) {
                        return exports.encodeBase64Packet(packet, callback)
                    }
                    if (isAndroid) {
                        return encodeBlobAsArrayBuffer(packet, supportsBinary, callback)
                    }
                    var length = new Uint8Array(1);
                    length[0] = packets[packet.type];
                    var blob = new Blob([length.buffer, packet.data]);
                    return callback(blob)
                }

                exports.encodeBase64Packet = function (packet, callback) {
                    var message = "b" + exports.packets[packet.type];
                    if (Blob && packet.data instanceof Blob) {
                        var fr = new FileReader;
                        fr.onload = function () {
                            var b64 = fr.result.split(",")[1];
                            callback(message + b64)
                        };
                        return fr.readAsDataURL(packet.data)
                    }
                    var b64data;
                    try {
                        b64data = String.fromCharCode.apply(null, new Uint8Array(packet.data))
                    } catch (e) {
                        var typed = new Uint8Array(packet.data);
                        var basic = new Array(typed.length);
                        for (var i = 0; i < typed.length; i++) {
                            basic[i] = typed[i]
                        }
                        b64data = String.fromCharCode.apply(null, basic)
                    }
                    message += global.btoa(b64data);
                    return callback(message)
                };
                exports.decodePacket = function (data, binaryType, utf8decode) {
                    if (typeof data == "string" || data === undefined) {
                        if (data.charAt(0) == "b") {
                            return exports.decodeBase64Packet(data.substr(1), binaryType)
                        }
                        if (utf8decode) {
                            try {
                                data = utf8.decode(data)
                            } catch (e) {
                                return err
                            }
                        }
                        var type = data.charAt(0);
                        if (Number(type) != type || !packetslist[type]) {
                            return err
                        }
                        if (data.length > 1) {
                            return {type: packetslist[type], data: data.substring(1)}
                        } else {
                            return {type: packetslist[type]}
                        }
                    }
                    var asArray = new Uint8Array(data);
                    var type = asArray[0];
                    var rest = sliceBuffer(data, 1);
                    if (Blob && binaryType === "blob") {
                        rest = new Blob([rest])
                    }
                    return {type: packetslist[type], data: rest}
                };
                exports.decodeBase64Packet = function (msg, binaryType) {
                    var type = packetslist[msg.charAt(0)];
                    if (!global.ArrayBuffer) {
                        return {type: type, data: {base64: true, data: msg.substr(1)}}
                    }
                    var data = base64encoder.decode(msg.substr(1));
                    if (binaryType === "blob" && Blob) {
                        data = new Blob([data])
                    }
                    return {type: type, data: data}
                };
                exports.encodePayload = function (packets, supportsBinary, callback) {
                    if (typeof supportsBinary == "function") {
                        callback = supportsBinary;
                        supportsBinary = null
                    }
                    if (supportsBinary) {
                        if (Blob && !isAndroid) {
                            return exports.encodePayloadAsBlob(packets, callback)
                        }
                        return exports.encodePayloadAsArrayBuffer(packets, callback)
                    }
                    if (!packets.length) {
                        return callback("0:")
                    }

                    function setLengthHeader(message) {
                        return message.length + ":" + message
                    }

                    function encodeOne(packet, doneCallback) {
                        exports.encodePacket(packet, supportsBinary, true, function (message) {
                            doneCallback(null, setLengthHeader(message))
                        })
                    }

                    map(packets, encodeOne, function (err, results) {
                        return callback(results.join(""))
                    })
                };

                function map(ary, each, done) {
                    var result = new Array(ary.length);
                    var next = after(ary.length, done);
                    var eachWithIndex = function (i, el, cb) {
                        each(el, function (error, msg) {
                            result[i] = msg;
                            cb(error, result)
                        })
                    };
                    for (var i = 0; i < ary.length; i++) {
                        eachWithIndex(i, ary[i], next)
                    }
                }

                exports.decodePayload = function (data, binaryType, callback) {
                    if (typeof data != "string") {
                        return exports.decodePayloadAsBinary(data, binaryType, callback)
                    }
                    if (typeof binaryType === "function") {
                        callback = binaryType;
                        binaryType = null
                    }
                    var packet;
                    if (data == "") {
                        return callback(err, 0, 1)
                    }
                    var length = "", n, msg;
                    for (var i = 0, l = data.length; i < l; i++) {
                        var chr = data.charAt(i);
                        if (":" != chr) {
                            length += chr
                        } else {
                            if ("" == length || length != (n = Number(length))) {
                                return callback(err, 0, 1)
                            }
                            msg = data.substr(i + 1, n);
                            if (length != msg.length) {
                                return callback(err, 0, 1)
                            }
                            if (msg.length) {
                                packet = exports.decodePacket(msg, binaryType, true);
                                if (err.type == packet.type && err.data == packet.data) {
                                    return callback(err, 0, 1)
                                }
                                var ret = callback(packet, i + n, l);
                                if (false === ret) return
                            }
                            i += n;
                            length = ""
                        }
                    }
                    if (length != "") {
                        return callback(err, 0, 1)
                    }
                };
                exports.encodePayloadAsArrayBuffer = function (packets, callback) {
                    if (!packets.length) {
                        return callback(new ArrayBuffer(0))
                    }

                    function encodeOne(packet, doneCallback) {
                        exports.encodePacket(packet, true, true, function (data) {
                            return doneCallback(null, data)
                        })
                    }

                    map(packets, encodeOne, function (err, encodedPackets) {
                        var totalLength = encodedPackets.reduce(function (acc, p) {
                            var len;
                            if (typeof p === "string") {
                                len = p.length
                            } else {
                                len = p.byteLength
                            }
                            return acc + len.toString().length + len + 2
                        }, 0);
                        var resultArray = new Uint8Array(totalLength);
                        var bufferIndex = 0;
                        encodedPackets.forEach(function (p) {
                            var isString = typeof p === "string";
                            var ab = p;
                            if (isString) {
                                var view = new Uint8Array(p.length);
                                for (var i = 0; i < p.length; i++) {
                                    view[i] = p.charCodeAt(i)
                                }
                                ab = view.buffer
                            }
                            if (isString) {
                                resultArray[bufferIndex++] = 0
                            } else {
                                resultArray[bufferIndex++] = 1
                            }
                            var lenStr = ab.byteLength.toString();
                            for (var i = 0; i < lenStr.length; i++) {
                                resultArray[bufferIndex++] = parseInt(lenStr[i])
                            }
                            resultArray[bufferIndex++] = 255;
                            var view = new Uint8Array(ab);
                            for (var i = 0; i < view.length; i++) {
                                resultArray[bufferIndex++] = view[i]
                            }
                        });
                        return callback(resultArray.buffer)
                    })
                };
                exports.encodePayloadAsBlob = function (packets, callback) {
                    function encodeOne(packet, doneCallback) {
                        exports.encodePacket(packet, true, true, function (encoded) {
                            var binaryIdentifier = new Uint8Array(1);
                            binaryIdentifier[0] = 1;
                            if (typeof encoded === "string") {
                                var view = new Uint8Array(encoded.length);
                                for (var i = 0; i < encoded.length; i++) {
                                    view[i] = encoded.charCodeAt(i)
                                }
                                encoded = view.buffer;
                                binaryIdentifier[0] = 0
                            }
                            var len = encoded instanceof ArrayBuffer ? encoded.byteLength : encoded.size;
                            var lenStr = len.toString();
                            var lengthAry = new Uint8Array(lenStr.length + 1);
                            for (var i = 0; i < lenStr.length; i++) {
                                lengthAry[i] = parseInt(lenStr[i])
                            }
                            lengthAry[lenStr.length] = 255;
                            if (Blob) {
                                var blob = new Blob([binaryIdentifier.buffer, lengthAry.buffer, encoded]);
                                doneCallback(null, blob)
                            }
                        })
                    }

                    map(packets, encodeOne, function (err, results) {
                        return callback(new Blob(results))
                    })
                };
                exports.decodePayloadAsBinary = function (data, binaryType, callback) {
                    if (typeof binaryType === "function") {
                        callback = binaryType;
                        binaryType = null
                    }
                    var bufferTail = data;
                    var buffers = [];
                    var numberTooLong = false;
                    while (bufferTail.byteLength > 0) {
                        var tailArray = new Uint8Array(bufferTail);
                        var isString = tailArray[0] === 0;
                        var msgLength = "";
                        for (var i = 1; ; i++) {
                            if (tailArray[i] == 255) break;
                            if (msgLength.length > 310) {
                                numberTooLong = true;
                                break
                            }
                            msgLength += tailArray[i]
                        }
                        if (numberTooLong) return callback(err, 0, 1);
                        bufferTail = sliceBuffer(bufferTail, 2 + msgLength.length);
                        msgLength = parseInt(msgLength);
                        var msg = sliceBuffer(bufferTail, 0, msgLength);
                        if (isString) {
                            try {
                                msg = String.fromCharCode.apply(null, new Uint8Array(msg))
                            } catch (e) {
                                var typed = new Uint8Array(msg);
                                msg = "";
                                for (var i = 0; i < typed.length; i++) {
                                    msg += String.fromCharCode(typed[i])
                                }
                            }
                        }
                        buffers.push(msg);
                        bufferTail = sliceBuffer(bufferTail, msgLength)
                    }
                    var total = buffers.length;
                    buffers.forEach(function (buffer, i) {
                        callback(exports.decodePacket(buffer, binaryType, true), i, total)
                    })
                }
            }).call(this, typeof self !== "undefined" ? self : typeof window !== "undefined" ? window : {})
        }, {"./keys": 22, after: 23, "arraybuffer.slice": 24, "base64-arraybuffer": 25, blob: 26, utf8: 27}],
        22: [function (_dereq_, module, exports) {
            module.exports = Object.keys || function keys(obj) {
                var arr = [];
                var has = Object.prototype.hasOwnProperty;
                for (var i in obj) {
                    if (has.call(obj, i)) {
                        arr.push(i)
                    }
                }
                return arr
            }
        }, {}],
        23: [function (_dereq_, module, exports) {
            module.exports = after;

            function after(count, callback, err_cb) {
                var bail = false;
                err_cb = err_cb || noop;
                proxy.count = count;
                return count === 0 ? callback() : proxy;

                function proxy(err, result) {
                    if (proxy.count <= 0) {
                        throw new Error("after called too many times")
                    }
                    --proxy.count;
                    if (err) {
                        bail = true;
                        callback(err);
                        callback = err_cb
                    } else if (proxy.count === 0 && !bail) {
                        callback(null, result)
                    }
                }
            }

            function noop() {
            }
        }, {}],
        24: [function (_dereq_, module, exports) {
            module.exports = function (arraybuffer, start, end) {
                var bytes = arraybuffer.byteLength;
                start = start || 0;
                end = end || bytes;
                if (arraybuffer.slice) {
                    return arraybuffer.slice(start, end)
                }
                if (start < 0) {
                    start += bytes
                }
                if (end < 0) {
                    end += bytes
                }
                if (end > bytes) {
                    end = bytes
                }
                if (start >= bytes || start >= end || bytes === 0) {
                    return new ArrayBuffer(0)
                }
                var abv = new Uint8Array(arraybuffer);
                var result = new Uint8Array(end - start);
                for (var i = start, ii = 0; i < end; i++, ii++) {
                    result[ii] = abv[i]
                }
                return result.buffer
            }
        }, {}],
        25: [function (_dereq_, module, exports) {
            (function (chars) {
                "use strict";
                exports.encode = function (arraybuffer) {
                    var bytes = new Uint8Array(arraybuffer), i, len = bytes.length, base64 = "";
                    for (i = 0; i < len; i += 3) {
                        base64 += chars[bytes[i] >> 2];
                        base64 += chars[(bytes[i] & 3) << 4 | bytes[i + 1] >> 4];
                        base64 += chars[(bytes[i + 1] & 15) << 2 | bytes[i + 2] >> 6];
                        base64 += chars[bytes[i + 2] & 63]
                    }
                    if (len % 3 === 2) {
                        base64 = base64.substring(0, base64.length - 1) + "="
                    } else if (len % 3 === 1) {
                        base64 = base64.substring(0, base64.length - 2) + "=="
                    }
                    return base64
                };
                exports.decode = function (base64) {
                    var bufferLength = base64.length * .75, len = base64.length, i, p = 0, encoded1, encoded2, encoded3,
                        encoded4;
                    if (base64[base64.length - 1] === "=") {
                        bufferLength--;
                        if (base64[base64.length - 2] === "=") {
                            bufferLength--
                        }
                    }
                    var arraybuffer = new ArrayBuffer(bufferLength), bytes = new Uint8Array(arraybuffer);
                    for (i = 0; i < len; i += 4) {
                        encoded1 = chars.indexOf(base64[i]);
                        encoded2 = chars.indexOf(base64[i + 1]);
                        encoded3 = chars.indexOf(base64[i + 2]);
                        encoded4 = chars.indexOf(base64[i + 3]);
                        bytes[p++] = encoded1 << 2 | encoded2 >> 4;
                        bytes[p++] = (encoded2 & 15) << 4 | encoded3 >> 2;
                        bytes[p++] = (encoded3 & 3) << 6 | encoded4 & 63
                    }
                    return arraybuffer
                }
            })("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/")
        }, {}],
        26: [function (_dereq_, module, exports) {
            (function (global) {
                var BlobBuilder = global.BlobBuilder || global.WebKitBlobBuilder || global.MSBlobBuilder || global.MozBlobBuilder;
                var blobSupported = function () {
                    try {
                        var b = new Blob(["hi"]);
                        return b.size == 2
                    } catch (e) {
                        return false
                    }
                }();
                var blobBuilderSupported = BlobBuilder && BlobBuilder.prototype.append && BlobBuilder.prototype.getBlob;

                function BlobBuilderConstructor(ary, options) {
                    options = options || {};
                    var bb = new BlobBuilder;
                    for (var i = 0; i < ary.length; i++) {
                        bb.append(ary[i])
                    }
                    return options.type ? bb.getBlob(options.type) : bb.getBlob()
                }

                module.exports = function () {
                    if (blobSupported) {
                        return global.Blob
                    } else if (blobBuilderSupported) {
                        return BlobBuilderConstructor
                    } else {
                        return undefined
                    }
                }()
            }).call(this, typeof self !== "undefined" ? self : typeof window !== "undefined" ? window : {})
        }, {}],
        27: [function (_dereq_, module, exports) {
            (function (global) {
                (function (root) {
                    var freeExports = typeof exports == "object" && exports;
                    var freeModule = typeof module == "object" && module && module.exports == freeExports && module;
                    var freeGlobal = typeof global == "object" && global;
                    if (freeGlobal.global === freeGlobal || freeGlobal.window === freeGlobal) {
                        root = freeGlobal
                    }
                    var stringFromCharCode = String.fromCharCode;

                    function ucs2decode(string) {
                        var output = [];
                        var counter = 0;
                        var length = string.length;
                        var value;
                        var extra;
                        while (counter < length) {
                            value = string.charCodeAt(counter++);
                            if (value >= 55296 && value <= 56319 && counter < length) {
                                extra = string.charCodeAt(counter++);
                                if ((extra & 64512) == 56320) {
                                    output.push(((value & 1023) << 10) + (extra & 1023) + 65536)
                                } else {
                                    output.push(value);
                                    counter--
                                }
                            } else {
                                output.push(value)
                            }
                        }
                        return output
                    }

                    function ucs2encode(array) {
                        var length = array.length;
                        var index = -1;
                        var value;
                        var output = "";
                        while (++index < length) {
                            value = array[index];
                            if (value > 65535) {
                                value -= 65536;
                                output += stringFromCharCode(value >>> 10 & 1023 | 55296);
                                value = 56320 | value & 1023
                            }
                            output += stringFromCharCode(value)
                        }
                        return output
                    }

                    function createByte(codePoint, shift) {
                        return stringFromCharCode(codePoint >> shift & 63 | 128)
                    }

                    function encodeCodePoint(codePoint) {
                        if ((codePoint & 4294967168) == 0) {
                            return stringFromCharCode(codePoint)
                        }
                        var symbol = "";
                        if ((codePoint & 4294965248) == 0) {
                            symbol = stringFromCharCode(codePoint >> 6 & 31 | 192)
                        } else if ((codePoint & 4294901760) == 0) {
                            symbol = stringFromCharCode(codePoint >> 12 & 15 | 224);
                            symbol += createByte(codePoint, 6)
                        } else if ((codePoint & 4292870144) == 0) {
                            symbol = stringFromCharCode(codePoint >> 18 & 7 | 240);
                            symbol += createByte(codePoint, 12);
                            symbol += createByte(codePoint, 6)
                        }
                        symbol += stringFromCharCode(codePoint & 63 | 128);
                        return symbol
                    }

                    function utf8encode(string) {
                        var codePoints = ucs2decode(string);
                        var length = codePoints.length;
                        var index = -1;
                        var codePoint;
                        var byteString = "";
                        while (++index < length) {
                            codePoint = codePoints[index];
                            byteString += encodeCodePoint(codePoint)
                        }
                        return byteString
                    }

                    function readContinuationByte() {
                        if (byteIndex >= byteCount) {
                            throw Error("Invalid byte index")
                        }
                        var continuationByte = byteArray[byteIndex] & 255;
                        byteIndex++;
                        if ((continuationByte & 192) == 128) {
                            return continuationByte & 63
                        }
                        throw Error("Invalid continuation byte")
                    }

                    function decodeSymbol() {
                        var byte1;
                        var byte2;
                        var byte3;
                        var byte4;
                        var codePoint;
                        if (byteIndex > byteCount) {
                            throw Error("Invalid byte index")
                        }
                        if (byteIndex == byteCount) {
                            return false
                        }
                        byte1 = byteArray[byteIndex] & 255;
                        byteIndex++;
                        if ((byte1 & 128) == 0) {
                            return byte1
                        }
                        if ((byte1 & 224) == 192) {
                            var byte2 = readContinuationByte();
                            codePoint = (byte1 & 31) << 6 | byte2;
                            if (codePoint >= 128) {
                                return codePoint
                            } else {
                                throw Error("Invalid continuation byte")
                            }
                        }
                        if ((byte1 & 240) == 224) {
                            byte2 = readContinuationByte();
                            byte3 = readContinuationByte();
                            codePoint = (byte1 & 15) << 12 | byte2 << 6 | byte3;
                            if (codePoint >= 2048) {
                                return codePoint
                            } else {
                                throw Error("Invalid continuation byte")
                            }
                        }
                        if ((byte1 & 248) == 240) {
                            byte2 = readContinuationByte();
                            byte3 = readContinuationByte();
                            byte4 = readContinuationByte();
                            codePoint = (byte1 & 15) << 18 | byte2 << 12 | byte3 << 6 | byte4;
                            if (codePoint >= 65536 && codePoint <= 1114111) {
                                return codePoint
                            }
                        }
                        throw Error("Invalid UTF-8 detected")
                    }

                    var byteArray;
                    var byteCount;
                    var byteIndex;

                    function utf8decode(byteString) {
                        byteArray = ucs2decode(byteString);
                        byteCount = byteArray.length;
                        byteIndex = 0;
                        var codePoints = [];
                        var tmp;
                        while ((tmp = decodeSymbol()) !== false) {
                            codePoints.push(tmp)
                        }
                        return ucs2encode(codePoints)
                    }

                    var utf8 = {version: "2.0.0", encode: utf8encode, decode: utf8decode};
                    if (typeof define == "function" && typeof define.amd == "object" && define.amd) {
                        define(function () {
                            return utf8
                        })
                    } else if (freeExports && !freeExports.nodeType) {
                        if (freeModule) {
                            freeModule.exports = utf8
                        } else {
                            var object = {};
                            var hasOwnProperty = object.hasOwnProperty;
                            for (var key in utf8) {
                                hasOwnProperty.call(utf8, key) && (freeExports[key] = utf8[key])
                            }
                        }
                    } else {
                        root.utf8 = utf8
                    }
                })(this)
            }).call(this, typeof self !== "undefined" ? self : typeof window !== "undefined" ? window : {})
        }, {}],
        28: [function (_dereq_, module, exports) {
            (function (global) {
                var rvalidchars = /^[\],:{}\s]*$/;
                var rvalidescape = /\\(?:["\\\/bfnrt]|u[0-9a-fA-F]{4})/g;
                var rvalidtokens = /"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g;
                var rvalidbraces = /(?:^|:|,)(?:\s*\[)+/g;
                var rtrimLeft = /^\s+/;
                var rtrimRight = /\s+$/;
                module.exports = function parsejson(data) {
                    if ("string" != typeof data || !data) {
                        return null
                    }
                    data = data.replace(rtrimLeft, "").replace(rtrimRight, "");
                    if (global.JSON && JSON.parse) {
                        return JSON.parse(data)
                    }
                    if (rvalidchars.test(data.replace(rvalidescape, "@").replace(rvalidtokens, "]").replace(rvalidbraces, ""))) {
                        return new Function("return " + data)()
                    }
                }
            }).call(this, typeof self !== "undefined" ? self : typeof window !== "undefined" ? window : {})
        }, {}],
        29: [function (_dereq_, module, exports) {
            exports.encode = function (obj) {
                var str = "";
                for (var i in obj) {
                    if (obj.hasOwnProperty(i)) {
                        if (str.length) str += "&";
                        str += encodeURIComponent(i) + "=" + encodeURIComponent(obj[i])
                    }
                }
                return str
            };
            exports.decode = function (qs) {
                var qry = {};
                var pairs = qs.split("&");
                for (var i = 0, l = pairs.length; i < l; i++) {
                    var pair = pairs[i].split("=");
                    qry[decodeURIComponent(pair[0])] = decodeURIComponent(pair[1])
                }
                return qry
            }
        }, {}],
        30: [function (_dereq_, module, exports) {
            var re = /^(?:(?![^:@]+:[^:@\/]*@)(http|https|ws|wss):\/\/)?((?:(([^:@]*)(?::([^:@]*))?)?@)?((?:[a-f0-9]{0,4}:){2,7}[a-f0-9]{0,4}|[^:\/?#]*)(?::(\d*))?)(((\/(?:[^?#](?![^?#\/]*\.[^?#\/.]+(?:[?#]|$)))*\/?)?([^?#\/]*))(?:\?([^#]*))?(?:#(.*))?)/;
            var parts = ["source", "protocol", "authority", "userInfo", "user", "password", "host", "port", "relative", "path", "directory", "file", "query", "anchor"];
            module.exports = function parseuri(str) {
                var src = str, b = str.indexOf("["), e = str.indexOf("]");
                if (b != -1 && e != -1) {
                    str = str.substring(0, b) + str.substring(b, e).replace(/:/g, ";") + str.substring(e, str.length)
                }
                var m = re.exec(str || ""), uri = {}, i = 14;
                while (i--) {
                    uri[parts[i]] = m[i] || ""
                }
                if (b != -1 && e != -1) {
                    uri.source = src;
                    uri.host = uri.host.substring(1, uri.host.length - 1).replace(/;/g, ":");
                    uri.authority = uri.authority.replace("[", "").replace("]", "").replace(/;/g, ":");
                    uri.ipv6uri = true
                }
                return uri
            }
        }, {}],
        31: [function (_dereq_, module, exports) {
            var global = function () {
                return this
            }();
            var WebSocket = global.WebSocket || global.MozWebSocket;
            module.exports = WebSocket ? ws : null;

            function ws(uri, protocols, opts) {
                var instance;
                if (protocols) {
                    instance = new WebSocket(uri, protocols)
                } else {
                    instance = new WebSocket(uri)
                }
                return instance
            }

            if (WebSocket) ws.prototype = WebSocket.prototype
        }, {}],
        32: [function (_dereq_, module, exports) {
            (function (global) {
                var isArray = _dereq_("isarray");
                module.exports = hasBinary;

                function hasBinary(data) {
                    function _hasBinary(obj) {
                        if (!obj) return false;
                        if (global.Buffer && global.Buffer.isBuffer(obj) || global.ArrayBuffer && obj instanceof ArrayBuffer || global.Blob && obj instanceof Blob || global.File && obj instanceof File) {
                            return true
                        }
                        if (isArray(obj)) {
                            for (var i = 0; i < obj.length; i++) {
                                if (_hasBinary(obj[i])) {
                                    return true
                                }
                            }
                        } else if (obj && "object" == typeof obj) {
                            if (obj.toJSON) {
                                obj = obj.toJSON()
                            }
                            for (var key in obj) {
                                if (obj.hasOwnProperty(key) && _hasBinary(obj[key])) {
                                    return true
                                }
                            }
                        }
                        return false
                    }

                    return _hasBinary(data)
                }
            }).call(this, typeof self !== "undefined" ? self : typeof window !== "undefined" ? window : {})
        }, {isarray: 33}],
        33: [function (_dereq_, module, exports) {
            module.exports = Array.isArray || function (arr) {
                return Object.prototype.toString.call(arr) == "[object Array]"
            }
        }, {}],
        34: [function (_dereq_, module, exports) {
            var global = _dereq_("global");
            try {
                module.exports = "XMLHttpRequest" in global && "withCredentials" in new global.XMLHttpRequest
            } catch (err) {
                module.exports = false
            }
        }, {global: 35}],
        35: [function (_dereq_, module, exports) {
            module.exports = function () {
                return this
            }()
        }, {}],
        36: [function (_dereq_, module, exports) {
            var indexOf = [].indexOf;
            module.exports = function (arr, obj) {
                if (indexOf) return arr.indexOf(obj);
                for (var i = 0; i < arr.length; ++i) {
                    if (arr[i] === obj) return i
                }
                return -1
            }
        }, {}],
        37: [function (_dereq_, module, exports) {
            var has = Object.prototype.hasOwnProperty;
            exports.keys = Object.keys || function (obj) {
                var keys = [];
                for (var key in obj) {
                    if (has.call(obj, key)) {
                        keys.push(key)
                    }
                }
                return keys
            };
            exports.values = function (obj) {
                var vals = [];
                for (var key in obj) {
                    if (has.call(obj, key)) {
                        vals.push(obj[key])
                    }
                }
                return vals
            };
            exports.merge = function (a, b) {
                for (var key in b) {
                    if (has.call(b, key)) {
                        a[key] = b[key]
                    }
                }
                return a
            };
            exports.length = function (obj) {
                return exports.keys(obj).length
            };
            exports.isEmpty = function (obj) {
                return 0 == exports.length(obj)
            }
        }, {}],
        38: [function (_dereq_, module, exports) {
            var re = /^(?:(?![^:@]+:[^:@\/]*@)(http|https|ws|wss):\/\/)?((?:(([^:@]*)(?::([^:@]*))?)?@)?((?:[a-f0-9]{0,4}:){2,7}[a-f0-9]{0,4}|[^:\/?#]*)(?::(\d*))?)(((\/(?:[^?#](?![^?#\/]*\.[^?#\/.]+(?:[?#]|$)))*\/?)?([^?#\/]*))(?:\?([^#]*))?(?:#(.*))?)/;
            var parts = ["source", "protocol", "authority", "userInfo", "user", "password", "host", "port", "relative", "path", "directory", "file", "query", "anchor"];
            module.exports = function parseuri(str) {
                var m = re.exec(str || ""), uri = {}, i = 14;
                while (i--) {
                    uri[parts[i]] = m[i] || ""
                }
                return uri
            }
        }, {}],
        39: [function (_dereq_, module, exports) {
            (function (global) {
                var isArray = _dereq_("isarray");
                var isBuf = _dereq_("./is-buffer");
                exports.deconstructPacket = function (packet) {
                    var buffers = [];
                    var packetData = packet.data;

                    function _deconstructPacket(data) {
                        if (!data) return data;
                        if (isBuf(data)) {
                            var placeholder = {_placeholder: true, num: buffers.length};
                            buffers.push(data);
                            return placeholder
                        } else if (isArray(data)) {
                            var newData = new Array(data.length);
                            for (var i = 0; i < data.length; i++) {
                                newData[i] = _deconstructPacket(data[i])
                            }
                            return newData
                        } else if ("object" == typeof data && !(data instanceof Date)) {
                            var newData = {};
                            for (var key in data) {
                                newData[key] = _deconstructPacket(data[key])
                            }
                            return newData
                        }
                        return data
                    }

                    var pack = packet;
                    pack.data = _deconstructPacket(packetData);
                    pack.attachments = buffers.length;
                    return {packet: pack, buffers: buffers}
                };
                exports.reconstructPacket = function (packet, buffers) {
                    var curPlaceHolder = 0;

                    function _reconstructPacket(data) {
                        if (data && data._placeholder) {
                            var buf = buffers[data.num];
                            return buf
                        } else if (isArray(data)) {
                            for (var i = 0; i < data.length; i++) {
                                data[i] = _reconstructPacket(data[i])
                            }
                            return data
                        } else if (data && "object" == typeof data) {
                            for (var key in data) {
                                data[key] = _reconstructPacket(data[key])
                            }
                            return data
                        }
                        return data
                    }

                    packet.data = _reconstructPacket(packet.data);
                    packet.attachments = undefined;
                    return packet
                };
                exports.removeBlobs = function (data, callback) {
                    function _removeBlobs(obj, curKey, containingObject) {
                        if (!obj) return obj;
                        if (global.Blob && obj instanceof Blob || global.File && obj instanceof File) {
                            pendingBlobs++;
                            var fileReader = new FileReader;
                            fileReader.onload = function () {
                                if (containingObject) {
                                    containingObject[curKey] = this.result
                                } else {
                                    bloblessData = this.result
                                }
                                if (!--pendingBlobs) {
                                    callback(bloblessData)
                                }
                            };
                            fileReader.readAsArrayBuffer(obj)
                        } else if (isArray(obj)) {
                            for (var i = 0; i < obj.length; i++) {
                                _removeBlobs(obj[i], i, obj)
                            }
                        } else if (obj && "object" == typeof obj && !isBuf(obj)) {
                            for (var key in obj) {
                                _removeBlobs(obj[key], key, obj)
                            }
                        }
                    }

                    var pendingBlobs = 0;
                    var bloblessData = data;
                    _removeBlobs(bloblessData);
                    if (!pendingBlobs) {
                        callback(bloblessData)
                    }
                }
            }).call(this, typeof self !== "undefined" ? self : typeof window !== "undefined" ? window : {})
        }, {"./is-buffer": 41, isarray: 42}],
        40: [function (_dereq_, module, exports) {
            var debug = _dereq_("debug")("socket.io-parser");
            var json = _dereq_("json3");
            var isArray = _dereq_("isarray");
            var Emitter = _dereq_("component-emitter");
            var binary = _dereq_("./binary");
            var isBuf = _dereq_("./is-buffer");
            exports.protocol = 4;
            exports.types = ["CONNECT", "DISCONNECT", "EVENT", "BINARY_EVENT", "ACK", "BINARY_ACK", "ERROR"];
            exports.CONNECT = 0;
            exports.DISCONNECT = 1;
            exports.EVENT = 2;
            exports.ACK = 3;
            exports.ERROR = 4;
            exports.BINARY_EVENT = 5;
            exports.BINARY_ACK = 6;
            exports.Encoder = Encoder;
            exports.Decoder = Decoder;

            function Encoder() {
            }

            Encoder.prototype.encode = function (obj, callback) {
                debug("encoding packet %j", obj);
                if (exports.BINARY_EVENT == obj.type || exports.BINARY_ACK == obj.type) {
                    encodeAsBinary(obj, callback)
                } else {
                    var encoding = encodeAsString(obj);
                    callback([encoding])
                }
            };

            function encodeAsString(obj) {
                var str = "";
                var nsp = false;
                str += obj.type;
                if (exports.BINARY_EVENT == obj.type || exports.BINARY_ACK == obj.type) {
                    str += obj.attachments;
                    str += "-"
                }
                if (obj.nsp && "/" != obj.nsp) {
                    nsp = true;
                    str += obj.nsp
                }
                if (null != obj.id) {
                    if (nsp) {
                        str += ",";
                        nsp = false
                    }
                    str += obj.id
                }
                if (null != obj.data) {
                    if (nsp) str += ",";
                    str += json.stringify(obj.data)
                }
                debug("encoded %j as %s", obj, str);
                return str
            }

            function encodeAsBinary(obj, callback) {
                function writeEncoding(bloblessData) {
                    var deconstruction = binary.deconstructPacket(bloblessData);
                    var pack = encodeAsString(deconstruction.packet);
                    var buffers = deconstruction.buffers;
                    buffers.unshift(pack);
                    callback(buffers)
                }

                binary.removeBlobs(obj, writeEncoding)
            }

            function Decoder() {
                this.reconstructor = null
            }

            Emitter(Decoder.prototype);
            Decoder.prototype.add = function (obj) {
                var packet;
                if ("string" == typeof obj) {
                    packet = decodeString(obj);
                    if (exports.BINARY_EVENT == packet.type || exports.BINARY_ACK == packet.type) {
                        this.reconstructor = new BinaryReconstructor(packet);
                        if (this.reconstructor.reconPack.attachments == 0) {
                            this.emit("decoded", packet)
                        }
                    } else {
                        this.emit("decoded", packet)
                    }
                } else if (isBuf(obj) || obj.base64) {
                    if (!this.reconstructor) {
                        throw new Error("got binary data when not reconstructing a packet")
                    } else {
                        packet = this.reconstructor.takeBinaryData(obj);
                        if (packet) {
                            this.reconstructor = null;
                            this.emit("decoded", packet)
                        }
                    }
                } else {
                    throw new Error("Unknown type: " + obj)
                }
            };

            function decodeString(str) {
                var p = {};
                var i = 0;
                p.type = Number(str.charAt(0));
                if (null == exports.types[p.type]) return error();
                if (exports.BINARY_EVENT == p.type || exports.BINARY_ACK == p.type) {
                    p.attachments = "";
                    while (str.charAt(++i) != "-") {
                        p.attachments += str.charAt(i)
                    }
                    p.attachments = Number(p.attachments)
                }
                if ("/" == str.charAt(i + 1)) {
                    p.nsp = "";
                    while (++i) {
                        var c = str.charAt(i);
                        if ("," == c) break;
                        p.nsp += c;
                        if (i + 1 == str.length) break
                    }
                } else {
                    p.nsp = "/"
                }
                var next = str.charAt(i + 1);
                if ("" != next && Number(next) == next) {
                    p.id = "";
                    while (++i) {
                        var c = str.charAt(i);
                        if (null == c || Number(c) != c) {
                            --i;
                            break
                        }
                        p.id += str.charAt(i);
                        if (i + 1 == str.length) break
                    }
                    p.id = Number(p.id)
                }
                if (str.charAt(++i)) {
                    try {
                        p.data = json.parse(str.substr(i))
                    } catch (e) {
                        return error()
                    }
                }
                debug("decoded %s as %j", str, p);
                return p
            }

            Decoder.prototype.destroy = function () {
                if (this.reconstructor) {
                    this.reconstructor.finishedReconstruction()
                }
            };

            function BinaryReconstructor(packet) {
                this.reconPack = packet;
                this.buffers = []
            }

            BinaryReconstructor.prototype.takeBinaryData = function (binData) {
                this.buffers.push(binData);
                if (this.buffers.length == this.reconPack.attachments) {
                    var packet = binary.reconstructPacket(this.reconPack, this.buffers);
                    this.finishedReconstruction();
                    return packet
                }
                return null
            };
            BinaryReconstructor.prototype.finishedReconstruction = function () {
                this.reconPack = null;
                this.buffers = []
            };

            function error(data) {
                return {type: exports.ERROR, data: "parser error"}
            }
        }, {"./binary": 39, "./is-buffer": 41, "component-emitter": 8, debug: 9, isarray: 42, json3: 43}],
        41: [function (_dereq_, module, exports) {
            (function (global) {
                module.exports = isBuf;

                function isBuf(obj) {
                    return global.Buffer && global.Buffer.isBuffer(obj) || global.ArrayBuffer && obj instanceof ArrayBuffer
                }
            }).call(this, typeof self !== "undefined" ? self : typeof window !== "undefined" ? window : {})
        }, {}],
        42: [function (_dereq_, module, exports) {
            module.exports = _dereq_(33)
        }, {}],
        43: [function (_dereq_, module, exports) {
            (function (window) {
                var getClass = {}.toString, isProperty, forEach, undef;
                var isLoader = typeof define === "function" && define.amd;
                var nativeJSON = typeof JSON == "object" && JSON;
                var JSON3 = typeof exports == "object" && exports && !exports.nodeType && exports;
                if (JSON3 && nativeJSON) {
                    JSON3.stringify = nativeJSON.stringify;
                    JSON3.parse = nativeJSON.parse
                } else {
                    JSON3 = window.JSON = nativeJSON || {}
                }
                var isExtended = new Date(-0xc782b5b800cec);
                try {
                    isExtended = isExtended.getUTCFullYear() == -109252 && isExtended.getUTCMonth() === 0 && isExtended.getUTCDate() === 1 && isExtended.getUTCHours() == 10 && isExtended.getUTCMinutes() == 37 && isExtended.getUTCSeconds() == 6 && isExtended.getUTCMilliseconds() == 708
                } catch (exception) {
                }

                function has(name) {
                    if (has[name] !== undef) {
                        return has[name]
                    }
                    var isSupported;
                    if (name == "bug-string-char-index") {
                        isSupported = "a"[0] != "a"
                    } else if (name == "json") {
                        isSupported = has("json-stringify") && has("json-parse")
                    } else {
                        var value, serialized = '{"a":[1,true,false,null,"\\u0000\\b\\n\\f\\r\\t"]}';
                        if (name == "json-stringify") {
                            var stringify = JSON3.stringify,
                                stringifySupported = typeof stringify == "function" && isExtended;
                            if (stringifySupported) {
                                (value = function () {
                                    return 1
                                }).toJSON = value;
                                try {
                                    stringifySupported = stringify(0) === "0" && stringify(new Number) === "0" && stringify(new String) == '""' && stringify(getClass) === undef && stringify(undef) === undef && stringify() === undef && stringify(value) === "1" && stringify([value]) == "[1]" && stringify([undef]) == "[null]" && stringify(null) == "null" && stringify([undef, getClass, null]) == "[null,null,null]" && stringify({a: [value, true, false, null, "\x00\b\n\f\r	"]}) == serialized && stringify(null, value) === "1" && stringify([1, 2], null, 1) == "[\n 1,\n 2\n]" && stringify(new Date(-864e13)) == '"-271821-04-20T00:00:00.000Z"' && stringify(new Date(864e13)) == '"+275760-09-13T00:00:00.000Z"' && stringify(new Date(-621987552e5)) == '"-000001-01-01T00:00:00.000Z"' && stringify(new Date(-1)) == '"1969-12-31T23:59:59.999Z"'
                                } catch (exception) {
                                    stringifySupported = false
                                }
                            }
                            isSupported = stringifySupported
                        }
                        if (name == "json-parse") {
                            var parse = JSON3.parse;
                            if (typeof parse == "function") {
                                try {
                                    if (parse("0") === 0 && !parse(false)) {
                                        value = parse(serialized);
                                        var parseSupported = value["a"].length == 5 && value["a"][0] === 1;
                                        if (parseSupported) {
                                            try {
                                                parseSupported = !parse('"	"')
                                            } catch (exception) {
                                            }
                                            if (parseSupported) {
                                                try {
                                                    parseSupported = parse("01") !== 1
                                                } catch (exception) {
                                                }
                                            }
                                            if (parseSupported) {
                                                try {
                                                    parseSupported = parse("1.") !== 1
                                                } catch (exception) {
                                                }
                                            }
                                        }
                                    }
                                } catch (exception) {
                                    parseSupported = false
                                }
                            }
                            isSupported = parseSupported
                        }
                    }
                    return has[name] = !!isSupported
                }

                if (!has("json")) {
                    var functionClass = "[object Function]";
                    var dateClass = "[object Date]";
                    var numberClass = "[object Number]";
                    var stringClass = "[object String]";
                    var arrayClass = "[object Array]";
                    var booleanClass = "[object Boolean]";
                    var charIndexBuggy = has("bug-string-char-index");
                    if (!isExtended) {
                        var floor = Math.floor;
                        var Months = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334];
                        var getDay = function (year, month) {
                            return Months[month] + 365 * (year - 1970) + floor((year - 1969 + (month = +(month > 1))) / 4) - floor((year - 1901 + month) / 100) + floor((year - 1601 + month) / 400)
                        }
                    }
                    if (!(isProperty = {}.hasOwnProperty)) {
                        isProperty = function (property) {
                            var members = {}, constructor;
                            if ((members.__proto__ = null, members.__proto__ = {toString: 1}, members).toString != getClass) {
                                isProperty = function (property) {
                                    var original = this.__proto__, result = property in (this.__proto__ = null, this);
                                    this.__proto__ = original;
                                    return result
                                }
                            } else {
                                constructor = members.constructor;
                                isProperty = function (property) {
                                    var parent = (this.constructor || constructor).prototype;
                                    return property in this && !(property in parent && this[property] === parent[property])
                                }
                            }
                            members = null;
                            return isProperty.call(this, property)
                        }
                    }
                    var PrimitiveTypes = {"boolean": 1, number: 1, string: 1, undefined: 1};
                    var isHostType = function (object, property) {
                        var type = typeof object[property];
                        return type == "object" ? !!object[property] : !PrimitiveTypes[type]
                    };
                    forEach = function (object, callback) {
                        var size = 0, Properties, members, property;
                        (Properties = function () {
                            this.valueOf = 0
                        }).prototype.valueOf = 0;
                        members = new Properties;
                        for (property in members) {
                            if (isProperty.call(members, property)) {
                                size++
                            }
                        }
                        Properties = members = null;
                        if (!size) {
                            members = ["valueOf", "toString", "toLocaleString", "propertyIsEnumerable", "isPrototypeOf", "hasOwnProperty", "constructor"];
                            forEach = function (object, callback) {
                                var isFunction = getClass.call(object) == functionClass, property, length;
                                var hasProperty = !isFunction && typeof object.constructor != "function" && isHostType(object, "hasOwnProperty") ? object.hasOwnProperty : isProperty;
                                for (property in object) {
                                    if (!(isFunction && property == "prototype") && hasProperty.call(object, property)) {
                                        callback(property)
                                    }
                                }
                                for (length = members.length; property = members[--length]; hasProperty.call(object, property) && callback(property)) ;
                            }
                        } else if (size == 2) {
                            forEach = function (object, callback) {
                                var members = {}, isFunction = getClass.call(object) == functionClass, property;
                                for (property in object) {
                                    if (!(isFunction && property == "prototype") && !isProperty.call(members, property) && (members[property] = 1) && isProperty.call(object, property)) {
                                        callback(property)
                                    }
                                }
                            }
                        } else {
                            forEach = function (object, callback) {
                                var isFunction = getClass.call(object) == functionClass, property, isConstructor;
                                for (property in object) {
                                    if (!(isFunction && property == "prototype") && isProperty.call(object, property) && !(isConstructor = property === "constructor")) {
                                        callback(property)
                                    }
                                }
                                if (isConstructor || isProperty.call(object, property = "constructor")) {
                                    callback(property)
                                }
                            }
                        }
                        return forEach(object, callback)
                    };
                    if (!has("json-stringify")) {
                        var Escapes = {92: "\\\\", 34: '\\"', 8: "\\b", 12: "\\f", 10: "\\n", 13: "\\r", 9: "\\t"};
                        var leadingZeroes = "000000";
                        var toPaddedString = function (width, value) {
                            return (leadingZeroes + (value || 0)).slice(-width)
                        };
                        var unicodePrefix = "\\u00";
                        var quote = function (value) {
                            var result = '"', index = 0, length = value.length, isLarge = length > 10 && charIndexBuggy,
                                symbols;
                            if (isLarge) {
                                symbols = value.split("")
                            }
                            for (; index < length; index++) {
                                var charCode = value.charCodeAt(index);
                                switch (charCode) {
                                    case 8:
                                    case 9:
                                    case 10:
                                    case 12:
                                    case 13:
                                    case 34:
                                    case 92:
                                        result += Escapes[charCode];
                                        break;
                                    default:
                                        if (charCode < 32) {
                                            result += unicodePrefix + toPaddedString(2, charCode.toString(16));
                                            break
                                        }
                                        result += isLarge ? symbols[index] : charIndexBuggy ? value.charAt(index) : value[index]
                                }
                            }
                            return result + '"'
                        };
                        var serialize = function (property, object, callback, properties, whitespace, indentation, stack) {
                            var value, className, year, month, date, time, hours, minutes, seconds, milliseconds,
                                results, element, index, length, prefix, result;
                            try {
                                value = object[property]
                            } catch (exception) {
                            }
                            if (typeof value == "object" && value) {
                                className = getClass.call(value);
                                if (className == dateClass && !isProperty.call(value, "toJSON")) {
                                    if (value > -1 / 0 && value < 1 / 0) {
                                        if (getDay) {
                                            date = floor(value / 864e5);
                                            for (year = floor(date / 365.2425) + 1970 - 1; getDay(year + 1, 0) <= date; year++) ;
                                            for (month = floor((date - getDay(year, 0)) / 30.42); getDay(year, month + 1) <= date; month++) ;
                                            date = 1 + date - getDay(year, month);
                                            time = (value % 864e5 + 864e5) % 864e5;
                                            hours = floor(time / 36e5) % 24;
                                            minutes = floor(time / 6e4) % 60;
                                            seconds = floor(time / 1e3) % 60;
                                            milliseconds = time % 1e3
                                        } else {
                                            year = value.getUTCFullYear();
                                            month = value.getUTCMonth();
                                            date = value.getUTCDate();
                                            hours = value.getUTCHours();
                                            minutes = value.getUTCMinutes();
                                            seconds = value.getUTCSeconds();
                                            milliseconds = value.getUTCMilliseconds()
                                        }
                                        value = (year <= 0 || year >= 1e4 ? (year < 0 ? "-" : "+") + toPaddedString(6, year < 0 ? -year : year) : toPaddedString(4, year)) + "-" + toPaddedString(2, month + 1) + "-" + toPaddedString(2, date) + "T" + toPaddedString(2, hours) + ":" + toPaddedString(2, minutes) + ":" + toPaddedString(2, seconds) + "." + toPaddedString(3, milliseconds) + "Z"
                                    } else {
                                        value = null
                                    }
                                } else if (typeof value.toJSON == "function" && (className != numberClass && className != stringClass && className != arrayClass || isProperty.call(value, "toJSON"))) {
                                    value = value.toJSON(property)
                                }
                            }
                            if (callback) {
                                value = callback.call(object, property, value)
                            }
                            if (value === null) {
                                return "null"
                            }
                            className = getClass.call(value);
                            if (className == booleanClass) {
                                return "" + value
                            } else if (className == numberClass) {
                                return value > -1 / 0 && value < 1 / 0 ? "" + value : "null"
                            } else if (className == stringClass) {
                                return quote("" + value)
                            }
                            if (typeof value == "object") {
                                for (length = stack.length; length--;) {
                                    if (stack[length] === value) {
                                        throw TypeError()
                                    }
                                }
                                stack.push(value);
                                results = [];
                                prefix = indentation;
                                indentation += whitespace;
                                if (className == arrayClass) {
                                    for (index = 0, length = value.length; index < length; index++) {
                                        element = serialize(index, value, callback, properties, whitespace, indentation, stack);
                                        results.push(element === undef ? "null" : element)
                                    }
                                    result = results.length ? whitespace ? "[\n" + indentation + results.join(",\n" + indentation) + "\n" + prefix + "]" : "[" + results.join(",") + "]" : "[]"
                                } else {
                                    forEach(properties || value, function (property) {
                                        var element = serialize(property, value, callback, properties, whitespace, indentation, stack);
                                        if (element !== undef) {
                                            results.push(quote(property) + ":" + (whitespace ? " " : "") + element)
                                        }
                                    });
                                    result = results.length ? whitespace ? "{\n" + indentation + results.join(",\n" + indentation) + "\n" + prefix + "}" : "{" + results.join(",") + "}" : "{}"
                                }
                                stack.pop();
                                return result
                            }
                        };
                        JSON3.stringify = function (source, filter, width) {
                            var whitespace, callback, properties, className;
                            if (typeof filter == "function" || typeof filter == "object" && filter) {
                                if ((className = getClass.call(filter)) == functionClass) {
                                    callback = filter
                                } else if (className == arrayClass) {
                                    properties = {};
                                    for (var index = 0, length = filter.length, value; index < length; value = filter[index++], (className = getClass.call(value), className == stringClass || className == numberClass) && (properties[value] = 1)) ;
                                }
                            }
                            if (width) {
                                if ((className = getClass.call(width)) == numberClass) {
                                    if ((width -= width % 1) > 0) {
                                        for (whitespace = "", width > 10 && (width = 10); whitespace.length < width; whitespace += " ") ;
                                    }
                                } else if (className == stringClass) {
                                    whitespace = width.length <= 10 ? width : width.slice(0, 10)
                                }
                            }
                            return serialize("", (value = {}, value[""] = source, value), callback, properties, whitespace, "", [])
                        }
                    }
                    if (!has("json-parse")) {
                        var fromCharCode = String.fromCharCode;
                        var Unescapes = {
                            92: "\\",
                            34: '"',
                            47: "/",
                            98: "\b",
                            116: "	",
                            110: "\n",
                            102: "\f",
                            114: "\r"
                        };
                        var Index, Source;
                        var abort = function () {
                            Index = Source = null;
                            throw SyntaxError()
                        };
                        var lex = function () {
                            var source = Source, length = source.length, value, begin, position, isSigned, charCode;
                            while (Index < length) {
                                charCode = source.charCodeAt(Index);
                                switch (charCode) {
                                    case 9:
                                    case 10:
                                    case 13:
                                    case 32:
                                        Index++;
                                        break;
                                    case 123:
                                    case 125:
                                    case 91:
                                    case 93:
                                    case 58:
                                    case 44:
                                        value = charIndexBuggy ? source.charAt(Index) : source[Index];
                                        Index++;
                                        return value;
                                    case 34:
                                        for (value = "@", Index++; Index < length;) {
                                            charCode = source.charCodeAt(Index);
                                            if (charCode < 32) {
                                                abort()
                                            } else if (charCode == 92) {
                                                charCode = source.charCodeAt(++Index);
                                                switch (charCode) {
                                                    case 92:
                                                    case 34:
                                                    case 47:
                                                    case 98:
                                                    case 116:
                                                    case 110:
                                                    case 102:
                                                    case 114:
                                                        value += Unescapes[charCode];
                                                        Index++;
                                                        break;
                                                    case 117:
                                                        begin = ++Index;
                                                        for (position = Index + 4; Index < position; Index++) {
                                                            charCode = source.charCodeAt(Index);
                                                            if (!(charCode >= 48 && charCode <= 57 || charCode >= 97 && charCode <= 102 || charCode >= 65 && charCode <= 70)) {
                                                                abort()
                                                            }
                                                        }
                                                        value += fromCharCode("0x" + source.slice(begin, Index));
                                                        break;
                                                    default:
                                                        abort()
                                                }
                                            } else {
                                                if (charCode == 34) {
                                                    break
                                                }
                                                charCode = source.charCodeAt(Index);
                                                begin = Index;
                                                while (charCode >= 32 && charCode != 92 && charCode != 34) {
                                                    charCode = source.charCodeAt(++Index)
                                                }
                                                value += source.slice(begin, Index)
                                            }
                                        }
                                        if (source.charCodeAt(Index) == 34) {
                                            Index++;
                                            return value
                                        }
                                        abort();
                                    default:
                                        begin = Index;
                                        if (charCode == 45) {
                                            isSigned = true;
                                            charCode = source.charCodeAt(++Index)
                                        }
                                        if (charCode >= 48 && charCode <= 57) {
                                            if (charCode == 48 && (charCode = source.charCodeAt(Index + 1), charCode >= 48 && charCode <= 57)) {
                                                abort()
                                            }
                                            isSigned = false;
                                            for (; Index < length && (charCode = source.charCodeAt(Index), charCode >= 48 && charCode <= 57); Index++) ;
                                            if (source.charCodeAt(Index) == 46) {
                                                position = ++Index;
                                                for (; position < length && (charCode = source.charCodeAt(position), charCode >= 48 && charCode <= 57); position++) ;
                                                if (position == Index) {
                                                    abort()
                                                }
                                                Index = position
                                            }
                                            charCode = source.charCodeAt(Index);
                                            if (charCode == 101 || charCode == 69) {
                                                charCode = source.charCodeAt(++Index);
                                                if (charCode == 43 || charCode == 45) {
                                                    Index++
                                                }
                                                for (position = Index; position < length && (charCode = source.charCodeAt(position), charCode >= 48 && charCode <= 57); position++) ;
                                                if (position == Index) {
                                                    abort()
                                                }
                                                Index = position
                                            }
                                            return +source.slice(begin, Index)
                                        }
                                        if (isSigned) {
                                            abort()
                                        }
                                        if (source.slice(Index, Index + 4) == "true") {
                                            Index += 4;
                                            return true
                                        } else if (source.slice(Index, Index + 5) == "false") {
                                            Index += 5;
                                            return false
                                        } else if (source.slice(Index, Index + 4) == "null") {
                                            Index += 4;
                                            return null
                                        }
                                        abort()
                                }
                            }
                            return "$"
                        };
                        var get = function (value) {
                            var results, hasMembers;
                            if (value == "$") {
                                abort()
                            }
                            if (typeof value == "string") {
                                if ((charIndexBuggy ? value.charAt(0) : value[0]) == "@") {
                                    return value.slice(1)
                                }
                                if (value == "[") {
                                    results = [];
                                    for (; ; hasMembers || (hasMembers = true)) {
                                        value = lex();
                                        if (value == "]") {
                                            break
                                        }
                                        if (hasMembers) {
                                            if (value == ",") {
                                                value = lex();
                                                if (value == "]") {
                                                    abort()
                                                }
                                            } else {
                                                abort()
                                            }
                                        }
                                        if (value == ",") {
                                            abort()
                                        }
                                        results.push(get(value))
                                    }
                                    return results
                                } else if (value == "{") {
                                    results = {};
                                    for (; ; hasMembers || (hasMembers = true)) {
                                        value = lex();
                                        if (value == "}") {
                                            break
                                        }
                                        if (hasMembers) {
                                            if (value == ",") {
                                                value = lex();
                                                if (value == "}") {
                                                    abort()
                                                }
                                            } else {
                                                abort()
                                            }
                                        }
                                        if (value == "," || typeof value != "string" || (charIndexBuggy ? value.charAt(0) : value[0]) != "@" || lex() != ":") {
                                            abort()
                                        }
                                        results[value.slice(1)] = get(lex())
                                    }
                                    return results
                                }
                                abort()
                            }
                            return value
                        };
                        var update = function (source, property, callback) {
                            var element = walk(source, property, callback);
                            if (element === undef) {
                                delete source[property]
                            } else {
                                source[property] = element
                            }
                        };
                        var walk = function (source, property, callback) {
                            var value = source[property], length;
                            if (typeof value == "object" && value) {
                                if (getClass.call(value) == arrayClass) {
                                    for (length = value.length; length--;) {
                                        update(value, length, callback)
                                    }
                                } else {
                                    forEach(value, function (property) {
                                        update(value, property, callback)
                                    })
                                }
                            }
                            return callback.call(source, property, value)
                        };
                        JSON3.parse = function (source, callback) {
                            var result, value;
                            Index = 0;
                            Source = "" + source;
                            result = get(lex());
                            if (lex() != "$") {
                                abort()
                            }
                            Index = Source = null;
                            return callback && getClass.call(callback) == functionClass ? walk((value = {}, value[""] = result, value), "", callback) : result
                        }
                    }
                }
                if (isLoader) {
                    define(function () {
                        return JSON3
                    })
                }
            })(this)
        }, {}],
        44: [function (_dereq_, module, exports) {
            module.exports = toArray;

            function toArray(list, index) {
                var array = [];
                index = index || 0;
                for (var i = index || 0; i < list.length; i++) {
                    array[i - index] = list[i]
                }
                return array
            }
        }, {}]
    }, {}, [1])(1)
});
/** Message format for recording events and for real-time service communication
 This message format primarily follows the xAPI format (https://github.com/adlnet/xAPI-Spec/blob/master/xAPI.md)
 but is much more relaxed in the requirements for parameters. It also includes elements
 of the FIPA messaging standard, most notably the Speech Act field (performative, http://www.fipa.org/specs/fipa00061/SC00061G.html)

 Package: SuperGLU (Generalized Learning Utilities)
 Author: Benjamin Nye
 License: APL 2.0
 Version: 1.0.0

 Requires:
 - zet.js
 - serialization.js
 **/
if (typeof SuperGLU === "undefined"){
    var SuperGLU = {};
    if (typeof window === "undefined") {
        var window = this;
    }
    window.SuperGLU = SuperGLU;
}

(function(namespace, undefined) {
    var VERSION = "1.0.0",
        SUPERGLU_VERSION = SuperGLU.version,
        Zet = SuperGLU.Zet,
        Serialization = SuperGLU.Serialization;

    var ACCEPT_PROPOSAL_ACT, AGREE_ACT, CANCEL_ACT, CALL_FOR_PROPOSAL_ACT,
        CONFIRM_ACT, DISCONFIRM_ACT, FAILURE_ACT, INFORM_ACT, INFORM_IF_ACT,
        INFORM_REF_ACT,  NOT_UNDERSTOOD_ACT, PROPAGATE_ACT, PROPOSE_ACT,
        PROXY_ACT, QUERY_IF_ACT, QUERY_REF_ACT, REFUSE_ACT, REJECT_PROPOSAL_ACT,
        REQUEST_ACT, REQUEST_WHEN_ACT, REQUEST_WHENEVER_ACT, SUBSCRIBE_ACT,

        ACTOR_KEY, VERB_KEY, OBJECT_KEY, RESULT_KEY,
        SPEECH_ACT_KEY, TIMESTAMP_KEY, CONTEXT_KEY,
        CONTEXT_CONVERSATION_ID_KEY, CONTEXT_REPLY_WITH_KEY,
        CONTEXT_IN_REPLY_TO_KEY, CONTEXT_REPLY_BY_KEY,
        AUTHORIZATION_KEY, SESSION_ID_KEY,
        CONTEXT_LANGUAGE_KEY, CONTEXT_ONTOLOGY_KEY,
        SUPERGLU_VERSION_KEY, MESSAGE_VERSION_KEY,
        SPEECH_ACT_SET, tokenizeObject, untokenizeObject;

// Core Speech Acts
    INFORM_ACT = "Inform";                       // Asserting something
    INFORM_REF_ACT = "Inform Ref";               // Assert the name of something
    NOT_UNDERSTOOD_ACT = "Not Understood";       // Informing that you didn't understand an act
    QUERY_REF_ACT = "Query Ref";                 // Asking the id of an object
    REQUEST_ACT = "Request";                     // Requesting action (now)
    REQUEST_WHEN_ACT = "Request When";           // Requesting action, conditional on X
    REQUEST_WHENEVER_ACT = "Request Whenever";   // Requesting action, whenever X

// Information Speech Acts
    CONFIRM_ACT = "Confirm";
    DISCONFIRM_ACT = "Disconfirm";
    INFORM_IF_ACT = "Inform If";
    QUERY_IF_ACT = "Query If";

// Proposal Speech Acts
    ACCEPT_PROPOSAL_ACT = "Accept Proposal";
    CALL_FOR_PROPOSAL_ACT = "Call for Proposal";
    PROPOSE_ACT = "Propose";
    REJECT_PROPOSAL_ACT = "Reject Proposal";

// Action Negotiation Status
    AGREE_ACT = "Agree";
    CANCEL_ACT = "Cancel";
    REFUSE_ACT = "Refuse";
    FAILURE_ACT = "Failure";

// Relay Actions
    PROPAGATE_ACT = "Propagate";
    PROXY_ACT = "Proxy";
    SUBSCRIBE_ACT = "Subscribe";

    SPEECH_ACT_SET = {ACCEPT_PROPOSAL_ACT : true, AGREE_ACT : true, CANCEL_ACT : true,
        CALL_FOR_PROPOSAL_ACT : true, CONFIRM_ACT : true, DISCONFIRM_ACT : true,
        FAILURE_ACT : true, INFORM_ACT : true, INFORM_IF_ACT : true,
        INFORM_REF_ACT : true,  NOT_UNDERSTOOD_ACT : true, PROPAGATE_ACT : true,
        PROPOSE_ACT : true, PROXY_ACT : true, QUERY_IF_ACT : true,
        QUERY_REF_ACT : true, REFUSE_ACT : true, REJECT_PROPOSAL_ACT : true,
        REQUEST_ACT : true, REQUEST_WHEN_ACT : true, REQUEST_WHENEVER_ACT : true,
        SUBSCRIBE_ACT : true};

    ACTOR_KEY = "actor";
    VERB_KEY = "verb";
    OBJECT_KEY = "object";
    RESULT_KEY = "result";
    SPEECH_ACT_KEY = "speechAct";
    TIMESTAMP_KEY = "timestamp";
    CONTEXT_KEY = "context";

    CONTEXT_CONVERSATION_ID_KEY = "conversation-id";
    CONTEXT_IN_REPLY_TO_KEY = "in-reply-to";
    CONTEXT_REPLY_WITH_KEY = "reply-with";
    CONTEXT_REPLY_BY_KEY = "reply-by";

    AUTHORIZATION_KEY = "authorization";
    SESSION_ID_KEY = "session-id";
    CONTEXT_LANGUAGE_KEY = 'language';
    CONTEXT_ONTOLOGY_KEY = 'ontology';

    SUPERGLU_VERSION_KEY = 'SuperGLU-version';
    MESSAGE_VERSION_KEY = 'message-version';

    tokenizeObject = Serialization.tokenizeObject;
    untokenizeObject = Serialization.untokenizeObject;

    /** Message format, for passing information between services
     This is serializable, and can be cast into JSON, along with
     any contained objects (including Messages) that are also serializable.
     **/
    Zet.declare('Message', {
        superclass : Serialization.Serializable,
        defineBody : function(self){
            // Private Properties

            // Public Properties

            /** Create a Message
             @param actor: The actor who did or would do the given action
             @param verb: Some action that was or would be done by the actor
             @param obj: An object or target for the action
             @param result: The outcome of the action
             @param speechAct: A performative, stating why this message was sent
             @param context: A context object for the message, with additional data
             @param timestamp: A timestamp for when the message was created
             @param anId: A unique Id.  If none given, one will be assigned.
             **/
            self.construct = function construct(actor, verb, obj, result, speechAct,
                                                context, timestamp, anId){
                self.inherited(construct, [anId]);
                if (typeof actor === "undefined") {actor = null;}
                if (typeof verb === "undefined") {verb = null;}
                if (typeof obj === "undefined") {obj = null;}
                if (typeof result === "undefined") {result = null;}
                if (typeof speechAct === "undefined") {speechAct = INFORM_ACT;}
                if (typeof context === "undefined") {context = {};}
                if (typeof timestamp === "undefined") {timestamp = null;}
                self._actor = actor;
                self._verb = verb;
                self._obj = obj;
                self._result = result;
                self._speechAct = speechAct;
                self._timestamp = timestamp;
                if (self._timestamp == null){
                    self.updateTimestamp();
                }
                // Fill in version keys
                if (!(MESSAGE_VERSION_KEY in context)){
                    context[MESSAGE_VERSION_KEY] = VERSION;
                }
                if (!(SUPERGLU_VERSION_KEY in context)){
                    context[SUPERGLU_VERSION_KEY] = SUPERGLU_VERSION;
                }
                self._context = context;
            };

            /** Get the actor for the message **/
            self.getActor = function getActor(){
                return self._actor;
            };
            /** Set the actor for the message **/
            self.setActor = function setActor(value){
                self._actor = value;
            };

            /** Get the verb for the message **/
            self.getVerb = function getVerb(){
                return self._verb;
            };
            /** Set the verb for the message **/
            self.setVerb = function setVerb(value){
                self._verb = value;
            };

            /** Get the object for the message **/
            self.getObject = function getObject(){
                return self._obj;
            };
            /** Set the object for the message **/
            self.setObject = function setObject(value){
                self._obj = value;
            };

            /** Get the result for the message **/
            self.getResult = function getResult(){
                return self._result;
            };
            /** Set the result for the message **/
            self.setResult = function setResult(value){
                self._result = value;
            };

            /** Get the speech act for the message **/
            self.getSpeechAct = function getSpeechAct(){
                return self._speechAct;
            };
            /** Set the speech act for the message **/
            self.setSpeechAct = function setSpeechAct(value){
                self._speechAct = value;
            };

            /** Get the timestamp for the message (as an ISO-format string)**/
            self.getTimestamp = function getTimestamp(){
                return self._timestamp;
            };
            /** Set the timestamp for the message (as an ISO-format string) **/
            self.setTimestamp = function setTimestamp(value){
                self._timestamp = value;
            };
            /** Update the timestamp to the current time **/
            self.updateTimestamp = function updateTimestamp(){
                self._timestamp = new Date().toISOString();
            };

            /** Check if the context field has a given key **/
            self.hasContextValue = function hasContextValue(key){
                return (key in self._context) === true;
            };

            /** Get all the keys for the context object **/
            self.getContextKeys = function getContextKeys(){
                var key, keys;
                keys = [];
                for (key in self._context){
                    keys.push(key);
                }
                return keys;
            };

            /** Get the context value with the given key. If missing, return the default. **/
            self.getContextValue = function getContextValue(key, aDefault){
                if (!(key in self._context)){
                    return aDefault;
                }
                return self._context[key];
            };

            /** Set a context value with the given key-value pair **/
            self.setContextValue = function setContextValue(key, value){
                self._context[key] = value;
            };

            /** Delete the given key from the context **/
            self.delContextValue = function delContextValue(key){
                delete self._context[key];
            };

            /** Save the message to a storage token **/
            self.saveToToken = function saveToToken(){
                var key, token, newContext, hadKey;
                token = self.inherited(saveToToken);
                if (self._actor != null){
                    token.setitem(ACTOR_KEY, tokenizeObject(self._actor));
                }
                if (self._verb != null){
                    token.setitem(VERB_KEY, tokenizeObject(self._verb));
                }
                if (self._obj != null){
                    token.setitem(OBJECT_KEY, tokenizeObject(self._obj));
                }
                if (self._result != null){
                    token.setitem(RESULT_KEY, tokenizeObject(self._result));
                }
                if (self._speechAct != null){
                    token.setitem(SPEECH_ACT_KEY, tokenizeObject(self._speechAct));
                }
                if (self._timestamp != null){
                    token.setitem(TIMESTAMP_KEY, tokenizeObject(self._timestamp));
                }
                hadKey = false;
                newContext = {};
                for (key in self._context){
                    hadKey = true;
                    newContext[tokenizeObject(key)] = tokenizeObject(self._context[key]);
                }
                if (hadKey){
                    token.setitem(CONTEXT_KEY, tokenizeObject(newContext));
                }
                return token;
            };

            /** Initialize the message from a storage token and some additional context (e.g., local objects) **/
            self.initializeFromToken = function initializeFromToken(token, context){
                self.inherited(initializeFromToken, [token, context]);
                self._actor = untokenizeObject(token.getitem(ACTOR_KEY, true, null), context);
                self._verb = untokenizeObject(token.getitem(VERB_KEY, true, null), context);
                self._obj = untokenizeObject(token.getitem(OBJECT_KEY, true, null), context);
                self._result = untokenizeObject(token.getitem(RESULT_KEY, true, null), context);
                self._speechAct = untokenizeObject(token.getitem(SPEECH_ACT_KEY, true, null), context);
                self._timestamp = untokenizeObject(token.getitem(TIMESTAMP_KEY, true, null), context);
                self._context = untokenizeObject(token.getitem(CONTEXT_KEY, true, {}), context);
            };
        }
    });

    namespace.version = VERSION;
    namespace.Message = Message;

    namespace.SPEECH_ACT_SET = SPEECH_ACT_SET;
    namespace.ACCEPT_PROPOSAL_ACT = ACCEPT_PROPOSAL_ACT;
    namespace.AGREE_ACT = AGREE_ACT;
    namespace.CANCEL_ACT = CANCEL_ACT;
    namespace.CALL_FOR_PROPOSAL_ACT = CALL_FOR_PROPOSAL_ACT;
    namespace.CONFIRM_ACT = CONFIRM_ACT;
    namespace.DISCONFIRM_ACT = DISCONFIRM_ACT;
    namespace.FAILURE_ACT = FAILURE_ACT;
    namespace.INFORM_ACT = INFORM_ACT;
    namespace.INFORM_IF_ACT = INFORM_IF_ACT;
    namespace.INFORM_REF_ACT = INFORM_REF_ACT;
    namespace.NOT_UNDERSTOOD_ACT = NOT_UNDERSTOOD_ACT;
    namespace.PROPAGATE_ACT = PROPAGATE_ACT;
    namespace.PROPOSE_ACT = PROPOSE_ACT;
    namespace.PROXY_ACT = PROXY_ACT;
    namespace.QUERY_IF_ACT = QUERY_IF_ACT;
    namespace.QUERY_REF_ACT = QUERY_REF_ACT;
    namespace.REFUSE_ACT = REFUSE_ACT;
    namespace.REJECT_PROPOSAL_ACT = REJECT_PROPOSAL_ACT;
    namespace.REQUEST_ACT = REQUEST_ACT;
    namespace.REQUEST_WHEN_ACT = REQUEST_WHEN_ACT;
    namespace.REQUEST_WHENEVER_ACT = REQUEST_WHENEVER_ACT;
    namespace.SUBSCRIBE_ACT = SUBSCRIBE_ACT;

    namespace.ACTOR_KEY = ACTOR_KEY;
    namespace.VERB_KEY = VERB_KEY;
    namespace.OBJECT_KEY = OBJECT_KEY;
    namespace.RESULT_KEY = RESULT_KEY;
    namespace.SPEECH_ACT_KEY = SPEECH_ACT_KEY;
    namespace.TIMESTAMP_KEY = TIMESTAMP_KEY;
    namespace.CONTEXT_KEY = CONTEXT_KEY;

    namespace.CONTEXT_CONVERSATION_ID_KEY = CONTEXT_CONVERSATION_ID_KEY;
    namespace.CONTEXT_IN_REPLY_TO_KEY = CONTEXT_IN_REPLY_TO_KEY;
    namespace.CONTEXT_REPLY_WITH_KEY = CONTEXT_REPLY_WITH_KEY;
    namespace.CONTEXT_REPLY_BY_KEY = CONTEXT_REPLY_BY_KEY;

    namespace.AUTHORIZATION_KEY = AUTHORIZATION_KEY;
    namespace.SESSION_ID_KEY = SESSION_ID_KEY;
    namespace.CONTEXT_LANGUAGE_KEY = CONTEXT_LANGUAGE_KEY;
    namespace.CONTEXT_ONTOLOGY_KEY = CONTEXT_ONTOLOGY_KEY;

    namespace.SUPERGLU_VERSION_KEY = SUPERGLU_VERSION_KEY;
    namespace.MESSAGE_VERSION_KEY = MESSAGE_VERSION_KEY;

    SuperGLU.Messaging = namespace;
})(window.Messaging = window.Messaging || {});
/** Messaging gateways and service base classes, which form
 a network of gateways for messages to propogate across.
 This module has two main types of classes:
 A. Gateways: These relay messages to their connected services (children)
 and also to other gateways that will also relay the message.
 Gateways exist to abstract away the network and iframe topology.
 Gateways send messages to their parent gateway and can also distribute
 messages downstream to child gateways and services.
 B. Services: Services that receive messages and may (or may not) respond.
 Services exist to process and transmit messages, while doing
 meaningful things to parts of systems that they control.
 Services only send and receive message with their parent gateway.

 As a general rule, every service should be able to act reasonably and
 sensibly, regardless of what messages it receives. In short, no service
 should hard fail. There may be conditions there the system as a whole may
 not be able to function, but all attempts should be made to soft-fail.

 Likewise, all services should be prepared to ignore any messages that it
 does not want to respond to, without any ill effects on the service (e.g.,
 silently ignore) or, alternatively, to send back a message indicating that
 the message was not understood. Typically, silently ignoring is usually best.

 Package: SuperGLU (Generalized Learning Utilities)
 Author: Benjamin Nye
 License: APL 2.0

 Requires:
 - Zet.js
 - Serializable.js
 - Messaging.js
 **/

if (typeof SuperGLU === "undefined") {
    var SuperGLU = {};
    if (typeof window === "undefined") {
        var window = this;
    }
    window.SuperGLU = SuperGLU;
}

(function (namespace, undefined) {
    var Zet = SuperGLU.Zet,
        Serialization = SuperGLU.Serialization,
        Messaging = SuperGLU.Messaging;

    var CATCH_BAD_MESSAGES = false,
        SESSION_ID_KEY = 'sessionId';

    /** The base class for a messaging node (either a Gateway or a Service) **/
    Zet.declare('BaseMessagingNode', {
        // Base class for messaging gateways
        superclass: Serialization.Serializable,
        defineBody: function (self) {
            // Public Properties

            /** Initialize a messaging node.  Should have a unique ID and (optionally)
             also have one or more gateways connected.
             @param id: A unique ID for the node. If none given, a random UUID will be used.
             @type id: str
             @param gateways: Gateway objects, which this node will register with.
             @type gateways: list of MessagingGateway object
             **/
            self.construct = function construct(id, nodes) {
                self.inherited(construct, [id]);
                if (nodes == null) {
                    nodes = [];
                }
                self._nodes = {};
                self._requests = {};
                self._uuid = UUID.genV4();
                self.addNodes(nodes);
            };

            /** Receive a message. When a message is received, two things should occur:
             1. Any service-specific processing
             2. A check for callbacks that should be triggered by receiving this message
             The callback check is done here, and can be used as inherited behavior.
             **/
            self.receiveMessage = function receiveMessage(msg) {
                // Processing to handle a received message
                //console.log(self._id + " received MSG: "+ self.messageToString(msg));
                self._triggerRequests(msg);
            };

            /** Send a message to connected nodes, which will dispatch it (if any gateways exist). **/
            self.sendMessage = function sendMessage(msg) {
                //console.log(self._id + " sent MSG: "+ self.messageToString(msg));
                self._distributeMessage(self._nodes, msg);
            };

            /** Handle an arriving message from some source.
             Services other than gateways should generally not need to change this.
             @param msg: The message arriving
             @param senderId: The id string for the sender of this message.
             **/
            self.handleMessage = function handleMessage(msg, senderId) {
                self.receiveMessage(msg);
            };

            /** Sends a message each of 'nodes', except excluded nodes (e.g., original sender) **/
            self._distributeMessage = function _distributeMessage(nodes, msg, excludeIds) {
                var nodeId, node, condition;
                if (excludeIds == null) {
                    excludeIds = [];
                }
                for (nodeId in nodes) {
                    condition = nodes[nodeId].condition;
                    node = nodes[nodeId].node;
                    if ((excludeIds.indexOf(nodeId) < 0) &&
                        (condition == null || condition(msg))) {
                        self._transmitMessage(node, msg, self.getId());
                    }
                }
            };

            /** Transmit the message to another node **/
            self._transmitMessage = function _transmitMessage(node, msg, senderId) {
                node.handleMessage(msg, senderId);
            };

            // Manage Connected Nodes

            /** Get all connected nodes for the gateway **/
            self.getNodes = function getNodes() {
                return Object.keys(self._nodes).map(function (key) {
                    return self._nodes[key].node;
                });
            };

            /** Connect nodes to this node **/
            self.addNodes = function addNodes(nodes) {
                var i;
                if (nodes == null) {
                    nodes = [];
                }
                for (i = 0; i < nodes.length; i++) {
                    nodes[i].onBindToNode(self);
                    self.onBindToNode(nodes[i]);
                }
            };

            /** Remove the given connected nodes. If nodes=null, remove all. **/
            self.removeNodes = function removeNodes(nodes) {
                var i;
                if (nodes == null) {
                    nodes = self.getNodes();
                }
                for (i = 0; i < nodes.length; i++) {
                    nodes[i].onUnbindToNode(self);
                    self.onUnbindToNode(nodes[i]);
                }
            };

            /** Register the node and signatures of messages that the node is interested in **/
            self.onBindToNode = function onBindToNode(node) {
                if (!(node.getId() in self._nodes)) {
                    self._nodes[node.getId()] = {
                        'node': node,
                        'conditions': node.getMessageConditions()
                    };
                }
            };

            /** This removes this node from a connected node (if any) **/
            self.onUnbindToNode = function onUnbindToNode(node) {
                if (node.getId() in self._nodes) {
                    delete self._nodes[node.getId()];
                }
            };

            /** Get a list of conditions functions that determine if a gateway should
             relay a message to this node (can be propagated across gateways to filter
             messages from reaching unnecessary parts of the gateway network).
             **/
            self.getMessageConditions = function getMessageConditions() {
                /** Function to check if this node is interested in this message type */
                return function () {
                    return true;
                };
            };

            /** Get the conditions for sending a message to a node **/
            self.getNodeMessageConditions = function getNodeMessageConditions(nodeId) {
                if (nodeId in self._nodes) {
                    return self._nodes[nodeId].conditions;
                } else {
                    return function () {
                        return true;
                    };
                }
            };

            /** Update the conditions for sending a message to a node **/
            self.updateNodeMessageConditions = function updateNodeMessageConditions(nodeId, conditions) {
                if (nodeId in self._nodes) {
                    self._nodes[nodeId] = [self._nodes[nodeId].node, conditions];
                }
            };

            // Request Management

            /** Internal function to get all pending request messages **/
            self._getRequests = function _getRequests() {
                var key, reqs;
                reqs = [];
                for (key in self._requests) {
                    reqs.push(self._requests[key][0]);
                }
                return reqs;
            };

            /** Add a request to the queue, to respond to at some point
             @param msg: The message that was sent that needs a reply.
             @param callback: A function to call when the message is received, as f(newMsg, requestMsg)
             @TODO: Add a timeout for requests, with a timeout callback (maxWait, timeoutCallback)
             **/
            self._addRequest = function _addRequest(msg, callback) {
                if (callback != null) {
                    self._requests[msg.getId()] = [msg.clone(), callback];
                }
            };

            /** Make a request, which is added to the queue and then sent off to connected services
             @param msg: The message that was sent that needs a reply.
             @param callback: A function to call when the message is received, as f(newMsg, requestMsg)
             **/
            self._makeRequest = function _makeRequest(msg, callback) {
                self._addRequest(msg, callback);
                self.sendMessage(msg);
                //console.log("SENT REQUEST:" + Serialization.makeSerialized(Serialization.tokenizeObject(msg)));
            };

            /** Trigger any requests that are waiting for a given message. A
             request is filled when the conversation ID on the message matches
             the one for the original request. When a request is filled, it is
             removed, unless the speech act was request whenever (e.g., always)
             @param msg: Received message to compare against requests.
             **/
            self._triggerRequests = function _triggerRequests(msg) {
                var key, convoId, oldMsg, callback;
                //console.log("Heard REPLY:" + Serialization.makeSerialized(Serialization.tokenizeObject(msg)));
                convoId = msg.getContextValue(Messaging.CONTEXT_CONVERSATION_ID_KEY, null);
                //console.log("CONVO ID: " + convoId);
                //console.log(self._requests);
                if (convoId != null) {
                    // @TODO: This is a dict, so can check directly?
                    for (key in self._requests) {
                        if (key === convoId) {
                            oldMsg = self._requests[key][0];
                            callback = self._requests[key][1];
                            callback(msg, oldMsg);
                            // Remove from the requests, unless asked for a permanent feed
                            if (oldMsg.getSpeechAct() !== Messaging.REQUEST_WHENEVER_ACT) {
                                delete self._requests[key];
                            }
                        }
                    }
                }
            };

            // Pack/Unpack Messages

            /** Convenience function to serialize a message **/
            self.messageToString = function messageToString(msg) {
                return Serialization.makeSerialized(Serialization.tokenizeObject(msg));
            };

            /** Convenience function to turn a serialized JSON message into a message
             If the message is invalid when unpacked, it is ignored.
             **/
            self.stringToMessage = function stringToMessage(msg) {
                if (CATCH_BAD_MESSAGES) {
                    try {
                        msg = Serialization.untokenizeObject(Serialization.makeNative(msg));
                    } catch (err) {
                        // console.log("ERROR: Could not process message data received.  Received:");
                        // console.log(msg);
                        msg = undefined;
                    }
                } else {
                    msg = Serialization.untokenizeObject(Serialization.makeNative(msg));
                }
                return msg;
            };
        }
    });

    /** A messaging gateway base class, for relaying messages **/
    Zet.declare('MessagingGateway', {
        // Base class for messaging gateways
        superclass: BaseMessagingNode,
        defineBody: function (self) {
            // Public Properties

            /** Initialize a Messaging Gateway.
             @param id: Unique ID for the gateway
             @param nodes: Connected nodes for this gateway
             @param scope: Extra context data to add to messages sent to this gateway, if those keys missing
             **/
            self.construct = function construct(id, nodes, scope) {
                // Should check for cycles at some point
                if (scope == null) {
                    scope = {};
                }
                self.inherited(construct, [id, nodes]);
                self._scope = scope;
            };

            // Handle Incoming Messages
            /** Receive a message from a connected node and propogate it. **/
            self.handleMessage = function handleMessage(msg, senderId) {
                self.receiveMessage(msg);
                self._distributeMessage(self._nodes, msg, [senderId]);
            };

            // Relay Messages

            /** Distribute the message, after adding some gateway context data. **/
            self._distributeMessage = function _distributeMessage(nodes, msg, excludeIds) {
                msg = self.addContextDataToMsg(msg);
                self.inherited(_distributeMessage, [nodes, msg, excludeIds]);
            };

            /** Add the additional context data in the Gateway scope, unless those
             keys already exist in the message's context object.
             **/
            self.addContextDataToMsg = function addContextDataToMsg(msg) {
                var key;
                for (key in self._scope) {
                    if (!(msg.hasContextValue(key))) {
                        msg.setContextValue(key, self._scope[key]);
                    }
                }
                return msg;
            };
        }
    });

    /** Messaging Gateway Node Stub for Cross-Domain Page Communication
     A stub gateway that is a placeholder for a PostMessage gateway in another frame.
     This should only be a child or parent of a PostMessageGateway, because other
     nodes will not know to send messages via HTML5 postMessage to the actual frame
     that this stub represents.
     **/
    Zet.declare('PostMessageGatewayStub', {
        //
        superclass: BaseMessagingNode,
        defineBody: function (self) {
            // Private Properties
            var ANY_ORIGIN = '*';

            // Public Properties

            /** Initialize a PostMessageGatewayStub
             @param id: Unique id for the gateway
             @param gateway: The parent gateway for this stub
             @param origin: The base URL expected for messages from this frame.
             @param element: The HTML element (e.g., frame/iframe) that the stub represents. By default parent window.
             **/
            self.construct = function construct(id, gateway, origin, element) {
                var nodes = null;
                if (gateway != null) {
                    nodes = [gateway];
                }
                self.inherited(construct, [id, nodes]);
                if (origin == null) {
                    origin = ANY_ORIGIN;
                }
                if (element == null) {
                    element = parent;
                }
                if (element === window) {
                    element = null;
                }
                self._origin = origin;
                self._element = element;
                self._queue = [];
            };

            /** Get the origin, which is the frame location that is expected **/
            self.getOrigin = function getOrigin() {
                return self._origin;
            };

            /** Get the HTML element where messages would be sent **/
            self.getElement = function getElement() {
                return self._element;
            };

            self.getQueue = function getQueue() {
                return self._queue;
            };
        }
    });


    /** Messaging Gateway for Cross-Domain Page Communication
     Note: This should not directly take other PostMessageGateways as nodes.
     PostMessageGatewayStub objects must be used instead. Only use ONE
     PostMessageGateway per frame.
     **/
    Zet.declare('PostMessageGateway', {
        superclass: MessagingGateway,
        defineBody: function (self) {
            // Private Properties
            var ANY_ORIGIN = '*';

            // Public Properties

            /** Initialize a PostMessageGateway
             @param id: The unique ID for this gateway.
             @param nodes: Child nodes for the gateway
             @param origin: The origin URL for the current window
             @param scope: Additional context parameters to add to messages sent by children.
             **/
            self.construct = function construct(id, nodes, origin, scope) {
                if (origin == null) {
                    origin = ANY_ORIGIN;
                }
                self._origin = origin;
                // Get these ready before adding nodes in base constructor
                self._postNodes = {};
                self._validOrigins = {};
                self._anyOriginValid = true;
                self._registrationInterval = 0;
                self._registry = {};
                // Construct
                self.inherited(construct, [id, nodes, scope]);
                self.validatePostingHierarchy();
                if (window) {
                    self.bindToWindow(window);
                }
                if (nodes && nodes.length) {
                    nodes.forEach(function (t) {
                        if (PostMessageGatewayStub.isInstance(t) && t.getElement() === window.parent) {
                            self.startRegistration(t);
                            t._isActive = false;        //stub is inactive unless registered
                        }
                    });
                }
            };

            self.startRegistration = function (node) {
                var senderId = self.getId();
                var msg = Message(senderId, 'REGISTER', null, true);
                var interval = setInterval(function () {
                    self._transmitPostMessage(node, msg, senderId);
                }, 2000);
                self._registrationInterval = interval
            };

            self.stopRegistration = function () {
                clearInterval(self._registrationInterval);
            };

            /** Get the origin for this window **/
            self.getOrigin = function getOrigin() {
                return self._origin;
            };

            /** Get a stub that is the equivalent to this gateway **/
            self.getStub = function getStub() {
                return PostMessageGatewayStub(self._id, self._gateway, self._origin);
            };

            /** Validates that no additional PostMessageGateway nodes are connected
             and in the same frame. Valid neighbors can have no PostMessageGateway nodes,
             and only the parent OR the children can be of the PostMessageGatewayStub class
             **/
            self.validatePostingHierarchy = function validatePostingHierarchy() {
                var key;
                for (key in self._nodes) {
                    if (PostMessageGateway.isInstance(self._nodes[key])) {
                        throw TypeError("Error: Cannot directly connect PostMessageGateways");
                    }
                }
                // @TODO: Check for cycles in the posting hierarchy
            };

            /** Register the node and signatures of messages that the node is interested in **/
            self.onBindToNode = function onBindToNode(node) {
                self.inherited(onBindToNode, [node]);
                self._onAttachNode(node);
            };

            /** This removes this node from a connected node (if any) **/
            self.onUnbindToNode = function onUnbindToNode(node) {
                self._onDetachNode(node);
                self.inherited(onUnbindToNode, [node]);
            };

            /** When attaching nodes, adds any origins of PostMessageGatewayStubs
             to an allowed list of valid origins for HTML5 postMessages.
             @param node: A child node to attach.
             @type node: BaseMessagingNode
             **/
            self._onAttachNode = function _onAttachNode(node) {
                // @TODO: Should check if already attached and raise error
                if (PostMessageGatewayStub.isInstance(node) &&
                    (!(node.getId() in self._postNodes))) {
                    if (self._validOrigins[node.getOrigin()] == null) {
                        self._validOrigins[node.getOrigin()] = 1;
                    } else {
                        self._validOrigins[node.getOrigin()] += 1;
                    }
                    if (node.getOrigin() === ANY_ORIGIN) {
                        self._anyOriginValid = true;
                    }
                    self._postNodes[node.getId()] = node;
                }
            };

            /** When detaching nodes, clears any origins of PostMessageGatewayStubs
             from an allowed list of valid origins for HTML5 postMessages.
             @param node: A child node to attach.
             @type node: BaseMessagingNode
             **/
            self._onDetachNode = function _onDetachNode(node) {
                if (PostMessageGatewayStub.isInstance(node) &&
                    (node.getId() in self._postNodes)) {
                    self._validOrigins[node.getOrigin()] += -1;
                    if (self._validOrigins[node.getOrigin()] === 0) {
                        delete self._validOrigins[node.getOrigin()];
                        if (!(ANY_ORIGIN in self._validOrigins)) {
                            self._anyOriginValid = false;
                        }
                    }
                    delete self._postNodes[node.getId()];
                }
            };

            /** Bind the HTML5 event listener for HTML5 postMessage **/
            self.bindToWindow = function bindToWindow(aWindow) {
                var eventMethod, eventer, messageEvent;
                eventMethod = aWindow.addEventListener ? "addEventListener" : "attachEvent";
                eventer = aWindow[eventMethod];
                messageEvent = eventMethod == "attachEvent" ? "onmessage" : "message";
                eventer(messageEvent, function (event) {
                    self._receivePostMessage(event);
                });
            };

            // Messaging

            /** Send a message to parent. Send as normal, but send using sendPostMessage
             if sending to a PostMessage stub.
             **/
            /** Transmit the message to another node **/
            self._transmitMessage = function _transmitMessage(node, msg, senderId) {
                if (PostMessageGatewayStub.isInstance(node)) {
                    if (node._isActive) {
                        self._processPostMessageQueue(node);
                        self._transmitPostMessage(node, msg, senderId);
                    } else {
                        node.getQueue().push({
                            msg: msg,
                            senderId: senderId
                        });
                    }
                } else {
                    node.handleMessage(msg, senderId);
                }
            };

            self._processPostMessageQueue = function (stub) {
                stub.getQueue().forEach(function (o) {
                    self._transmitPostMessage(stub, o.msg, o.senderId);
                });
                stub.getQueue().splice(0, stub.getQueue().length);
            };

            // HTML5 PostMessage Commands
            self._transmitPostMessage = function _transmitPostMessage(node, msg, senderId) {
                if (node._stubId) {
                    msg.setObject(msg.getObject() == null ? {} : msg.getObject());
                    msg.getObject()["stubId"] = node._stubId;
                }

                var postMsg, element;
                postMsg = JSON.stringify({
                    'SuperGLU': true,
                    'msgType': 'SuperGLU',
                    'version': SuperGLU.version,
                    'senderId': senderId,
                    'targetId': node.getId(),
                    'msg': self.messageToString(msg)
                });
                element = node.getElement();
                if (element != null) {
                    // console.log(JSON.parse(postMsg).senderId + " POSTED UP " + self.messageToString(msg));
                    element.postMessage(postMsg, node.getOrigin());
                }
            };

            self._receivePostMessage = function _receivePostMessage(event) {
                var senderId, message, targetId;
                //console.log(self._id + " RECEIVED POST " + JSON.parse(event.data));
                if (self.isValidOrigin(event.origin)) {
                    try {
                        message = JSON.parse(event.data);
                    } catch (err) {
                        // console.log("Post Message Gateway did not understand: " + event.data);
                        return;
                    }
                    senderId = message.senderId;
                    targetId = message.targetId;
                    message = self.stringToMessage(message.msg);
                    console.log(message);
                    if (Messaging.Message.isInstance(message) &
                        (targetId === self.getId()) &&
                        message.getVerb() === 'REGISTER'
                    ) {
                        var obj = message.getObject() || {};
                        var node = null;
                        var verb = 'REGISTERED';
                        var stubId = UUID.genV4().toString();
                        if (obj.stubId) {
                            stubId = obj.stubId;
                            node = self._registry[stubId];
                        } else {
                            node = SuperGLU.Messaging_Gateway.PostMessageGatewayStub(senderId, null, null, event.source);
                            self._registry[stubId] = node;
                            self.addNodes([node]);
                        }
                        var msg = Message(self.getId(), verb, {stubId: stubId}, true);
                        self._transmitPostMessage(node, msg, self.getId());
                    } else if (Messaging.Message.isInstance(message) &
                        (targetId === self.getId()) &&
                        message.getVerb() === 'REGISTERED'
                    ) {
                        var nodes = self.getNodes();
                        nodes.forEach(function (node) {
                            if (PostMessageGatewayStub.isInstance(node) && node.getElement() === window.parent) {
                                self.stopRegistration();
                                node._isActive = true;        //stub is inactive unless registered
                                self._stubId = message.getObject().stubId;
                                self._processPostMessageQueue(node);
                            }
                        });
                    }
                    else if (Messaging.Message.isInstance(message) &
                        (targetId === self.getId()) &&
                        (senderId in self._postNodes)) {
                        self.handleMessage(message, senderId);
                    }
                }
            };

            self.isValidOrigin = function isValidOrigin(url) {
                if (self._anyOriginValid) {
                    return true;
                } else {
                    return url in self._validOrigins;
                }
            };
        }
    });


    Zet.declare('HTTPMessagingGateway', {
        // Base class for messaging gateways
        // This uses socket.io.js and uuid.js
        superclass: MessagingGateway,
        defineBody: function (self) {
            // Public Properties
            // Events: connecting, connect, disconnect, connect_failed, error,
            //         message, anything, reconnecting, reconnect, reconnect_failed
            // Listed At: github.com/LearnBoost/socket.io/wiki/Exposed-events
            var MESSAGING_NAMESPACE = '/messaging',
                TRANSPORT_SET = ['websocket',
                    'flashsocket',
                    'htmlfile',
                    'xhr-polling',
                    'jsonp-polling'];
            // Set Socket.IO Allowed Transports


            self.construct = function construct(id, nodes, url, sessionId, scope) {
                self.inherited(construct, [id, nodes, scope]);      // Classifier not used here, as messages are exact responses.
                if (url == null) {
                    url = null;
                }
                if (sessionId == null) {
                    sessionId = UUID.genV4().toString();
                }
                self._url = url;
                self._socket = io.connect(self._url + MESSAGING_NAMESPACE);
                self._isConnected = false;
                self._sessionId = sessionId;
                self._socket.on('message', self.receiveWebsocketMessage);
            };

            self.bindToConnectEvent = function bindToConnectEvent(funct) {
                self._socket.on('connect', funct);
            };

            self.bindToCloseEvent = function bindToCloseEvent(funct) {
                self._socket.on('disconnect', funct);
            };

            self.addSessionData = function addSessionData(msg) {
                msg.setContextValue(SESSION_ID_KEY, self._sessionId);
                return msg;
            };

            /** Distribute the message, after adding some gateway context data. **/
            self._distributeMessage = function _distributeMessage(nodes, msg, excludeIds, noSocket) {
                msg = self.addContextDataToMsg(msg);
                if (noSocket !== true && self._url != null) {
                    msg = self.addSessionData(msg);
                    self.sendWebsocketMessage(msg);
                }
                self.inherited(_distributeMessage, [nodes, msg, excludeIds]);
            };

            self.sendWebsocketMessage = function sendWebsocketMessage(msg) {
                msg = self.messageToString(msg);
                self._socket.emit('message', {data: msg, sessionId: self._sessionId});
            };

            self.receiveWebsocketMessage = function receiveWebsocketMessage(msg) {
                var sessionId;
                sessionId = msg.sessionId;
                msg = msg.data;
                msg = self.stringToMessage(msg);
                // console.log("GOT THIS:" + sessionId);
                // console.log("Real Sess: " + self._sessionId);
                if (Messaging.Message.isInstance(msg) &&
                    (sessionId == null || sessionId == self._sessionId)) {
                    self._distributeMessage(self._nodes, msg, [], true);
                }
            };
        }
    });


    Zet.declare('BaseService', {
        // Base class for messaging gateways
        superclass: BaseMessagingNode,
        defineBody: function (self) {
            // Public Properties

            self.construct = function construct(id, gateway) {
                var nodes = null;
                if (gateway != null) {
                    nodes = [gateway];
                }
                self.inherited(construct, [id, nodes]);
            };

            /** Connect nodes to this node.
             Only one node (a gateway) should be connected to a service.
             **/
            self.addNodes = function addNodes(nodes) {
                if (nodes.length + self.getNodes().length <= 1) {
                    self.inherited(addNodes, [nodes]);
                } else {
                    console.log("Error: Attempted to add more than one node to a service. Service must only take a single gateway node. Service was: " + self.getId());
                }
            };

            /** Bind nodes to this node.
             Only one node (a gateway) should be connected to a service.
             **/
            self.onBindToNode = function onBindToNode(node) {
                if (self.getNodes().length === 0) {
                    self.inherited(onBindToNode, [node]);
                } else {
                    console.log("Error: Attempted to bind more than one node to a service. Service must only take a single gateway node.");
                }
            };
        }
    });

    Zet.declare('TestService', {
        // Base class for messaging gateways
        superclass: BaseService,
        defineBody: function (self) {
            // Public Properties
            self.receiveMessage = function receiveMessage(msg) {
                console.log("TEST SERVICE " + self.getId() + " GOT: \n" + self.messageToString(msg));
                self.inherited(receiveMessage, [msg]);
            };

            self.sendTestString = function sendTestString(aStr) {
                console.log("Test Service is Sending: " + aStr);
                self.sendMessage(Messaging.Message("TestService", "Sent Test", "To Server", aStr));
            };

            self.sendTestMessage = function sendTestMessage(actor, verb, object, result, speechAct, context, addGatewayContext) {
                var msg;
                if (context == null) {
                    context = {};
                }
                if (addGatewayContext == null) {
                    addGatewayContext = true;
                }
                msg = Messaging.Message(actor, verb, object, result, speechAct, context);
                console.log(msg);
                if ((self._gateway != null) && (addGatewayContext)) {
                    msg = self._gateway.addContextDataToMsg(msg);
                }
                self.sendMessage(msg);
            };

            self.sendTestRequest = function sendTestRequest(callback, actor, verb, object, result, speechAct, context, addGatewayContext) {
                var msg;
                if (context == null) {
                    context = {};
                }
                if (addGatewayContext == null) {
                    addGatewayContext = true;
                }
                msg = Messaging.Message(actor, verb, object, result, speechAct, context);
                console.log(msg);
                if ((self._gateway != null) && (addGatewayContext)) {
                    msg = self._gateway.addContextDataToMsg(msg);
                }
                self._makeRequest(msg, callback);
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

    SuperGLU.Messaging_Gateway = namespace;
})(window.Messaging_Gateway = window.Messaging_Gateway || {});

/** Services for determining if another service or gateway
 is functional (e.g., loaded properly, heartbeat functional)

 Package: SuperGLU (Generalized Learning Utilities)
 Author: Benjamin Nye
 License: APL 2.0

 Requires:
 - Util\zet.js
 - Util\serializable.js
 - Core\messaging.js
 - Core\messaging-gateway.js
 **/

if (typeof SuperGLU === "undefined"){
    var SuperGLU = {};
    if (typeof window === "undefined") {
        var window = this;
    }
    window.SuperGLU = SuperGLU;
}

(function(namespace, undefined) {
    var Zet = SuperGLU.Zet,
        Serialization = SuperGLU.Serialization,
        Messaging = SuperGLU.Messaging,
        Messaging_Gateway = SuperGLU.Messaging_Gateway;

// Verbs and Context Keys
    var HEARTBEAT_VERB = 'Heartbeat',
        ORIGIN_KEY = 'Origin';

    /** Heartbeat service, which generates a regular message that
     is sent at some interval.
     **/
    Zet.declare('HeartbeatService', {
        superclass : Messaging_Gateway.BaseService,
        defineBody : function(self){
            // Public Properties
            var DEFAULT_HB = 'DefaultHeartbeat',
                DEFAULT_DELAY = 60;

            /** Initialize the heartbeat service
             @param gateway: The parent gateway for this service
             @param heartbeatName: The name for the heartbeat
             @param delay: The interval for sending the heartbeat, in seconds.
             @param id: The UUID for this service
             **/
            self.construct = function construct(gateway, heartbeatName, delay, id){
                self.inherited(construct, [id, gateway]);
                if (heartbeatName == null) {heartbeatName = DEFAULT_HB;}
                if (delay == null) {delay = DEFAULT_DELAY;}
                self._heartbeatName = heartbeatName;
                self._delay = delay;
                self._isActive = false;
            };

            /** Send the heartbeat message **/
            self.sendHeartbeat = function sendHeartbeat(){
                var msg = Message(self.getId(), HEARTBEAT_VERB, self._heartbeatName,
                    window.location.href);
                msg.setContextValue(ORIGIN_KEY, window.location.href);
                self.sendMessage(msg);
            };

            /** Start this service heartbeat, with a given delay.
             If already started, does nothing.
             @param delay: The interval for the heartbeat. If none
             given, uses the service default.
             **/
            self.start = function start(delay){
                if (delay != null){
                    self._delay = delay;
                }
                var heartbeatFunct = function(){
                    if (self._isActive){
                        self.sendHeartbeat();
                        setTimeout(heartbeatFunct, self._delay*1000);
                    }
                };
                if (self._isActive !== true){
                    self._isActive = true;
                    heartbeatFunct();
                }
            };

            /** Change the rate of this heartbeat generated.
             @param delay: The interval for the heartbeat, in seconds.
             **/
            self.changeHeartrate = function changeHeartrate(delay){
                if (delay == null){ delay = DEFAULT_DELAY; }
                self._delay = delay;
            };

            /** Stop the heartbeat. **/
            self.stop = function stop(){
                self._isActive = false;
            };
        }
    });

    /** Heartbeat monitor service, which monitors one or more heartbeat messages.
     This service determines that a beat is skipped if ANY heartbeat is missed.
     Each heartbeat has a value that stores the last time that any message matched
     that monitor. This value is updated every time a message is received, with the
     time that the message was received.  If the monitor checks any monitor and its
     last message is too old, a function is called.
     **/
    Zet.declare('HeartbeatMonitor', {
        superclass : Messaging_Gateway.BaseService,
        defineBody : function(self){
            var DEFAULT_DELAY = 150;

            /** Initialize the heartbeat monitor service
             @param gateway: The parent gateway for this service
             @param heartbeatNames: The names of each heartbeat being monitored
             @param delay: The delay allowed for each heartbeat to arrive.
             @param onSkipbeat: Function called if a beat is skipped, in form f(heartbeatName, self)
             @param offOnSkip: If true, turns off if beat skipped.
             Else, calls onSkipbeat repeatedly.
             @param id: The uuid for this service.
             **/
            self.construct = function construct(gateway, heartbeatNames, delay,
                                                onSkipbeat, offOnSkip, id){
                self.inherited(construct, [id, gateway]);
                if (heartbeatNames == null) {heartbeatNames = [];}
                if (delay == null) {delay = DEFAULT_DELAY;}
                if (offOnSkip == null) {offOnSkip = false;}
                self._heartbeatNames = heartbeatNames;
                self._delay = delay;
                self._onSkipbeat = onSkipbeat;
                self._offOnSkip = offOnSkip;
                self._isActive = false;
                self._heartbeatTimes = {};
                self.resetHeartbeatTimes();
            };

            /** Receive messages. Only looks for messages with a heartbeat verb.
             If heartbeat message hits, this updates the time for that heartbeat
             (stated as the 'object' message component).
             **/
            self.receiveMessage = function receiveMessage(msg){
                self.inherited(receiveMessage, [msg]);
                if (msg.getVerb() === HEARTBEAT_VERB){
                    if (self._heartbeatNames.indexOf(msg.getObject()) >= 0){
                        self._heartbeatTimes[msg.getObject()] = new Date().getTime();
                    }
                }
            };

            /** Start the heartbeat monitor, which resets all heartbeat monitors
             and starts the cycle that checks for any expired heartbeats.
             @param delay: The delay between when to check heartbeat monitors, in seconds.
             **/
            self.start = function start(delay){
                if (delay != null){
                    self._delay = delay;
                }
                var monitorFunct = function(){
                    if (self._isActive){
                        self.checkMonitors();
                        setTimeout(monitorFunct, self._delay*1000);
                    }
                };
                self.resetHeartbeatTimes();
                if (self._isActive !== true){
                    self._isActive = true;
                    monitorFunct();
                }
            };

            /** Check all monitors to see if any have expired.
             If any have expired, run the onSkipbeat function.
             **/
            self.checkMonitors = function checkMonitors(){
                var key, time;
                var currentTime = new Date().getTime();
                for (key in self._heartbeatNames){
                    key = self._heartbeatNames[key];
                    time = self._heartbeatTimes[key];
                    if (currentTime - time > self._delay*1000){
                        if (self._onSkipbeat){
                            self._onSkipbeat(key, self);
                            if (self._offOnSkip){
                                self.stop();
                            }
                        }
                    }
                }
            };

            /** Reset the heartbeat monitor times, by setting them each to
             the current time, and clearing out any values not in the list
             of monitored heartbeat names.
             **/
            self.resetHeartbeatTimes = function resetHeartbeatTimes(){
                var key;
                self._heartbeatTimes = {};
                for (key in self._heartbeatNames){
                    key = self._heartbeatNames[key];
                    self._heartbeatTimes[key] = new Date().getTime();
                }
            };

            /** Stop monitoring the heartbeats. **/
            self.stop = function stop(){
                self._isActive = false;
            };
        }
    });

    namespace.HEARTBEAT_VERB = HEARTBEAT_VERB;
    namespace.HeartbeatService = HeartbeatService;
    namespace.HeartbeatMonitor = HeartbeatMonitor;

    SuperGLU.Heartbeat_Service = namespace;
})(window.Heartbeat_Service = window.Heartbeat_Service || {});
/** Data about this reference implementation **/
if (typeof window === "undefined") {
    var window = this;
}

(function(namespace, undefined) {

// Version Numbering
    namespace.REFERENCE_IMPLEMENTATION_VERSION_KEY = "reference-implementation-version";
    namespace.USER_AGENT_KEY = "UserAgent";
    namespace.version = "1.0.1";

})(window.ReferenceData = window.ReferenceData || {});