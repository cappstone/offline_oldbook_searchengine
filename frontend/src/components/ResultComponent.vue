<template>
  
  <div v-if="book!=''">
    <div class="book-container">
      <div class="book-card" v-for="(result, resultkey) in book.result" v-bind:key="resultkey" v-bind:style="[((result.mallCount==0) || (result.mallCount==1 && result.mall[0].price=='None'))?{'cursor':'default'}:{'cursor':'pointer'}, backShadow]" v-on:mouseover="changeHover(result)">
        <table class="book-aladin-info" v-on:click="moreView(result, resultkey)">
          <tr>
            <td rowspan="4" class="book-aladin-img">
              <img v-bind:src="result.imgUrl">
            </td>
          </tr>
          <tr>
            <td class="book-aladin-bookname">{{result.bookName}}</td>
          </tr>
          <tr>
            <td class="book-aladin-desc">{{result.description}}</td>
          </tr>
          <tr>
            <td class="book-aladin-store-none" v-if='result.mallCount==0 || (result.mallCount==1 && result.mall[0].price=="None")'><b>현재 모든 지점에 책이 없습니다.</b></td>
            <td class="book-aladin-store-is" v-else><b>{{result.mallCount}}개의 지점에 책이 존재합니다. 평균가: {{pricemean[result.id]}}원</b></td>
          </tr>
        </table>

        <Modal v-if="showmodal==true && showindex==resultkey" v-on:close="showmodal=false" v-bind:details="result"></Modal>

      </div>

    </div>
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
        shadowColour: '',
        pricemean: []
      }
    },

    components:{
      Modal
    },

    methods:{
      moreView: function(mall,index){
        if (mall.mallCount!=0 && !(mall.mallCount==1 && mall.mall[0].price=="None")) {
          this.showindex=index;
          this.showmodal=true;
        }
      },
      changeHover: function(count){
        if (count.mallCount == 0 || (count.mallCount == 1 && count.mall[0].price=="None")){
          this.shadowColour='rgba(230,99,138,0.8)';
        }
        else{
          this.shadowColour='rgba(99,230,138,0.8)';
        }
      }
    },

    watch: {
      showmodal: function() {
        if(this.showmodal==true){
          document.documentElement.style.overflow="hidden";
          return;
        }
        document.documentElement.style.overflow="auto";
      },
      
      book: function() {
        this.pricemean=[];
        for (var i in this.book.result){
          var sum=0;
          var count=0;

          for (var j in this.book.result[i].mall){
            if (this.book.result[i].mall[j].stock){
              for (var k in this.book.result[i].mall[j].stock){
                if (this.book.result[i].mall[j].stock[k]){
                  sum+=parseInt((this.book.result[i].mall[j].stock[k].price).replace(",",""));
                  count+=1;
                }
              }
            }
            else{
              if (this.book.result[i].mall[j].price){
                sum+=parseInt((this.book.result[i].mall[j].price).replace(",",""));
                count+=1;
              }
            }
          }
          this.pricemean.push(parseInt(sum/count));
        }
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
    min-height: 200px;

    transition: all 0.3s ease;

    display: inline-block;
  }

  .book-card:hover {
    box-shadow: 0 8px 16px 0 var(--box-shadow);
  }

  .book-aladin-info {
    padding: 5px;
    padding-top: 10px;
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
    font-size: max(1vw,13px);
  }
  .book-aladin-store-none {
    text-align: left;
    font-size: max(1vw,13px);
    color: #c64756;
  }

@media screen and (max-width:768px) {
  .book-card{
    max-width:95%;
    min-height: auto;
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