<template>
  <transition name="modal" appear>
    <div class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">

          <!-- 모달 헤더 -->
          <div class="modal-header">
            <slot name="header">
              책 정보
              <button class="modal-default-button" @click="$emit('close')"></button>
            </slot>
          </div>

          <!-- 모달 보디 -->
          <div class="modal-body">
            <slot name="body">
              <div v-for="(result,resultkey) in details" v-bind:key="resultkey">
                <div class="book-aladin-place">{{result.mallName}}</div>
                <div class="book-aladin-status" v-for="(status,statuskey) in result.stock" v-bind:key="statuskey">
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
            </slot>
          </div>

        </div>
      </div>
    </div>
  </transition>
</template>

<script>
  export default {
    props:['details']
  }
</script>

<style>
  .modal-mask {
    position: fixed;
    z-index: 9998;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, .5);
    display: table;
    transition: opacity .3s ease;
  }

  .modal-wrapper {
    display: table-cell;
    vertical-align: middle;
  }

  .modal-container {
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    width: 70%;
    max-height: 500px;
    margin: 0px auto;
    padding: 20px 30px;
    background-color: #fff;
    border-radius: 2px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, .33);
    transition: all .3s ease;
    font-family: Helvetica, Arial, sans-serif;
    overflow-y: scroll;
  }

  .modal-header {
    margin-top: 0;
    color: #8db596;
    font-size:2vw;
    font-weight:800;
    text-align:center;
  }

  .modal-body {
    margin: 20px 0;
  }

  .modal-default-button {
    border: 2px solid black;
    border-radius: 50%;
    left: 50%;
    bottom: 35px;
    width: 30px;
    height: 30px;
    background-color: #ffffff;
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