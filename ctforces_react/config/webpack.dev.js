const merge = require('webpack-merge');
const path = require('path');
const common = require('./webpack.common.js');

module.exports = merge(common, {
    mode: 'development',
    devServer: {
        contentBase: path.resolve(__dirname, '../dist'),
        historyApiFallback: true,
        host: '127.0.0.1',
        port: 3000,
    },
});
