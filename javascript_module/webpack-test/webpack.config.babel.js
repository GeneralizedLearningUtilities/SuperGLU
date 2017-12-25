const path = require('path')
const webpack = require('webpack')

module.exports = {
    context: path.resolve('src'),
    entry: {
        app: './super-glu'
    },
    output: {
        path: path.resolve('dist'),
        filename: 'superglu-all.js',
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