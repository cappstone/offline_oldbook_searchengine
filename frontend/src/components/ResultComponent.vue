<template>
  
  <div v-if="book[0]!=''">
    <div class="book-container">
      <div class="book-card" v-for="(book, bookey) in book[0].result" v-bind:key="bookey" v-bind:style="[book.mallCount==0?{'cursor':'default'}:{'cursor':'pointer'}, backShadow]" v-on:mouseover="changeHover(book)">
        <table class="book-aladin-info" v-on:click="moreView(book.mallCount, bookey)">
          <tr>
            <td rowspan="4" class="book-aladin-img">
              <img v-bind:src="book.imgUrl">
            </td>
          </tr>
          <tr>
            <td class="book-aladin-bookname">{{book.bookName}}</td>
          </tr>
          <tr>
            <td class="book-aladin-desc">{{book.description}}</td>
          </tr>
          <tr>
            <td class="book-aladin-store-is" v-if="book.mallCount!=0"><b>{{book.mallCount}}개의 지점에 책이 존재합니다.</b></td>
            <td class="book-aladin-store-none" v-else><b>현재 모든 지점에 책이 없습니다.</b></td>
          </tr>
        </table>

        <Modal v-if="showmodal==true && showindex==bookey" v-on:close="showmodal=false" v-bind:details="book.mall" v-bind:malltype="book[1]"></Modal>

      </div>

    </div>
    <!--
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
    -->
  </div>
</template>

<script>
import Modal from './common/ResultModal.vue'
export default {
    props:['book'],

    data: function() {
      return {
        showindex: '',
        showmodal: false,
        shadowColour: ''
      }
    },

    components:{
      Modal
    },

    methods:{
      moreView: function(count,index){
        if (count!=0) {
          this.showindex=index;
          this.showmodal=true;
        } 
      },
      changeHover: function(count){
        if (count.mallCount == 0){
          this.shadowColour='rgba(230,99,138,0.8)';
        }
        else{
          this.shadowColour='rgba(99,230,138,0.8)';
        }
      }
    },

    watch: {
      showModal: function() {
        if(this.showmodal==true){
          document.documentElement.style.overflow="hidden";
          return;
        }
        document.documentElement.style.overflow="auto";
      }
    },
    
    computed: {
      backShadow() {
        return {
          '--box-shadow': this.shadowColour
        }
      }
    }
}
</script>

<style scoped>

  .book-container {
    text-align: center;
  }
  
  .book-card {
    margin: 0.5vw;
    box-shadow: 0 8px 16px 0 rgba(0,0,0,0.3);
    border-radius: 12px;

    background-color: #ffffff;

    max-width: 35%;
    height: 200px;

    transition: all 0.3s ease;

    display: inline-block;
  }

  .book-card:hover {
    box-shadow: 0 8px 16px 0 var(--box-shadow);
  }

  .book-aladin-info {
    padding: 10px;
    width: 100%;

    table-layout: fixed;
  }

  .book-aladin-bookname {
    font-size: max(1.3vw,18px);
    font-weight: 600;
    
    text-align:left;
    vertical-align: top;

    word-break:keep-all;
  }

  .book-aladin-img {
    text-align: left;
    padding: 0px;
    width: 118px;
    height: 175px;

    border-collapse: collapse;
  }

  .book-aladin-img img {
    width: 100%;
    height: 100%;

    display:block;
  }

  .book-aladin-desc {
    font-size: max(0.9vw,10px);

    text-align: left;
    vertical-align: top;

    word-break:keep-all;
  }

  .book-aladin-store-is {
    text-align: left;
    font-size: max(1vw,14px);
  }
  .book-aladin-store-none {
    text-align: left;
    font-size: max(1vw,14px);
    color: #c64756;
  }

@media screen and (max-width:768px) {
  .book-card{
    max-width:95%;
    height: auto;
    border-radius:0;
    border: 1px solid #557174;
    box-shadow:none;
  }
  .book-card:hover{
    box-shadow:none;
  }

  .book-aladin-info{
    padding:0;
    margin:0;
  }

  .book-aladin-img{
    height: 100px;
    width: 67px;
  }

  .book-aladin-button{
    min-height:20px;
    border-radius:0;
  }
}
</style>