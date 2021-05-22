<template>
  <div>
    <Header/>
    <div class="header">
      <Search v-on:data-to-upper="dataEmit"></Search>
      <div class="warning" v-if="emittedbook!=''">
        <section style="color: #c64756">상황에 따라 재고 정보가 실시간으로 변동될 수 있습니다.</section>
        <section style="color: #477ec6">자세한 재고 정보는 각 항목을 눌러주세요.</section>
      </div>
    </div>
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

.header {
  position:sticky;
  top: 0;
  left: 0;
  right: 0;
  height: auto;
  background-color: #F6F6F6;
}


.warning {
  background-color: white;
  max-width: 70%;
  border: 3px solid #557174;
  border-radius: 12px;
  text-align: center;
  font-size: max(1.1vw,13px);
  font-weight: 800;
  margin-left: auto;
  margin-right: auto;
}

@media screen and (max-width: 768px) {
  body {
    margin: 0;
    padding: 0;
  }

  .warning{
    max-width: 100%;
    border: 1px solid #557174;
    border-radius: 0;
  }
}
</style>