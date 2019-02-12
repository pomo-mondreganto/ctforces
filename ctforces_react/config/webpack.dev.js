const merge = require('webpack-merge');
const common = require('./webpack.common.js');
const path = require('path');

module.exports = merge(common, {
    mode: 'development',
    devServer: {
        contentBase: path.resolve(__dirname, '../dist'),
        historyApiFallback: true,
        host: '127.0.0.1',
        port: 3000
    }
});
