import axios from 'axios';
import {store} from '../store/default'

//var active = '';
//var position = {};

var searchResult = {
  url : 'http://KR.lgtvsdp.com/rest/sdp/v12.0/search/retrieval',
  method : "POST",
  params : {
    'version' : 'v1',
    'service' : 'com.lge.rcmd.api.client',
    'start_index' : 1,
    'max_results' : 8,
    'domain': 'epg,tvshow,movie,youtube',
    "epg_info": 
      "113|2-1,114|3-1,798|4-1,54|5-1,567|6-1,133|7-1,795|8-1,45|9-1,606|10-1,140|11-1,468|12-1,138|13-1,881|14-1,250|15-1,570|16-1,20|17-1,571|18-1,569|19-1,738|20-1,632|21-1,70|21-1,743|22-1,573|23-1,24|24-1,142|25-1,148|26-1,781|27-1,25|27-2,253|31-1,285|32-1,499|33-1,684|33-2,679|34-1,509|37-1,176|38-1,706|39-1,104|39-1,916|43-1,19|44-1,22|45-1,129|46-1,388|47-1,UNKNOWN|48-1,754|51-1,335|52-1,UNKNOWN|55-1,100|56-1,101|57-1,UNKNOWN|58-1,818|59-1,147|61-1,124|62-1,30|63-1,487|64-1,44|65-1,172|67-1,666|68-1,23|69-1,38|70-1,358|71-1,252|73-1,55|74-1,669|75-1,27|77-1,118|78-1,780|79-1,28|80-1,813|81-1,106|83-1,622|84-1,379|86-1,46|88-1,735|89-1,918|90-1,792|91-1,33|93-1,42|94-1,156|94-2,903|96-1,47|97-1,427|98-1,184|99-1,113|2-0,114|3-0,798|4-0,54|5-0,567|6-0,133|7-0,795|8-0,45|9-0,606|10-0,140|11-0,468|12-0,138|13-0,881|14-0,250|15-0,570|16-0,20|17-0,571|18-0,569|19-0,743|20-0,70|21-0,738|22-0,573|23-0,24|24-0,142|25-0,148|26-0,781|27-0,780|28-0,916|29-0,19|30-0,388|31-0,813|32-0,22|33-0,706|34-0,679|35-0,285|36-0,253|37-0,124|41-0,147|42-0,30|43-0,427|95-0,184|96-0,47|97-0,148|1,54|2,632|3,567|4,881|5,250|6,795|7,140|8,606|9,138|10,468|11,45|12,798|13,133|14,570|15,20|16,743|17,571|18,569|19,816|20,253|22,27|23,24|24,573|25,622|26,19|33,22|34,167|35,129|36,388|37,447|38,706|39,750|40,740|41,916|42,103|43,679|44,818|45,109|50,30|51,124|52,147|53,398|54,109|55,922|56,615|57,44|61,487|62,578|63,104|64,335|71,754|72,684|73,783|74,25|75,108|76,37|77,379|78,499|79,285|80,598|81,100|82,912|91,693|92,355|93,332|94,664|95,915|96,925|97,694|98,38|101,172|102,430|103,725|104,160|105,91|106,685|107,358|108,596|150,17|151,23|152,749|153,596|154,723|155,176|201,414|202,906|203,753|205,15|206,415|207,128|208,247|209,917|210,918|211,597|212,817|213,130|250,126|251,43|252,118|253,55|254,46|255,488|257,94|258,262|259,254|260,613|261,80|262,359|351,78|352,106|353,132|354,594|355,157|356,380|357,771|358,703|360,117|361,509|401,119|402,792|403,900|404,63|405,904|406,26|409,697|410,735|411,933|412,764|413,79|414,579|415,495|416,50|417,166|418,798|451,546|452,777|453,561|454,384|455,47|501,427|502,184|503,707|504,156|550,42|551,293|552,907|553,688|554,52|555,903|556,33|557,779|558,48|559"
    
  }, 
};

var autoCompleteResult = {
  url : 'http://KR.lgtvsdp.com/rest/sdp/v12.0/search/auto_keyword',
  method : 'POST',
  params : {
    'version' : 'v1',
    'service' : 'com.lge.rcmd.api.client',
    'max_results' : 5,
    'domain': 'epg,tvshow,movie,youtube',
    'epg_code' : '794,795,796,798,797'
  }
};

var instantSearchResult = {
  url : 'http://KR.lgtvsdp.com/rest/sdp/v12.0/search/instant',
  method : 'POST',
  params : {
    'version' : 'v1',
    'service' : 'com.lge.rcmd.api.client',
    'query' : 'drama',
    'start_index' : '1',
    'max_results' : '8',
    'domain': 'epg,tvshow,movie,youtube'
  }
};

var keywordResult = {
  url : 'http://KR.lgtvsdp.com/rest/sdp/v12.0/search/popular_keyword',
  method : 'POST',
  params : {
    'version' : 'v1',
    'service' : 'com.lge.rcmd.api.client',
    'max_results' : '5'
  }
};

