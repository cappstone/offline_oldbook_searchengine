<template>
  <header v-on:click="refresh()">
    <h1><img src="logo.jpg"></h1>
  </header>
</template>

<script>
export default {
  methods:{
    refresh: function(){
      location.reload();
    }
  }

}
</script>

<style scoped>
h1 {
  font-size: max(2vw, 36px);
  text-align: center;
  margin: 30px;
  color:#557174;
  font-weight: 800;
  cursor: pointer;
}
@media screen and (max-width: 768px) {
  h1 {
    font-family: 'Roboto';
    font-size: max(1.3vw, 24px);
    margin-top: 15px;
    margin-bottom: 15px;
  }
}
</style>
