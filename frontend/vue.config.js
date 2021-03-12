/* eslint-disable */

module.exports = {
    devServer: {
        disableHostCheck: true,
        proxy: {
            '/api': {
                target: 'http://sc0nep.iptime.org:7000'
            }
        }
    }
};