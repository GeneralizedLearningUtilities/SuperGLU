var webpackConfig = require('./webpack.config.babel');
// webpackConfig.entry = {};

module.exports = function (config) {
    config.set({
        // browsers: ['IE_no_addons', 'Chrome'],
        browsers: ['Chrome', 'Firefox'],
        customLaunchers: {
            IE_no_addons: {
                base: 'IE',
                flags: ['-extoff']
            }
        },
        files: [
            'src/nn.js',
            'src/nn.test.js',
            'src/util/zet.js',
            'src/util/zet.test.js',
            'src/util/serialization.js',
            'src/util/serialization.test.js'
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
        logLevel: config.LOG_INFO,
        autoWatch: false,

        preprocessors: {
            'src/nn.js': ['webpack'],
            'src/nn.test.js': ['webpack'],
            'src/util/zet.js': ['webpack'],
            'src/util/zet.test.js': ['webpack'],
            'src/util/serialization.js': ['webpack'],
            'src/util/serialization.test.js': ['webpack']
        },

        webpack: webpackConfig,
        webpackMiddleware: {
            noInfo: true
        },
        singleRun: false,
        concurrency: Infinity,
    });
};