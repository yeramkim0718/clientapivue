<template>
<div>
<app-header style = hegiht:50px;></app-header>
<div>
    <sidebar class = "sidebar" ></sidebar>

    <searchbar class = "search"></searchbar>
    <div  class = "container"> 

        <scroll class = "image" >  
          <app-image></app-image>
        </scroll>
        <span style = "width:100px"></span>
        <div>
            <request ></request>
            <div style = "height:30px"></div>
            <item ></item>
        </div>

    </div>
</div>
</div>
</template>

<script>
import Sidebar from './components/Sidebar.vue'
import Searchbar from './components/Searchbar.vue'
import Header from './components/Header.vue'
import Request from './components/Request.vue'
import Item from './components/Item.vue'
import Image from './components/Image.vue'


export default {
    data () {
        return {
        }
    },
components : {
    'searchbar' : Searchbar,
    'sidebar' : Sidebar,
    'app-header' : Header,
    'request' : Request,
    'item' : Item,
    'app-image' : Image,
    
},
 methods : {

 }
}
</script>

<style scoped>

.search {
    display : block;
    margin:0 auto;
    padding-top:30px;
    z-index:1;

}

.sidebar {
    background-color:grey; 
    position:fixed; 
    float:left; 
    z-index:1; 
    display:block;  
    transition: 0.5s;
}

.container {
    display:flex;
    width:100%; 
    height:700px; 
    padding:30px; 
    z-index:2;
}


.image {
    width:600px; 
    padding:10px;
    float:right;
    overflow: scroll;
    border:1px solid grey;
}

.r {
    position: absolute;
    left: 0;
    top: 60px;
    width: 100%;
    height: 156px;
    overflow-y: auto;
}

</style>