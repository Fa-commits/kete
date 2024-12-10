export default (config, env, helpers) => {
      config.devServer = config.devServer || {};
      config.devServer.proxy = {
        '/api': {
          target: 'http://localhost:5000',
          changeOrigin: true,
        },
      };
  };