var searchConditionResult = {
  url : 'http://KR.lgtvsdp.com/rest/sdp/v12.0/search/condition',
  method : 'POST',
  params : {
    'version' : 'v1',
    'service' : 'com.lge.rcmd.api.client'
  }
};

var contentDetailSearchResult = {
  url : 'http://KR.lgtvsdp.com/rest/sdp/v12.0/search/content_detail',
  method : 'POST',
  params : {
    'version' : 'v1',
    'service' : 'com.lge.rcmd.api.client',
    'query' : 'My'
  }
};

var guideKeyword = {
  url : 'http://KR.lgtvsdp.com/rest/sdp/v12.0/search/guide_keyword',
  method : 'POST',
  params : {
    'service' : 'com.lge.rcmd.api.client',
    'limit' :  3,
    'domain' : 'epg_onair,epg_program,tvshow,movie'
  }
};

var youtubeMusicSearch = {
  url : 'http://KR.lgtvsdp.com/rest/sdp/v12.0/search/youtube/music',
  method : 'POST',
  params : {
    'service' : 'com.lge.rcmd.api.client',
    'start_index' : 1,
    'max_results' : 5,
    'query' : "oasis don't look back in anger"
  }
};


export function callSearchResult (keyword) {

  searchResult.params.query = keyword;
  searchResult.params.domain = "epg,tvshow,movie,youtube";
  searchResult.params.start_index = 1;
  
  store.state.calledApi = 'searchResult';
  store.state.req = JSON.stringify(searchResult.params, null, " ");

  store.state.res = '';
  store.state.isThumb = true;
  store.state.hasCate = true;
  store.commit('setItems',{});

  var items = {};

  axios({
    url: searchResult.url,
    method: searchResult.method,
    headers : store.state.headers,
    params : searchResult.params,

  }).then(function(response) {
    let res = response;
    store.state.res =JSON.stringify(res, null, " ");
    store.state.time = response.data.response.time;

    for (var i =0; i<response.data.response.results.length;i++) {
      var cate = response.data.response.results[i].id;
      items.[cate] = response.data.response.results[i].doc;
      store.state.total_cnts.[cate] = response.data.response.results[i].total_count;
      store.state.hit_cnts.[cate] = response.data.response.results[i].hit_count;
      store.state.now_cnts.[cate] = store.state.hit_cnts.[cate];
      store.state.start_idxes.[cate] = 1;
      console.log(store.state.hit_cnts.[cate]);
    }
    store.commit('setItems',items);
    console.log(response);

  }).catch(function (error) {
    store.state.res = error;
    console.log(error);
  });
  }

  export function clickSearchPrevious (domain) {
    console.log(store.state.hit_cnts.[domain]);

    store.state.calledApi = 'searchResult';
    store.state.start_idxes.[domain] = searchResult.params.start_index;
    searchResult.params.domain = domain;
    searchResult.params.start_index = searchResult.params.start_index - searchResult.params.max_results;
    store.state.start_idxes.[domain] = searchResult.params.start_index;
    store.state.now_cnts.[domain] = store.state.now_cnts.[domain]
    - store.state.hit_cnts.[domain];
    
    store.state.req = JSON.stringify(searchResult.params, null, " ");
    store.state.res = '';
  
    axios({
      url: searchResult.url,
      method: searchResult.method,
      headers : store.state.headers,
      params : searchResult.params,
  
    }).then(function(response) {
      
      console.log(response);
      store.state.res =JSON.stringify(response, null, " ");
      store.state.time = response.data.response.time;

      var item = response.data.response.results[0].doc;

      store.state.hit_cnts.[domain] = response.data.response.results[0].hit_count;


      store.state.items.[domain] = item;
  
    }).catch(function (error) {
      store.state.res = error;
      console.log(error);
    });
  }

  export function clickSearchNext (domain) {
    console.log('clickSearchNext search.js' )
    store.state.calledApi = 'searchResult';
    searchResult.params.start_index = searchResult.params.start_index + store.state.hit_cnts.[domain] ;    
    store.state.start_idxes.[domain] = searchResult.params.start_index;
    searchResult.params.domain = domain;

    store.state.req = JSON.stringify(searchResult.params, null, " ");
    store.state.res = '';
  
    axios({
      url: searchResult.url,
      method: searchResult.method,
      headers : store.state.headers,
      params : searchResult.params,
  
    }).then(function(response) {
      store.state.res =JSON.stringify(response, null, " ");
      store.state.time = response.data.response.time;

      var item = response.data.response.results[0].doc;
      store.state.hit_cnts.[domain]  = response.data.response.results[0].hit_count;
      store.state.now_cnts.[domain] = store.state.now_cnts.[domain]
                                      + store.state.hit_cnts.[domain];
      store.state.items.[domain] = item;

  
    }).catch(function (error) {
      store.state.res = error;
      console.log(error);
    });
  }

