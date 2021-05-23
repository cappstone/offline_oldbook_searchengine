<template>
  <transition name="modal" appear>
    <section class="modal-overlay">
      <div class="modal-window">
        <!-- 모달 헤더 -->
        <div class="modal-header">
          <span class="book-copy" v-on:click="copyData(details)"><i class="far fa-copy fa-2x"></i></span>
          <div class="book-name">{{details.bookName}}</div>
          <div>{{details.description}}</div>
        </div>

        <!-- 모달 보디 -->
        <div>
          <div id="book-aladin-map"></div>
        </div>
        <div class="modal-body">
          <div class="body-container" v-for="(result,resultkey) in details.mall" v-bind:key="resultkey" v-on:click="getLocation(result.mallName,result.mall_id)">
            <div class="book-aladin-place"><b> {{result.mallName}}</b> - {{result.stockCount}}개</div>
            <div v-if="result.stock">
              <div class="book-aladin-status" v-for="(status,statuskey) in result.stock" v-bind:key="statuskey">
                <table class="book-aladin-stock">
                  <tr>
                    <td class="book-aladin-location">위치: {{status.location}}</td>
                    <td rowspan="5" class="book-aladin-price">{{status.price}}원</td>
                  </tr>
                  <tr>
                    <td class="book-aladin-quality">품질: {{status.quality}}</td>
                  </tr>
                </table>
              </div>
            </div>
            <div v-else>
              <table class="book-aladin-stock">
                <tr>
                  <td class="book-aladin-location">위치: {{result.location}}</td>
                  <td rowspan="5" class="book-aladin-price">{{result.price}}원</td>
                </tr>
                <tr>
                  <td class="book-aladin-quality">재고: {{result.stockCount}}개</td>
                </tr>
              </table>
            </div>
          </div>
        </div>

        <!-- 모달 풋터 -->
        <div class="modal-footer">
          <span>지점 이름을 누르면 해당 위치로 이동합니다.</span>
          <button class="modal-default-button" @click="$emit('close')"><i class="fas fa-times fa-3x"></i></button>
        </div>
        <div id="toast">복사 완료했습니다.</div>
      </div>
    </section>
  </transition>
</template>

<script>
  export default {
    props:['details'],

    data: function(){
      return{
        map: {},
        location: {},
        mall: this.details.mall,
        address: {},
        addresstext: '',
        toastshow: false,
        window: {},
        markerlist: []
      }
    },

    mounted: function() {
      if (window.kakao && window.kakao.maps) {
        this.initMap();
      }
      else {
        this.addKakaoMapScript();
      }
    },

    methods: {
      copyData(data) {
        var textarea= document.createElement('textarea');
        var text= String(data.bookName+'\n'+data.description);
        for (var i in data.mall){
          text+=String('\n\n'+data.mall[i].mallName+'에 '+data.mall[i].stockCount+'개 존재');
          if (data.mall[i].stock){
            for (var j in data.mall[i].stock){
              text+=String('\n\n'+data.mall[i].stock[j].location+'에 위치, '
                +data.mall[i].stock[j].quality+'급 품질\n'
                +'가격 '+data.mall[i].stock[j].price);
            }
          } else {
            text+=String('\n\n'+data.mall[i].location+'에 위치\n'
            +'가격 '+data.mall[i].price+'원')
          }
        }
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand("copy");
        document.body.removeChild(textarea);

        const toaster = document.getElementById('toast');
        this.toastshow = true;
        toaster.classList.add('show');
        setTimeout(()=>{
          toaster.classList.remove('show');
          this.toastshow=false;
        },2700);
      },

      initMap() {
        var mapContainer = document.getElementById("book-aladin-map"); // 지도를 표시할 div
        var mapOption = {
          center: new kakao.maps.LatLng(35.77114136986587, 127.84584124824799), // 지도의 중심좌표
          level: document.documentElement.clientWidth>768?13:15, // 지도의 확대 레벨
        };
        this.map = new kakao.maps.Map(mapContainer, mapOption);
        this.location = new kakao.maps.services.Places();
        this.address = new kakao.maps.services.Geocoder();
        this.window = new kakao.maps.InfoWindow({zIndex:1});

        var tempmap=this.map;
        var tempmarker=this.markerlist;
        
        for (var i=0; i<this.mall.length; i++) {
          this.location.keywordSearch(this.mall[i].mallName=="YES24 수영점F1963"?"YES24 수영점":this.mall[i].mallName, function(data,status){
            if (status === kakao.maps.services.Status.OK) {
              for (var j=0; j<data.length; j++){
                var marker= new kakao.maps.Marker({
                  map: tempmap,
                  position: new kakao.maps.LatLng(data[j].y,data[j].x)
                });
                tempmarker.push(marker);
              }
            }
          });
          this.markerlist=tempmarker;
        }
      },

      addKakaoMapScript() {
        const script = document.createElement("script");
        script.onload = function() { kakao.maps.load(this.initMap); }
        script.src = "//dapi.kakao.com/v2/maps/sdk.js?appkey=86a89344314a38af4882760b5c260ce0&libraries=services";
        document.head.appendChild(script);
      },

      getLocation(keyword,index) {
        var tempmap=this.map;
        var tempadd=this.address;
        var tempwin=this.window;
        var tempmarker=this.markerlist[index];
        var tempaddtext=this.addtext;
        
        this.location.keywordSearch(keyword=="YES24 수영점F1963"?"YES24 수영점":keyword, function(data,status){
          if (status === kakao.maps.services.Status.OK) {

            // 검색된 장소 위치를 기준으로 지도 범위를 재설정하기위해
            // LatLngBounds 객체에 좌표를 추가합니다
            var bounds = new kakao.maps.LatLngBounds();

            for (var i=0; i<data.length; i++) {
              var cor=[data[i].x,data[i].y]

              tempadd.coord2Address(cor[0],cor[1], function(result){
                tempaddtext=result[0].road_address.address_name;
                tempwin.setContent('<div style="width:200px;padding:5px;font-size:12px;color:#8db596;word-break:keep-all">' + tempaddtext + '</div>');
                tempmarker.setPosition(new kakao.maps.LatLng(cor[1],cor[0]));
                tempwin.open(tempmap,tempmarker);
              });

              bounds.extend(new kakao.maps.LatLng(cor[1], cor[0]));
            }

            // 검색된 장소 위치를 기준으로 지도 범위를 재설정합니다
            tempmap.setBounds(bounds);
          }
        });
      }
    }
  }
