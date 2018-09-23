const path = require('path');

const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const ExtractTextPlugin = require('extract-text-webpack-plugin');

const production = process.env.NODE_ENV === "production";

module.exports = {
    entry: [
        "babel-polyfill",
        './src/index.js'
    ],
    output: {
        path: path.join(__dirname, '/dist'),
        filename: 'index_bundle.js'
    },
    devtool: production ? false : 'source-map',
    module: {
        loaders: [
            {test: /\.js$/, exclude: /node_modules/, loader: 'babel-loader'},
            {
                test: /\.css$/,
                loader: production
                    ? ExtractTextPlugin.extract({
                        fallback: "style-loader",
                        use: "css-loader",
                        //allChunks: true
                    })
                    : 'style-loader!css-loader'
            },
            {
                test: /\.(eot|svg|ttf|woff|woff2)$/,
                loader: 'file-loader?name=public/fonts/[name].[ext]'
            },
            {test: /\.(jpe?g|gif|png|wav|mp3)$/, loader: "file-loader"}
        ]
    },
    plugins: [
        new HtmlWebpackPlugin({
            template: __dirname + '/src/index.html',
            filename: 'index.html',
            inject: 'body'
        }),
        // new HtmlWebpackPlugin({
        //     template: __dirname + '/src/appendices.html',
        //     filename: 'appendices.html',
        //     inject: 'body'
        // }),
        new CopyWebpackPlugin([
            {from: 'src/public', to: 'public/'}
        ]),
        new ExtractTextPlugin("styles.css")
    ]
};

// var debug = process.env.NODE_ENV !== "production";
// var webpack = require('webpack');
//
// module.exports = {
//   context: __dirname,
//   devtool: debug ? "inline-sourcemap" : null,
//   entry: "./js/main.js",
//   output: {
//     path: __dirname + "/dist",
//     filename: "scripts.min.js"
//   },
//   plugins: debug ? [] : [
//     new webpack.optimize.DedupePlugin(),
//     new webpack.optimize.OccurenceOrderPlugin(),
//     new webpack.optimize.UglifyJsPlugin({ mangle: false, sourcemap: false }),
//   ]
// };