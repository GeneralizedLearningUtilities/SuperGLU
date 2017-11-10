var webpackConfig = require('./webpack.config.babel');
// webpackConfig.entry = {};

module.exports = function (config) {
    config.set({
        browsers: ['IE_no_addons', 'Chrome'],
        // browsers: ['Chrome'],
        customLaunchers: {
            IE_no_addons: {
                base: 'IE',
                flags: ['-extoff']
            }
        },
        files: [
            'nn.js',
            'nn.test.js'
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
            'nn.js': ['webpack'],
            'nn.test.js': ['webpack'],
        },

        webpack: webpackConfig,
        webpackMiddleware: {
            noInfo: true
        },
        singleRun: true,
        concurrency: Infinity,
    });
};