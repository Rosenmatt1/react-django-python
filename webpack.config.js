var path = require('path');
var ExtractTextPlugin = require('extract-text-webpack-plugin');
var HtmlWebpackPlugin = require('html-webpack-plugin')

module.exports = {
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader"
                },
            },
            // { test: /\.jpg$/, loader: 'file-loader' },
            // { test: /\.png$/, loader: 'url-loader' },
            // { test: /\.(jpg|png)$/, 
            //     use: [
            //         {
            //             loaders: 'file-directory',
            //             options: {
            //                 name: '[name].[ext]',
                            
            //             }
            //         }
            //     ]
            // },
            // {
            //     test: /\.html$/i,
            //     loader: 'html-loader',
            //     options: {
            //         attributes: {
            //             list: [
            //                 {
            //                     tag: 'img',
            //                     attribute: 'src',
            //                     type: 'src',
            //                 }
            //             ]
            //         }
            //     }
            // }
        ]
    }
}