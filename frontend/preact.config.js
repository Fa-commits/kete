export default {
    webpack(config, env, helpers, options) {
      config.devServer = config.devServer || {};
      config.devServer.proxy = {
        '/api': {
          target: 'http://localhost:5000',
          changeOrigin: true,
        },
      };
    },
  };