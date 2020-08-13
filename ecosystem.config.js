module.exports = {
  apps: [{
    name: 'otc',
    script: '/home/otc-admin/opendatacam/server.js',
    env: {
      "NODE_ENV": "production",
      "PORT": "8080"
    },
  }]
};
