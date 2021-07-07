module.exports = {
  devServer: {
    proxy: {
      "^/api": {
        target: "http://localhost:8000/",
        pathRewrite: {
          // remove base path
          "^/api": "/"
        }
      }
    }
  },
  chainWebpack: config => {
    const svgRule = config.module.rule("svg");

    svgRule.uses.clear();

    svgRule.use("vue-svg-loader").loader("vue-svg-loader"); // or `vue-loader-v16` if you are using a preview support of Vue 3 in Vue CLI
  }
};
