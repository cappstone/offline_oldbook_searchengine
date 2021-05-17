<template>
  <div class="search-wrapper">
    <div class="search-container">
      <div class="search">
        <input v-on:keyup="checkEntered" v-model="searchname" placeholder="책이름">
        <button v-on:click="getData"><i class="fas fa-search search-icon"></i></button>
      </div>
      <div class="select">
        <input type="radio" id="aladin" value="0" v-model="searchstore"><label for="aladin">Aladin</label>
        <input type="radio" id="yes" value="1" v-model="searchstore"><label for="yes">Yes24</label>
      </div>
    </div>
    <Spinner v-bind:isVisible="isLoading"></Spinner>
  </div>
</template>

<script>
  import axios from 'axios'
  import Spinner from './common/Spinner.vue'

  export default {
    components:{Spinner},

    data:function(){return {isLoading:false,axiosInterceptor:null,searchname:'',searchstore:'0',searchurl:'', search:''}},

    methods: {
      checkEntered: function() {
        if(window.event.keyCode == 13) {
          this.getData();
        }
      },
      getData: function() {
        const vue = this;
        vue.searchurl='https://bookapi.nendo.space/search?word='+String(vue.searchname)+'&mode='+String(vue.searchstore)
        //vue.searchurl='http://localhost:7000/search?word='+String(vue.searchname)+'&mode='+String(vue.searchstore) //서버 맛갔을때 디버그용
        if (vue.searchname!='') {
          axios.get(vue.searchurl).then(function(response) {
            //vue.display(response.data); //콘솔창 디버그용
            vue.search=response.data;
            if (vue.search.result==''){alert("찾는 데이타가 없습니다")}
            vue.$emit('data-to-upper',[vue.search,vue.searchstore]);
          }).catch(function(error) {
            console.log(error);
            alert(+(error=="TypeError: Cannot set property 'isLoading' of undefined")?'서버와의 연결이 끊어졌습니다':error);
            vue.isLoading=false; //스피너 끄기
          });
        }
        else { //검색어 안입력했을때
          alert('검색어를 입력하세요');
        }
      },
      //로딩 스크린 활성화-인터셉터
      enableInterceptor: function() {
        this.axiosInterceptor = axios.interceptors.request.use(config=>{
          this.isLoading=true;
          return config;
        }, (error)=>{
          this.isLoading=false;
          return Promise.reject(error);
        }),
        axios.interceptors.response.use(response=>{
          this.isLoading=false;
          return response;
        }, function(error){
          this.isLoading=false;
          return Promise.reject(error);
        });
      },
      //인터셉터 지워야할시
      disableInterceptor: function() {
        axios.interceptors.request.eject(this.axiosInterceptor);
      }
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
    },
    //콤포넌트 초기화시 자동 실행
    created() {
      this.enableInterceptor();
    }
  }
</script>

<style scoped>
  .search{
    height: 50px;
    max-width: 70%;

    border: 3px solid #557174;
    border-radius: 6px;

    margin: 0 auto;
    position: relative;
    display: flex;
    flex-direction: row;

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
    margin-left: auto;
    margin-right: auto;
    font-size: clamp(10px, 1.2vw, 30px);
  }

  .select{
    margin-top: 10px;
    margin-bottom: 10px;
    margin-left: auto;
    margin-right: auto;
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

  /* 모바일 환경 */
  @media screen and (max-width: 768px){

    .search{
      height: 30px;
      max-width: 100%;
      border: 0px;
      border-top: 1px solid #557174;
      border-bottom: 1px solid #557174;
      border-radius: 0;

      margin:0;
      padding:0;

      position:inherit;
    }

    .search input{
      font-size: 12px;
    }

    .search button{
      border: 0;
      border-left: 1px solid #557174;
      border-radius: 0;
    }

    .select{
      max-width: 100%;
      height: 20px;
      border:0;
      border-radius:0;
      border-bottom:1px solid #557174;
      margin:0;
    }
  }
</style>