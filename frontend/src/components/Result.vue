<template>
  <div v-if="book[0]!=''">
    <div v-if="book[1]=='0'">

      <div v-for="(book,bookey) in book[0]" v-bind:key="bookey" v-bind:class="['book-card', {'accordion-open': accordionOpen.includes(bookey)}]">
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
            <td><b>{{book.stores}}</b></td>
          </tr>
          <tr>
            <td class="temp">
              <button class="book-aladin-button" v-on:click="moreView(bookey)">
                <label for="book-aladin-button" v-if="book.result==''"><b>재고 없음</b></label>
                <label for="book-aladin-button" v-else><b>자세히</b></label>
              </button>
            </td>
          </tr>
        </table>

        <div class="book-aladin-result">
          <div v-for="(result,resultkey) in book.result" v-bind:key="resultkey">
            <div class="book-aladin-place">{{result.mall}}</div>
              <div class="book-aladin-status" v-for="(status,statuskey) in result.status_stock" v-bind:key="statuskey">
                <table class="book-aladin-stock">
                  <tr>
                    <td class="book-aladin-location">{{status.location}}</td>
                    <td rowspan="2" class="book-aladin-price">{{status.price}}</td>
                  </tr>
                  <tr>
                    <td class="book-aladin-quality">{{status.quality}}급</td>
                  </tr>
                </table>
              </div>
          </div>
        </div>

      </div>

    </div>

    <div id="yes" v-else>
      <ul class="book-card" v-for="key in book[0]" v-bind:key="key" style="margin-bottom:1vw; padding:25px">
        <li>
          <b>{{key.mall}}</b>
          <ol v-for="resultkey in key.result" v-bind:key="resultkey">
            <li v-if="resultkey!='검색 결과 없음'">
              <b>{{resultkey.bookname}}</b>
              <p>{{resultkey.description}}</p>
              <div>{{resultkey.location}}이 {{resultkey.price}} 가격으로 있습니다.</div>
            </li>
            <li v-else>
              <div>현재 재고가 없습니다.</div>
            </li>
          </ol>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
    props:['book'],

    data: function() {
      return {
        accordionOpen:[]
      }
    },

    methods:{
      moreView: function(index){
        if (this.accordionOpen.includes(index)) {
          this.accordionOpen = this.accordionOpen.filter(i => i != index)
          return
        }
        this.accordionOpen.push(index);
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

    max-width: 63%;
    height: auto;
    position: relative;

    transition: all 0.3s ease;
  }

  .book-card:hover {
    box-shadow: 0 16px 32px 0 rgba(99,230,138,0.6);
  }

  
  .book-card:not(.accordion-open) .book-aladin-result {
    height:0;
    overflow:hidden;
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

    overflow:auto;
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
  }

  .book-aladin-button {
    width: 100%;
    height: 100%;
    border-style: groove;
    border-color: #557174;
    background-color: white;
    cursor: pointer;
  }

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
</style>