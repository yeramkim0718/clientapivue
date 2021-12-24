<template>
  <b-navbar type="dark" variant="dark" style = "padding:3px; display:block">
      <b-navbar-brand style = "display:inline-block; font-size:20px">APIClient</b-navbar-brand>
      <b-button v-b-toggle.sidebar-backdrop>Sidebar</b-button>

  <b-button class = "setting" v-b-modal.modal-1 > Setting </b-button>
  <b-modal @ok="handleOK(server,version,cntry,language)" id="modal-1" title="Setting" >
    <b-form-group style = font-size:15px; label="Server" >
      <b-form-select style = font-size:15px; 
          v-model="form.server" :options="servers" ></b-form-select>
              {{form.server}}

    </b-form-group>
    <b-form-group style = font-size:15px; label="Version" >
      <b-form-select style = font-size:15px; 
          v-model="form.version" :options="versions" ></b-form-select>
          {{form.version}}
    </b-form-group>
    <p>cntry</p>
    <input v-model="form.cntry" placeholder="입력해주세요."> {{form.cntry}}
    <b-form-group style = font-size:15px; label="Language" >
      <b-form-select style = font-size:15px; 
          v-model="form.language" :options="languages" ></b-form-select>
          {{form.language}}
    </b-form-group>
    <p class="my-4">fck : {{fck}}</p>
  </b-modal>

  </b-navbar>
</template>

<script>
import {mapState} from 'vuex';

  export default {
    data() {
      return {
        servers: [
          'pd',
          'qt2'
        ],
        versions : [
          'v11',
          'v12'
        ],
        form : {
          server : '',
          cntry : '',
          language : '',
          version : ''
        }
      
      }
    },
      
  created() { 
    this.form.server = this.$store.state.server;
    this.form.version = this.$store.state.version;
    this.form.cntry = this.$store.state.cntry;
    this.form.language = this.$store.state.language;
  }, 
  
  computed : mapState([
    'languages',
    'fck'
  ]),

  methods : {
    handleOK : function() {
      this.$store.commit('setSettingValue',this.form);
    },
  }
}
</script>

<style scoped>
.setting {
  display : inline-block;
  float : right;
}
</style>
