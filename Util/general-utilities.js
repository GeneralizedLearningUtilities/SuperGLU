/** Various utilities useful for HTML pages
    Package: SuperGLU
    Authors: Benjamin Nye and Daqi Dong
    License: APL 2.0
    Requires:
        - jquery
        - purl.js
**/

/** Check if a file exists on the server (synchronously)
    @param urlToFile: The URL for the file
    @type urlToFile: str
    @return: True if file exists, else false.
    @rtype: bool
**/
var checkIfFileExists = function checkIfFileExists(urlToFile){
	var xhr = new XMLHttpRequest();
	xhr.open('HEAD', urlToFile, false);
	xhr.send();
	
	if (xhr.status == "404") {
		return false;
	} else {
		return true;
	}
};

/** Add a set of parameters to a URL (uses purl.js)
    @param url: The base URL to change parameters on. If null, uses the window.location
    @param sourceParams: The original URL parameters. If null, pulled from window.location
    @param updatedParams: The updated parameters (e.g., new values, additional values)
    @param invalidParams: Parameters to filter from the URL, if identified.
**/
var addURLParams = function addURLParams(url, sourceParams, updatedParams, invalidParams){
        var key, 
            outParams = {};
        if (url == null){ 
            url = window.location.protocol + '//' + window.location.host + window.location.pathname;
        }
        if (invalidParams == null){ invalidParams = []; }
        if (sourceParams == null){ sourceParams = purl().param(); }
        if (updatedParams == null){ updatedParams = {}; }
        for (key in sourceParams){ 
            if (invalidParams.indexOf(key) < 0){
                outParams[key] = sourceParams[key];
            }
        }
        for (key in updatedParams){ 
            if (invalidParams.indexOf(key) < 0){
                outParams[key] = updatedParams[key];
            }
        }
        return url + '?' + $.param(outParams);
};
window.addURLParams = addURLParams;