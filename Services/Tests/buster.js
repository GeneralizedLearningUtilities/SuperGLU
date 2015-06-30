if (typeof module !== "undefined" && typeof module.exports !== "undefined"){
    var config = module.exports;
    var packageDir = "AWS_Core_Services";
    var utilPackage = "Util";
    var skoPackage = "SKO_Architecture";

    config[packageDir + " Tests"] = {
        rootPath: "../../",
        environment: "browser", // or "node"
        sources: [
            utilPackage + "/emacs5-compatibility-patches.js",
            utilPackage + "/uuid.js",
            utilPackage + "/zet.js",
            utilPackage + "/serialization.js",
            skoPackage + "/messaging.js",
            skoPackage + "/messaging-gateway.js",
            packageDir + "/**/*.js"
        ],
        tests: [
            //packageDir + "/Tests/*_UnitTests.js"
            packageDir + "/Tests/**/*_UnitTests.js"
        ]
    };
}