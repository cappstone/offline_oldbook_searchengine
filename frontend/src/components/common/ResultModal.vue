<template>
  <transition name="modal" appear>
    <section class="modal-overlay">
      <div class="modal-window">
        <!-- 모달 헤더 -->
        <div class="modal-header">
          <div id="book-aladin-map"></div>
        </div>

        <!-- 모달 보디 -->
        <div class="modal-body">
          <div v-for="(result,resultkey) in details" v-bind:key="resultkey">
            <div class="book-aladin-place" v-on:click="getLocation(result.mallName)"><b> {{result.mallName}}</b> - {{result.stockCount}}개</div>
            <div v-if="result.stock">
              <div class="book-aladin-status" v-for="(status,statuskey) in result.stock" v-bind:key="statuskey">
                <table class="book-aladin-stock">
                  <tr>
                    <td class="book-aladin-location">위치: {{status.location}}</td>
                    <td rowspan="5" class="book-aladin-price">{{status.price}}</td>
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
                  <td rowspan="5" class="book-aladin-price">{{result.price}}</td>
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
        result: this.details,
        address: {},
        window: {}
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
      initMap() {
        var mapContainer = document.getElementById("book-aladin-map"); // 지도를 표시할 div
        var mapOption = {
          center: new kakao.maps.LatLng(37.611014434376564, 126.99575607232063), // 지도의 중심좌표
          level: 15, // 지도의 확대 레벨
        };
        this.map = new kakao.maps.Map(mapContainer, mapOption);
        this.location = new kakao.maps.services.Places();
        this.address = new kakao.maps.services.Geocoder();
        this.window = new kakao.maps.InfoWindow({zIndex:1});

        var tempmap=this.map;
        var tempwin=this.window;
        
        for (var i=0; i<this.result.length; i++) {
          this.location.keywordSearch(this.result[i].mallName, function(data,status){
            if (status === kakao.maps.services.Status.OK) {
              for (var j=0; j<data.length; j++){
                var marker = new kakao.maps.Marker({
                  map: tempmap,
                  position: new kakao.maps.LatLng(data[j].y, data[j].x) 
                });
              }
            }
          });
        }
      },

      addKakaoMapScript() {
        const script = document.createElement("script");
        script.onload = function() { kakao.maps.load(this.initMap); }
        script.src = "//dapi.kakao.com/v2/maps/sdk.js?appkey=86a89344314a38af4882760b5c260ce0&libraries=services";
        document.head.appendChild(script);
      },

      getLocation(keyword) {
        //console.log(this.map);
        var tempmap=this.map;
        var tempadd=this.address;
        var tempwin=this.window;

        this.location.keywordSearch(keyword, function(data,status){
          //console.log(data);
          if (status === kakao.maps.services.Status.OK) {

            // 검색된 장소 위치를 기준으로 지도 범위를 재설정하기위해
            // LatLngBounds 객체에 좌표를 추가합니다
            var bounds = new kakao.maps.LatLngBounds();

            for (var i=0; i<data.length; i++) {
              var marker = new kakao.maps.Marker({
                map: tempmap,
                position: new kakao.maps.LatLng(data[i].y,data[i].x)
              });

              var juso='';

              tempadd.coord2Address(data[i].x,data[i].y, function(result){
                juso=result[0].road_address.address_name;
                tempwin.setContent('<div style="padding:5px;font-size:12px;">' + juso + '</div>');
                tempwin.open(tempmap,marker);
              });

              bounds.extend(new kakao.maps.LatLng(data[i].y, data[i].x));
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
    z-index: 9999;
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
    max-height: 80%;
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
    color: #8db596;
    font-size:max(1.3vw,18px);
    font-weight:800;
    text-align:center;
  }

  .modal-body {
    height: 30vh;
    margin: 0;
    text-align: left;
    overflow-y: auto;
  }
  
  .book-aladin-place {
    cursor: pointer;
  }

  .modal-default-button {
    width: 100%;
    border-top: 1px solid #000000;
    cursor: pointer;
  }

  .modal-default-button:focus {
    border:none;
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
    height: 30vh;
    margin: 0;
    float: right;
  }

  @media screen and (max-width:768px){
    .modal-window{
      width: 95%;
    }

    #book-aladin-map {
      width:100%;
      float: none;
    }
    
    .book-aladin-stock {
      padding: 0;
    }
  }
</style>