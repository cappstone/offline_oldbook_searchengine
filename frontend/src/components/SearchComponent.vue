<template>
  <div class="search-wrapper">
    <div class="search-container">
      <div class="search">
        <input v-on:keyup="checkEntered" v-model="searchname" placeholder="책이름">
        <button v-on:click="getData"><i class="fas fa-search search-icon"></i></button>
      </div>
      <div class="select">
        <input type="radio" id="default" value="0" v-model="sortcriteria"><label for="default" title="검색어와 가장 관련이 깊은 책부터 보여줍니다.">정확도순</label>
        <input type="radio" id="aladin" value="1" v-model="sortcriteria"><label for="aladin" title="123->abc->가나다 순으로 보여줍니다.">제목순</label>
        <input type="radio" id="yes" value="2" v-model="sortcriteria"><label for="yes" title="가장 많은 점포에 분포한 책부터 보여줍니다.">점포개수순</label>
      </div>
    </div>
    <Spinner v-bind:isVisible="isLoading" v-bind:message="message"></Spinner>
  </div>
</template>

<script>
  import axios from 'axios'
  import Spinner from './common/Spinner.vue'

  export default {
    components:{Spinner},

    data:function(){ return {
      isLoading:false,
      axiosInterceptor:null,
      searchname:'',
      sortcriteria:'0',
      searchurl:'', search:'', search2:'',
      message:''
      }
    },

    methods: {
      checkEntered: function() {
        if(window.event.keyCode == 13) {
          this.getData();
        }
      },
      getData: function() {
        const vue = this;
        vue.searchurl='http://bookapi.nendo.space/search?word='+String(vue.searchname)
        //vue.searchurl='http://172.30.1.7:23700/search?word='+String(vue.searchname); //공유기 서버
        //vue.searchurl='http://localhost:7000/search?word='+String(vue.searchname) //서버 맛갔을때 디버그용
        if (vue.searchname!='') {
          //크롤링
          //axios.all([axios(vue.searchurl+'&mode=0'),axios(vue.searchurl+'&mode=1')]).then(axios.spread(function(response,response2){
          vue.message="YES24 불러오는 중입니다..."
          axios.get(vue.searchurl+"&mode=1",{timeout:60000}).then(function(response2){
            vue.message="알라딘 불러오는 중입니다..."
            axios.get(vue.searchurl+"&mode=0",{timeout:60000}).then(function(response){
              vue.search=response.data;
              vue.search2=response2.data;
              //console.log(vue.search,vue.search2);

              //알라딘 예스24 합치는 함수
              if (vue.search.error){
                vue.search=vue.search2;
              }
              else{
                vue.search.searchTotal+=vue.search2.searchTotal;
                var i,j,k;
                for (i=0;i<vue.search.result.length;i++){
                  for (j=0;j<vue.search2.result.length;j++){
                    if (vue.search.result[i].bookName==vue.search2.result[j].bookName){
                      vue.search.result[i].mallCount+=vue.search2.result[j].mallCount;
                      for (k=0;k<vue.search2.result[j].mall.length;k++){
                        vue.search.result[i].mall.push(vue.search2.result[j].mall[k]);
                      }
                      vue.search2.result.splice(j,j);
                      vue.search.searchTotal-=1;
                      vue.search2.searchTotal-=1;
                    }
                  }
                }
                for (i=0;i<vue.search2.result.length;i++){
                  vue.search.result.push(vue.search2.result[i]);
                }
              }

              //기준에 맞춰 정렬하기
              vue.search.result.sort(function(a,b){
                if(vue.sortcriteria=='0'){
                  null;
                }
                else if (vue.sortcriteria=='1'){
                  if (a.bookName<b.bookName) return -1;
                  if (a.bookName>b.bookName) return 1;
                  if (a.bookName===b.bookName) return 0;
                }
                else if (vue.sortcriteria=='2'){
                  if (a.mallCount<b.mallCount) return 1;
                  if (a.mallCount>b.mallCount) return -1;
                  if (a.mallCount===b.mallCount) return 0;
                }
              });

              // id,mall_id 초기화
              for (i=0;i<vue.search.result.length;i++){
                vue.search.result[i].id=i;
                for (j=0;j<vue.search.result[i].mall.length;j++){
                  vue.search.result[i].mall[j].mall_id=j;
                }
              }

              if (vue.search.result=='' || vue.search.error){alert("찾는 데이타가 없습니다")}
              vue.$emit('data-to-upper',vue.search);
              vue.searchurl='',vue.search='',vue.search2=''; //초기화
            }).catch(function(error){
              alert('서버와 연결 할 수 없습니다.\n오류명:'+error);
            });
          }).catch(function(error) {
            //console.log(error);
            alert('서버와 연결 할 수 없습니다.\n오류명: '+error);
            vue.isLoading=false; //스피너 끄기;
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
        })
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
    max-width: 25%;
    border-style: inset;
    box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
    background: #8db596;
    border-radius: 20px;
    color: #ffffff;

    font-size: max(10px,1vw);
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