<template>
  <header v-on:click="refresh()">
    <h1>중고책 검색시스템</h1>
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
  text-align: center;
  margin: 30px;
  color:#557174;
  font-weight: 800;
  cursor: pointer;
}
</style>
