<template>
  <div>
    <section class="search">
      <input v-on:keyup="checkEntered" v-model="searchname" placeholder="책이름">
      <button v-on:click="getData"><i class="fas fa-search fa-2x search-icon"></i></button>
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
        vue.searchurl='http://sc0nep.iptime.org:7000/search?word='+String(vue.searchname)+'&mode='+String(vue.searchstore)
        //vue.searchurl='http://localhost:7000/search?word='+String(vue.searchname)+'&mode='+String(vue.searchstore) //서버 맛갔을때 디버그용
        if (vue.searchname!='') {
          axios.get(vue.searchurl)
            .then(function(response) { 
              //vue.display(response.data); //콘솔창 디버그용
              vue.search=response.data;
              if (vue.search==''){console.log("찾는 데이타가 없습니다")}
              vue.$emit('data-to-upper',[vue.search,vue.searchstore]);
            })
            .catch(function(error) {
              console.log('error');
            });
        }
        else { //검색어 안입력했을때
          alert('검색어를 입력하세요');
        }
      },
      //콘솔창 디버그함수
      /*display: function(data) {
        for(var key in data){
          console.log(data[key].bookname);
          for(var resultkey in data[key].result){
            console.log(data[key].result[resultkey].count_stock+"개의 책이"+data[key].result[resultkey].mall+"에 있습니다");
          }
        }
      },
      */
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
    display: flex;

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
    border-top: 0px;
    border-left: 3px solid #557174;
    border-right: 0px;
    border-bottom: 0px;
    border-top-left-radius: 6px;
    border-bottom-left-radius: 6px;
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

  .search-icon{
    color: #ffffff;
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
    color: #ffffff;

    font-size: 1vw;
    text-align:center;
  }

</style>