export function callInstantSearchResult (keyword) {
  console.log('instantSearchResult');
  instantSearchResult.params.query = keyword;
  store.state.calledApi = 'instantSearchResult';
  store.state.req = JSON.stringify(instantSearchResult.params, null, " ");
  store.state.res = '';
  store.state.isThumb = true;
  store.state.hasCate = false;
  store.commit('setItems',{});

  axios({
    url: instantSearchResult.url,
    method:  instantSearchResult.method,
    headers : store.state.headers,
    params : instantSearchResult.params

  }).then(function(response) {
    store.state.res = JSON.stringify(response, null, " ");
    store.commit('setItems',response.data.response.results);
    store.state.time = response.data.response.time;

    console.log(response);

  }).catch(function (error) {
    store.state.res = error;
    console.log(error);

  });
 }
 
export function callAutoCompleteResult (keyword) {
  console.log('autoCompleteResult');
  autoCompleteResult.params.query = keyword;

  axios({
    url: autoCompleteResult.url,
    method:  autoCompleteResult.method,
    headers : store.state.headers,
    params : autoCompleteResult.params

  }).then(function(response) {
    var autoComple = [];
    console.log(response.data.response.results)

    for (var i =0; i<response.data.response.results.length;i++) {
      var keyword = response.data.response.results[i].keyword;
      autoComple.push(keyword);
    }
    store.commit('setAutoCompleList',autoComple);
    console.log(autoComple);

  }).catch(function (error) {
    store.state.res = error;
    console.log(error);

  });
}

export function callKeywordResult () {
  console.log('keywordResult');
  store.state.calledApi = 'keywordResult';
  store.state.req = keywordResult.params;
  store.state.res = '';
  store.state.isThumb = false;
  store.state.hasCate = false;
  store.commit('setItems',{});

  axios({
    url: keywordResult.url,
    method:  keywordResult.method,
    headers : store.state.headers,
    params : keywordResult.params

  }).then(function(response) {
    store.state.res = response;
    store.state.time = response.data.response.time;
    store.commit('setItems',response.data.response.results);
    console.log(response);

  }).catch(function (error) {
    store.state.res = error;
    console.log(error);

  });
}

export function callSearchConditionResult () {
  console.log('searchConditionResult');
  store.state.calledApi = 'searchConditionResult';
  store.state.req = searchConditionResult.params;
  store.state.res = '';
  store.state.isThumb = false;
  store.state.hasCate = false;
  store.commit('setItems',{});

  axios({
    url: searchConditionResult.url,
    method:  searchConditionResult.method,
    headers : store.state.headers,
    params : searchConditionResult.params

  }).then(function(response) {
    store.state.res = response;
    store.state.time = response.data.response.time;
    store.commit('setItems',response.data.response.results);
    console.log(response);

  }).catch(function (error) {
    store.state.res = error;
    console.log(error);

  });
}

export function callContentDetailSearchResult () {
  console.log('contentDetailSearchResult');
  store.state.calledApi = 'contentDetailSearchResult';
  store.state.req = contentDetailSearchResult.params;
  store.state.res = '';
  store.state.isThumb = true;
  store.state.hasCate = true;
  store.commit('setItems',{});

  var items = {};

  axios({
    url: contentDetailSearchResult.url,
    method:  contentDetailSearchResult.method,
    headers : store.state.headers,
    params : contentDetailSearchResult.params

  }).then(function(response) {
    store.state.res = response;
    store.state.time = response.data.response.time;
    for (var i =0; i<response.data.response.results.length;i++) {
      var cate = response.data.response.results[i].domain;
      items.[cate] = response.data.response.results[i].doc;
    }
    store.commit('setItems',items);
    console.log(store.state.items);

  }).catch(function (error) {
    store.state.res = error;
    console.log(error);

  });
}

export function callGuideKeyword () {
  console.log('guideKeyword');
  store.state.calledApi = 'guideKeyword';
  store.state.req = guideKeyword.params;
  store.state.res = '';
  store.state.isThumb = false;
  store.state.hasCate = true;
  store.commit('setItems',{});

  axios({
    url: guideKeyword.url,
    method:  guideKeyword.method,
    headers : store.state.headers,
    params : guideKeyword.params

  }).then(function(response) {
    store.state.res = response;
    var items = {};
    store.state.time = response.data.time;

    console.log(response);
    items = response.data.results;

    store.commit('setItems',items);

  }).catch(function (error) {
    store.state.res = error;
    console.log(error);

  });
}

export function callYoutubeMusicSearch () {
  console.log('youtubeMusicSearch');
  store.state.calledApi = 'youtubeMusicSearch';
  store.state.req = youtubeMusicSearch.params;
  store.state.res = '';
  store.state.isThumb = true;
  store.state.hasCate = false;
  store.commit('setItems',{});

  axios({
    url: youtubeMusicSearch.url,
    method:  youtubeMusicSearch.method,
    headers : store.state.headers,
    params : youtubeMusicSearch.params

  }).then(function(response) {
    store.state.res = response;
    store.state.time = response.data.response.time;

    store.commit('setItems',response.data.response.results);
    console.log(response);

  }).catch(function (error) {
    store.state.res = error;
    console.log(error);
  });
}
