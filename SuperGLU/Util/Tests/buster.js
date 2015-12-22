if (typeof module !== "undefined" && typeof module.exports !== "undefined"){
    var config = module.exports;
    var packageDir = "Util";

    config[packageDir + " Tests"] = {
        rootPath: "../../",
        environment: "browser", // or "node"
        sources: [
            packageDir + "/zet.js"
        ],
        tests: [
            packageDir + "/Tests/**/*_UnitTests.js"
        ]
    };
}