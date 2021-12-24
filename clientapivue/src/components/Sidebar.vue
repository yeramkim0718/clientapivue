<template>
  <div>
    <b-sidebar id="sidebar-backdrop" backdrop shadow>    
      <div class="px-3 py-2">
        <b-form-group style = font-size:20px; label="통합검색" >
          <b-form-select style = font-size:15px; 
          v-model="search" :options="searches" 
          @change='change'></b-form-select>
        </b-form-group>
      </div>
    </b-sidebar>
  </div>
</template>

<script>
import * as searchApi from '@/api/search';

  export default {
    data() {
      return {
        search: '',
        searches: [
          'search_result',
          'instant_search_result',
          'keyword_result',
          'search_condition_result',
          'content_detail_search_result',
          'guide_keyword',
          'youtube_music_search',
        ]
      }
    },

    methods : {
      change : function() {
        switch(this.search) {
          case "search_result" :
            searchApi.callSearchResult('movie');
            break;
          case "instant_search_result" :
            searchApi.callInstantSearchResult('movie');
            break;
          case "keyword_result" :
            searchApi.callKeywordResult();
            break;
          case "search_condition_result" :
            searchApi.callSearchConditionResult();
            break;
          case "content_detail_search_result" :
            searchApi.callContentDetailSearchResult();
            break;
          case "guide_keyword" :
            searchApi.callGuideKeyword();
            break;
          case "youtube_music_search" :
            searchApi.callYoutubeMusicSearch();
            break;
                    
        }

      }
    }
  }
</script>