<template>
  
  <div v-if="book[0]!=''">
    <div v-if="book[1]=='0'">

      <div class="book-card" v-for="(book,bookey) in book[0]" v-bind:key="bookey">
        <table class="book-aladin-info">
          <tr>
            <td rowspan="4" class="book-aladin-img">
              <img v-bind:src="book.imgurl">
            </td>
            <td class="book_aladin_bookname">{{book.bookname}}</td>
          </tr>
          <tr>
            <td class="book-aladin-desc">{{book.description}}</td>
          </tr>
          <tr>
            <td class="book-aladin-store"><b>{{book.mall}}</b></td>
          </tr>
          <tr>
            <td class="temp">
              <button class="book-aladin-button" v-if="book.stock!=''" v-on:click="moreView(bookey)">
                <label for="book-aladin-button"><b>자세히</b></label>
              </button>
              <div v-else style="text-align:left; color:red"><b>재고 없음</b></div>
            </td>
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

    background-color: white;

    max-width: 70%;
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

  .book_aladin_bookname {
    font-size: 2vw;
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
    width:90%;
  }

  .book-aladin-desc {
    text-align: left;
    vertical-align: top;
    padding: 0;
    margin: 0;

    height:1vw;
  }

  .book-aladin-store {
    vertical-align: bottom;
  }

  .book-aladin-button {
    width: 100%;
    height: 100%;
    border-style: groove;
    border-color: #557174;
    background-color: white;
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
</style>