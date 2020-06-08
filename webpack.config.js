const path = require('path');

module.exports ={
  entry: './js/main.js',
  output: {
    path: path.resolve(__dirname, 'distr'),
    filename: 'bundle.js'
  },
  module: {
    rules:[{
      test:/\.js$/,
      exclude: /node_modules/,
      use:{
        loader: 'babel-loader',
        options: {
          presets: ['react']
        }
      }
    }]
  }

}
