<template>
<div>
  <b-modal id="modal-1" title="Setting">
    <b-form-group style = font-size:15px; label="Server" >
      <b-form-select style = font-size:15px; 
          v-model="server" :options="servers" 
          @change='changeServer'></b-form-select>
    </b-form-group>
    <b-form-group style = font-size:15px; label="Version" >
      <b-form-select style = font-size:15px; 
          v-model="version" :options="versions" 
          @change='changeVersion'></b-form-select>
    </b-form-group>
    <p class="my-4">cntry : </p>
    <p class="my-4">language : {{language}}</p>
    <p class="my-4">fck : {{fck}}</p>
  </b-modal>
</div>
</template>

<script>

export default {


}
</script>

<style scoped>

</style>
