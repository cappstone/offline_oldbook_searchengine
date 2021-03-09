<template>
  <div>
    <Header/>
    <Search v-on:dataemit="dataEmit"></Search>
    <br><br><br>
    <Result v-bind:book="emittedbook"></Result>
  </div>
</template>

<script>
import Header from './components/Header.vue'
import Search from './components/Search.vue'
import Result from './components/Result.vue'

export default {
  data: function() {
    return {
      emittedbook:'',
    }
  },

  components: {
    Header,
    Search,
    Result
  },

  methods: {
    dataEmit: function(value) {
      this.emittedbook=value;
      //console.log(this.emittedbook);
    }
  }
}
</script>

<style>
body {
  background-color: #F6F6F6;
}
</style>