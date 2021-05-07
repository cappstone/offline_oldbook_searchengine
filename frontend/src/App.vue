<template>
  <div>
    <Header/>
    <Search v-on:data-to-upper="dataEmit"></Search>
    <br><br><br>
    <Result v-bind:book="emittedbook"></Result>
  </div>
</template>

<script>
import Header from './components/TheHeader.vue'
import Search from './components/SearchComponent.vue'
import Result from './components/ResultComponent.vue'

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
@media screen and (max-width: 768px) {
  body {
    margin: 0;
    padding: 0;
  }
}
</style>