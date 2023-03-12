const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})
// vue.config.js
    
module.exports = {
  devServer: {
    proxy: {
      "/backend/api/v1": {
        target: "http://localhost:5000",
        ws: false,
        changeOrigin: true
      }
    }
  }
};