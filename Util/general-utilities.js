var checkIfFileExists = function checkIfFileExists(urlToFile){
	var xhr = new XMLHttpRequest();
	xhr.open('HEAD', urlToFile, false);
	xhr.send();
	
	if (xhr.status == "404") {
		return false;
	} else {
		return true;
	}
}

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