</script>

<style>
  .modal-overlay {
    position: fixed;
    align-items: center;
    justify-content: center;
    z-index: 99;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, .5);
    display: flex;
    transition: opacity .3s ease;
    cursor: default;
  }

  .modal-window {
    width: 70%;
    max-height: auto;
    margin: 0px auto;
    padding: 0px;
    background-color: #ffffff;
    border-radius: 2px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, .33);
    transition: all .3s ease;
    overflow-y: visible;
    cursor: default;
  }

  .modal-header {
    font-size:max(1vw,12px);
    font-weight: 800;
    margin: 10px;
  }

  .book-name {
    max-width: 90%;
    color: #8db596;
    font-size: max(1.3vw,18px);
    position: relative;
    margin: 0 auto;
    word-break: keep-all;
  }

  .book-copy {
    position: absolute;
    right: 16%;
  }

  .book-copy:active {
    color: #4788de;
  }

  .modal-body {
    height: 60vh;
    margin: 0;
    padding-left: 10px;
    padding-right: 10px;
    text-align: left;
    overflow-y: auto;
  }
  
  .body-container:hover {
    cursor: pointer;
    color: #8db596;
  }

  .modal-default-button {
    width: 100%;
    border: none;
    cursor: pointer;
  }

  .modal-default-button:focus {
    border-top:1px solid #557173;
    outline:none;
  }

  /*
  * The following styles are auto-applied to elements with
  * transition="modal" when their visibility is toggled
  * by Vue.js.
  *
  * You can easily play with the modal transition by editing
  * these styles.
  */

  .modal-enter {
    opacity: 0;
  }

  .modal-leave-active {
    opacity: 0;
  }

  .modal-enter .modal-container,
  .modal-leave-active .modal-container {
    -webkit-transform: scale(1.1);
    transform: scale(1.1);
  }
  
  .book-aladin-place {
    font-size: max(1vw,14px);
    border-bottom: 1px groove #557174;
  }

  .book-aladin-stock {
    padding: 5px;
    width:100%;
    font-size: max(1vw,12px);
  }

  .book-aladin-price {
    text-align: right;
    font-size: max(1vw,14px);
    font-weight: 800;
  }

  #book-aladin-map {
    width: 50%;
    height: 60vh;
    margin: 0;
    float: right;
  }

  #toast {
    position: absolute;
    bottom: 88%;
    left: 83%;
    transform: translate(-50%, 10px);
    border-radius: 30px;
    overflow: hidden;
    font-size: max(1vw,12px);
    padding: 5px 5px;
    opacity: 0;
    visibility: hidden;
    transition: opacity 0.5s, visibility 0.5s, transform 0.5s;
    background: #557174;
    color: white;
    z-index: 999;
  }
  #toast.show {
    opacity: 1;
    visibility: visible;
    transform: translate(-50%, 0);
  }

  @media screen and (max-width:768px){
    .modal-window{
      width: 95%;
    }

    .book-name {
      max-width: 84%;
    }

    .book-copy {
      right: 5%;
    }

    #book-aladin-map {
      width:100%;
      height: 30vh;
      float: none;
    }

    #toast {
      bottom: 30px;
      left: 50%;
    }

    .modal-body {
      margin-top: 10px;
      height: 30vh;
    }
    
    .book-aladin-stock {
      padding: 0;
    }
  }
</style>