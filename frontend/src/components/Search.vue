<template>
  <div>
    <section class="search">
      <input v-on:keyup="checkEntered" v-model="searchname" placeholder="책이름">
      <button v-on:click="getData"></button>
    </section>
    <div class="select">
      <input type="radio" id="aladin" value="0" v-model="searchstore"><label for="aladin">Aladin</label>
      <input type="radio" id="yes" value="1" v-model="searchstore"><label for="yes">Yes24</label>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data:function(){return {searchname:'',searchstore:'0',searchurl:'', search:''}},

  methods: {
    checkEntered: function() {
      if(window.event.keyCode == 13) {
        this.getData();
      }
    },
    getData: function() {
      var vue = this;
      //vue.searchurl='http://sc0nep.iptime.org:8000/search?word='+String(vue.searchname)+'&mode='+String(vue.searchstore)
      vue.searchurl='http://localhost:8000/search?word='+String(vue.searchname)+'&mode='+String(vue.searchstore) //서버 맛갔을때 디버그용
      axios.get(vue.searchurl)
        .then(function(response) { 
          //console.log(response.data);
          vue.display(response.data);
          vue.search=response.data;
          if (vue.search==''){console.log("찾는 데이타가 없습니다")}
          vue.$emit('dataemit',[vue.search,vue.searchstore]);
        })
        .catch(function(error) {
          console.log('error');
        });
    },
    display: function(data) {
      for(var key in data){
        console.log(data[key].bookname);
        for(var resultkey in data[key].result){
          console.log(data[key].result[resultkey].count_stock+"개의 책이"+data[key].result[resultkey].mall+"에 있습니다");
        }
      }
    }
  }
}
</script>

 <style scoped>
  .search{
    height: 50px;
    max-width: 60%;

    border: 3px solid #557174;
    border-radius: 6px;

    margin: 0 auto;
    position: relative;
    display:flex;

    background-color: white;
  }
  .search input{
    width: 90%;

    padding: 11px;

    text-align: left;
    font-size: 24px;

    border: 0px;
    outline: none;

    float: left;
  }
  .search button{
    height: 100%;
    width: 10%;
    float: right;

    border-top-left-radius: 6px;
    border-bottom-left-radius: 6px;
    border-top: 0px;
    border-right: 0px;
    border-bottom: 0px;
    outline:none;

    background: #8db596;

    cursor: pointer;
  }

  .search button:hover{
    background: #70af85;
  }
  .search button:active{
    border-left:3px solid #557174;
    border-top:1px solid #557174;
    border-right:1px solid #557174;
    border-bottom:1px solid #557174;

  }

  .select{
    margin-top: 10px;
    margin-left:auto;
    margin-right:auto;
    padding:2px;
    max-width: 15%;
    border-style: inset;
    box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
    background: #8db596;
    border-radius: 20px;
    color: white;

    font-size: 1vw;
    text-align:center;
  }

</style>