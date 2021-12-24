import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex);

const c_headers = {
  v11 : {
    pd : {  'X-Device-Platform': 'W20O',
    'X-Device-Product': 'webOSTV 5.0',
    'X-Device-Sales-Model': 'WEBOS5.0',
    'X-Device-SDK-VERSION': '5.0.0',
    'X-Device-FCK': '184',
    },
    qt2 : {
      'X-Device-Platform': 'W20O',
      'X-Device-Product': 'webOSTV 5.0',
      'X-Device-Sales-Model': 'WEBOS5.0',
      'X-Device-SDK-VERSION': '5.0.0',
      'X-Device-FCK': '245',
      }
  },
    
  v12 : {
    pd : {
  'X-Device-Platform': 'W21O',
  'X-Device-Product': 'webOSTV 6.0',
  'X-Device-Sales-Model': 'WEBOS6.0',
  'X-Device-SDK-VERSION': '6.0.0',
  'X-Device-FCK': '220',
    },
    qt2 : {
      'X-Device-Platform': 'W21O',
      'X-Device-Product': 'webOSTV 6.0',
      'X-Device-Sales-Model': 'WEBOS6.0',
      'X-Device-SDK-VERSION': '6.0.0',
      'X-Device-FCK': '184',
    }
  }
};

export const store =  new Vuex.Store ( {
  state : {
    calledApi : '',
    req : '',
    res : '',
    time : '',

    // only for searchResult paging
    start_idxes :{},
    hit_cnts : {},
    now_cnts : {},
    total_cnts : {},

    // only for autoCompleted
    compleList : [],

    isThumb : false,
    hasCate : false,
    items : {}, 
    selected : '선택안됨', // selected item

    // for setting
    server : 'pd',
    version : 'v12',
    cntry : 'KR',
    language : 'kr-KR',
    languages : ['kr-KR','en-US'],
    fck : '220',

    init : {
      pd : "http://kr.lgtvsdp.com/rest/sdp/v11.0/initservices",
      qt2 : "http://qt2-kr.lgtvsdp.com/rest/sdp/v11.0/initservices",
    },

    headers : {
      'Access-Control-Allow-Origin' : '*',
      'X-Device-ContentsQA-Flag': 'N',
      'X-Device-Eco-Info': '1',
      'X-Device-Eula': 'additionalDataAllowed,customAdAllowed,generalTermsAllowed,networkAllowed,voiceAllowed',
      'X-Device-FW-Version': '00.00.00',
      'X-Device-ID': 'PsDN9MLUMuNmRQ/I9qWfYAgk9WHSr6tU3+yPLnyyP7bcmcO19ywxVrTiZfmvU20nTL7jiaONYf1c5BxoytZWDIwzTC4MfnQ4hpl9fMT0pUShpGD3uk2yWi0s66dIBpXi',

      'X-Device-Model': 'HE_DTV_W21O_AFABATAA',
      'X-Device-Netcast-Platform-Version': '6.0.0',

      'X-Device-Publish-Flag': 'N',
      'X-Device-Remote-Flag': 'N',
      'X-Device-Type': 'T01',
      'Content-Type': 'application/json',
      'X-Authentication': 'khjk3kp9n5hzsSj3b0jXLX/yOoc=',

      'X-Device-Platform': 'W21O',
      'X-Device-Product': 'webOSTV 6.0',
      'X-Device-Sales-Model': 'WEBOS6.0',
      'X-Device-SDK-VERSION': '6.0.0',
      'X-Device-FCK': '220',

      'X-Device-Country': 'KR',
      'X-Device-Country-Group': 'KR',
      'X-Device-Language': 'kr-KR',
      'X-Device-Locale': 'kr-KR',
      'X-Device-Spokenlanguage': 'ko-KR',

    },
    params : {
      'api_info' : 'auth:Y,provisioning:Y,services:Y,appupdatecheck:Y',
      'dram_size' : '1280',
      'support_3d' : 'NONE',
      'display_type' : 'LCD',
      'video_resolution' : 'UHD',
      'osd_resolution' : '1920,1080',
      'use_game_pad' : 'Y',
      'broadcast_type' : 'ATSC',
      'support_voice_recognition' : 'Y',
      'supportBnoModel' : 'false',
      'voice' : 'Y HTTP/1.1',
      'model_name' : 'WEBOS6.0',
    }
  },

  mutations : {
    initAuthentification : function(state) {
      var url = state.init.pd;
      if (state.server == 'qt2') {
        url = state.init.qt2;
      }
      
      axios({
        url: url,
        method: 'POST',
        headers : state.headers,
        params : state.params
    
      }).then(function(response) {
        state.headers['X-Authentication'] = response.data.initServices.authentication.sessionID;
        console.log(state.headers['X-Authentication'])
      }).catch(function (error) {
        console.log(error);

      });
    },

    setItem : function(state,selected) {
      state.selected = selected;
    },
    setItems : function(state,items) {
      state.items = items;
    },
    setOneCateItems : function(state,cate,cateItems) {
      state.items[cate] = cateItems;
    },
    setAutoCompleList : function(state,autoComple) {
      state.compleList = autoComple;
    },
    setSettingValue : function(state,form) {

      state.server = form.server;
      state.cntry = form.cntry;
      state.version = form.version;
      state.language = form.language;

      console.log(form);
      console.log(state);

      var n_header = c_headers[state.version][state.server];

      for ( var key in n_header) {
        var val = n_header[key];
        state.headers[key] = val
      }

      console.log(state.headers); 

    },


}


});