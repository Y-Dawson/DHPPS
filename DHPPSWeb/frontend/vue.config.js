module.exports = {
    devServer: {
      // open: true, //是否自动弹出浏览器页面
      host: "127.0.0.1",
      port: '8080',
      https: false,
      hotOnly: false,
      proxy: {
        '/backend': {
          target: 'http://127.0.0.1:8000', //API服务器的地址
          ws: true,  //代理websockets
          changeOrigin: true, // 虚拟的站点需要更管origin
          cookiePathRewrite: {//重写cookie路径
            '/tb-customer-web_war': '/'
            }
        }
      },
    }
  };
  