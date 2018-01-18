const path = require('path')
const webpack = require('webpack')


module.exports = env => {
    const buildCore = env && env.core || false
    console.log("Building Core : ",buildCore)
    return {
        context: path.resolve('src'),
        entry: {
            app: buildCore ? './superglu-core-main' : './superglu-standard-main'
        },
        output: {
            path: path.resolve('dist'),
            filename: buildCore ? 'superglu-core.js' : 'superglu-standard.js',
            publicPath: '/dist/'
        },
        // debug: true,
        devtool: 'source-map',
        module: {
            loaders: [
                {
                    loader: "babel-loader",

                    // Skip any files outside of your project's `src` directory
                    include: [
                        path.resolve(__dirname, "src"),
                    ],

                    exclude: [
                        path.resolve(__dirname, "node_modules"),
                    ],

                    // Only run `.js` and `.jsx` files through Babel
                    test: /\.jsx?$/
                },
            ]
        }
    }
}