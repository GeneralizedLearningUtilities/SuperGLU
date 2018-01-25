const path = require('path')

module.exports = env =>{
    const buildCore = env && env.core || false
    console.log("Building core : ", buildCore)
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
                    include: [
                        path.resolve(__dirname, "src"),
                    ],
                    exclude: [
                        path.resolve(__dirname, "node_modules"),
                    ],
                    test: /\.jsx?$/
                },
            ]
        }
    }
}