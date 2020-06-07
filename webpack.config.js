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
            { test: /\.jpg$/, loader: 'file-loader' },
            { test: /\.png$/, loader: 'url-loader' },
            {
                test: /\.html$/i,
                loader: 'html-loader',
                options: {
                    attributes: {
                        list: [
                            {
                                tag: 'img',
                                attribute: 'src',
                                type: 'src',
                            }
                        ]
                    }
                }
            }
        ]
    }
}