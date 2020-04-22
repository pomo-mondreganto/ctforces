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
    },
};
