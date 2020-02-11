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
    pluginOptions: {
        webpackBundleAnalyzer: {
            openAnalyzer: false,
        },
    },
};
