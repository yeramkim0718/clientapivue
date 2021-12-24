<template>
<div  class = "searchBar">
<vue-autosuggest  
    :suggestions="[{data: compleList}]"
    @input="onInputChange"
    v-on:keyup.enter="onSearch">
</vue-autosuggest>
</div>
</template>

<script>
import { VueAutosuggest } from 'vue-autosuggest';
import {mapState} from 'vuex';
import * as searchApi from '@/api/search';

export default {
  computed : mapState ([
    'compleList',
    'instantList'
  ]),
  methods: {
    onInputChange(input) {
      searchApi.callAutoCompleteResult(input);
      searchApi.callInstantSearchResult(input);
    },
    onSearch(event) {
      console.log(event.target.value);
      searchApi.callSearchResult(event.target.value);
    }
  },
  components : {
    'vue-autosuggest' : VueAutosuggest
  }
};
</script>

<style>
.searchBar {
  width : 450px;
}

</style>