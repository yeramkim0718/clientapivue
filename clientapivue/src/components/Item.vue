<template>
<div class = "request">
    <pre style = "overflow:visible">{{selected}}</pre>
</div>

</template>
<script>
import {mapState} from 'vuex';
export default {
    computed : mapState([
    'selected'
  ])
}
</script>
<style scoped>
.request {
    width:500px; 
    height: 300px;
    padding:10px;
    align:left;
    overflow: scroll;
    border : 0.5px solid grey;
}
</style>