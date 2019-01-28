const withCSS = require('@zeit/next-css');

if (typeof require !== 'undefined') {
    require.extensions['.less'] = () => {};
    require.extensions['.css'] = file => {};
}

module.exports = withCSS({
    webpack(config, options) {
        config.module.rules.push({
            test: /\.(png|jpg|gif|svg|eot|ttf|woff|woff2)$/,
            use: {
                loader: 'url-loader',
                options: {
                    limit: 100000
                }
            }
        });

        return config;
    }
});
