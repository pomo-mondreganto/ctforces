module.exports = {
    css: {
        loaderOptions: {
            sass: {
                prependData: `
            @use "sass:math";
            @import "@/styles/global/_variables.scss";
          `,
            },
        },
    },

    configureWebpack: {
        optimization: {
            splitChunks: {
                chunks: 'all',
            },
        },
    },

    devServer: {
        disableHostCheck: true,

        watchOptions: {
            ignored: /node_modules/,
            poll: 1000,
        },
    },
};
