/* eslint-disable */

module.exports = {
    configureWebpack: {
        devServer: {
            disableHostCheck: true,
            proxy: {
                '/api': {
                    target: 'http://sc0nep.iptime.org:7000'
                }
            }
        }
    }
};