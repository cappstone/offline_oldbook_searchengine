module.exports = {
    devServer: {
        proxy: 'http://localhost:8000/search?word=vue.js&mode=0'
    }
}