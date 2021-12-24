<template>
<div> 
<div class = "request">
  <b-tabs content-class="mt-3">
    <b-tab  title="request" active ><pre style = "overflow:visible">{{req}}</pre> 
    </b-tab>
    <b-tab title="response">
      <b-card-header>응답시간 : {{time}}</b-card-header>
      <pre style = "overflow:visible">{{res}}</pre>
    </b-tab>
  </b-tabs>
</div>
</div>

</template>
<script >

import {mapState} from 'vuex';
export default {
  created() { 
    this.$store.commit('initAuthentification');
     }, 

  computed : mapState([
    'req',
    'res',
    'time'

  ])

}
</script>
<style scoped>
.request {
    width:500px; 
    height: 300px;
    padding:10px;
    align:left;
    overflow : scroll;
    border : 0.5px solid grey;
}
</style>