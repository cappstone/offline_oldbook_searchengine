<template>
  
  <div v-if="book[0]!=''">
    <div v-if="book[1]=='0'">

      <div class="book-card" v-for="(book, bookey) in book[0].result" v-bind:key="bookey">
        <table class="book-aladin-info">
          <tr>
            <td rowspan="3" class="book-aladin-img">
              <img v-bind:src="book.imgurl">
            </td>
            <td class="book-aladin-bookname">{{book.bookname}}</td>
            <td rowspan="3" class="book-aladin-button-container">
              <button class="book-aladin-button" v-if="book.stock!=''" v-on:click="moreView(bookey)">
                <label for="book-aladin-button"><b>자세히</b></label>
              </button>
              <div v-else></div>
            </td>
          </tr>
          <tr>
            <td class="book-aladin-desc">{{book.description}}</td>
          </tr>
          <tr>
            <td class="book-aladin-store" v-if="book.mallCount!=0"><b>{{book.mallCount}}개의 지점에 책이 존재합니다.</b></td>
            <td class="book-aladin-store" v-else><b>현재 모든 지점에 책이 없습니다.</b></td>
          </tr>
        </table>

        <Modal v-if="showModal==true && showIndex==bookey" v-on:close="showModal=false" v-bind:details="book.stock"></Modal>

      </div>

    </div>

    <div id="yes" v-else>
      <ul class="book-card" v-for="key in book[0]" v-bind:key="key" style="margin-bottom:1vw; padding:25px">
        <li style="list-style-type: none">
          <b style="font-size: 2vw">{{key.mall}}</b>
          <ul v-for="resultkey in key.result" v-bind:key="resultkey">
            <li v-if="resultkey!='검색 결과 없음'">
              <b style="font-size: 1.2vw">{{resultkey.bookname}}</b>
              <div>{{resultkey.description}}</div>
              <div>{{resultkey.location}}이 {{resultkey.price}} 가격으로 있습니다.</div>
              <br>
            </li>
            <li v-else>
              <div>현재 재고가 없습니다.</div>
            </li>
          </ul>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import Modal from './common/ResultModal.vue'
export default {
    props:['book'],

    data: function() {
      return {
        showIndex: '',
        showModal: false
      }
    },

    components:{
      Modal
    },

    methods:{
      moreView: function(index){
        this.showIndex=index;
        this.showModal=true;
      }
    },

    watch: {
      showModal: function() {
        if(this.showModal==true){
          document.documentElement.style.overflow="hidden";
          return;
        }
        document.documentElement.style.overflow="auto";
      }
    }
}
</script>

<style scoped>
  
  .book-card {
    margin: 0 auto;
    margin-bottom: 2vw;
    box-shadow: 0 8px 16px 0 rgba(0,0,0,0.3);
    border-radius: 12px;

    background-color: white;

    max-width: 60%;
    height: auto;

    transition: all 0.3s ease;
  }

  .book-card:hover {
    box-shadow: 0 8px 16px 0 rgba(99,230,138,0.6);
  }

  .book-aladin-info {
    padding: 10px;
    width: 100%;

    table-layout: fixed;
  }

  .book-aladin-bookname {
    font-size: max(2vw, 36px);
    font-weight: 600;
    
    text-align: left;
    vertical-align: top;

    height:2vw;
  }

  .book-aladin-img {
    width: 20%;
    text-align: center;
    padding: 0;
    border-collapse: collapse;
  }

  .book-aladin-img img {
    max-width:90%;
  }

  .book-aladin-desc {
    font-size: max(1vw,12px);

    text-align: left;
    vertical-align: top;
    padding: 0;
    margin: 0;

    height:1vw;
  }

  .book-aladin-store {
    font-size: max(1.2vw, 15px);
  }

  .book-aladin-button-container {
    text-align: right;
    width: 10%;
    background-color: #ccd1ff;
  }

  .book-aladin-button {
    width: 100%;
    
    border-style:none;

    cursor: pointer;

    background-color: #ccd1ff;
  }

  .book-aladin-button label{
    font-size: max(1.2vw, 15px);
    cursor: pointer;
  }

/*
  .book-aladin-result {
    padding: 0 15px 0 20px;
    max-height:100%;
    overflow:hidden;
    background-color: white;
    transition: max-height 0.5s ease-in-out; 
  }
  
  .book-aladin-place {
    font-size: 1.5vw;
    font-weight:600;
    border-bottom: 1px groove #557174;
  }

  .book-aladin-stock {
    padding: 5px;
    width:100%;
  }

  .book-aladin-price {
    text-align: right;
    font-size: 2vw;
    font-weight: 800;
  }
*/

@media screen and (max-width:768px) {
  .book-card{
    max-width:100%;
    border-radius:0;
    border-bottom:1px solid #557174;
    margin:0;
    box-shadow:none;
  }
  .book-card:first-child{
    border-top:1px solid #557174;
  }
  .book-card:hover{
    box-shadow:none;
  }

  .book-aladin-bookname{
    font-size: max(1vw, 18px);
  }

  .book-aladin-info{
    padding:0;
  }

  .book-aladin-img img{
    object-fit: fill;
    height:100px;
  }

  .book-aladin-button{
    min-height:20px;
    border-radius:0;
  }
}
</style>