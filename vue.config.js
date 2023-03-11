const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})

 module.exports = {
  devServer: {
    proxy: {
      "/api/v1": {
        target: "http://localhost:5000",
        ws: false,
        changeOrigin: true
      }
    }
  }
};