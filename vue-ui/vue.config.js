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
  }
};
