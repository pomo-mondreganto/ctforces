module.exports = {
    css: {
        loaderOptions: {
            sass: {
                prependData: `
            @import "@/styles/global/_variables.scss";
          `,
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
