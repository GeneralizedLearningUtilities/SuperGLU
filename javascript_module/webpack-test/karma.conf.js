var webpackConfig = require('./webpack.config.babel')()
webpackConfig.entry = function () {
    return {}
}

module.exports = function (config) {
    config.set({
        browsers: ['IE_no_addons', 'Chrome', 'Firefox'],
        // browsers: ['Chrome', 'Firefox'],
        customLaunchers: {
            IE_no_addons: {
                base: 'IE',
                flags: ['-extoff']
            }
        },
        files: [
            'src/util/zet.js'
            , 'src/util/zet.test.js'
            , 'src/util/serialization.js'
            , 'src/util/serialization.test.js'
            , 'src/services/storage/local-storage-service.js'
            , 'src/services/storage/local-storage-service.test.js'
        ],
        plugins: [
            'karma-chrome-launcher',
            'karma-firefox-launcher',
            'karma-ie-launcher',
            'karma-mocha',
            'karma-chai',
            'karma-webpack'
        ],
        frameworks: ['mocha', 'chai'],
        port: 9876,
        colors: false,
        logLevel: config.LOG_DEBUG,
        autoWatch: false,
        preprocessors: {
            'src/util/zet.js': ['webpack']
            , 'src/util/zet.test.js': ['webpack']
            , 'src/util/serialization.js': ['webpack']
            , 'src/util/serialization.test.js': ['webpack']
            , 'src/services/storage/local-storage-service.js': ['webpack']
            , 'src/services/storage/local-storage-service.test.js': ['webpack']
        },

        webpack: webpackConfig,
        webpackMiddleware: {
            noInfo: true
        },
        singleRun: false,        //change it to false, and it'll run in watch mode - running tests whenever changes are saved
        concurrency: Infinity,
    })
}