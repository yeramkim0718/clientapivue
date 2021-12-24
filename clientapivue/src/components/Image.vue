<template>
<div>
  <b-tabs v-if = "hasCate && isThumb" content-class="mt-3">
    
    <b-tab  v-for = "(cateItems,cate,index) in items" v-model = "tabIndex" v-bind:key = "cate" v-bind:id = "cate"
    v-bind:title = "cate" > 
    <b-card-header v-if = "calledApi==='searchResult'"> 
    <b-button-group >
        <b-button @click = "clickPrevious(cate,index)" :disabled ="start_idxes[cate] <= 1" >Previous</b-button>
        <b-button @click = "clickNext(cate,index)" :disabled ="now_cnts[cate] == total_cnts[cate]">Next</b-button>
    </b-button-group>
    <span style = "align:right"> {{now_cnts[cate]}} / {{total_cnts[cate]}} </span>
    </b-card-header>    
    <div class = "elem" v-for = "item in cateItems" v-bind:key= "item" v-on:click="clickItem(item)">
    <img class = "img" v-bind:src = "item.thumbnail" >
    <div class = "title">
      <p> {{item.title}} </p>
    </div>
    </div>
  </b-tab>
  </b-tabs>
    <div v-else-if = "isThumb" class = "elem" v-for = "item in items" v-bind:key="item" v-on:click="clickItem(item)">
    <img class = "img" v-bind:src = "item.thumbnail"  >
      <div class = "title">
        <p> {{item.title}} </p>
      </div>
    </div>

    <b-tabs  v-else-if = "hasCate" class = "elem" >
      <b-tab  v-for = "(cateItems,cate) in items" v-bind:key = "cateItems" v-bind:title = "cate" >
        <p> {{cateItems}} </p>
      </b-tab>
    </b-tabs >

    <div v-else class = "elem" v-for = "item in items" v-bind:key="item" v-on:click="clickItem(item)">
        <p> {{item}} </p>
    </div>

  </div>
</template>

<script>
import {mapState} from 'vuex';
import * as searchApi from '@/api/search';

export default {
  data() {
      return {
        tabIndex : 0,

        
      }
    },

  computed : mapState([
    'isThumb',
    'hasCate',
    'items',
    'selected',
    'calledApi',
    'hit_cnts',
    'now_cnts',
    'total_cnts',
    'start_idxes'
  ]),

  methods : {
    clickItem : function(item) {
      this.$store.selected = '';
      this.$store.commit('setItem',item);
    },
    clickPrevious : function(cate,index) {
      this.tabIndex = index;
      searchApi.clickSearchPrevious(cate);
    },
    clickNext : function(cate,index) {
      this.tabIndex = index;
      searchApi.clickSearchNext(cate);
    }
  }
}
</script>

<style scoped>

.next {
  display:block;
  margin-left:auto;
}
.title {
  text-align : center;
  font-size:5px;
  width:130px;
  height:30px;
}

.img {
  width :130px;
  height : 200px;
}
.elem {
  float : left;
  margin : 5px;
}
</style>


