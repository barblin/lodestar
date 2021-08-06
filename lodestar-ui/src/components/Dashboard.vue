<template>
  <top-nav></top-nav>
  <side-nav></side-nav>
  <br>
  <Scatter :plotData="$store.getters.plotData" />
  <Network :network="$store.getters.network" />
</template>

<script>
import {defineProps} from 'vue'
import {updateResources, updateScatter, updateNetwork} from "../services/datasource";
import Scatter from "./views/Scatter.vue"
import Network from "./views/Network.vue"
import SideNav from "./menu/SideNav.vue";
import TopNav from "./menu/TopNav.vue";

defineProps({
  msg: String
})

export default {
  name: "Dashboard",
  components: {
    TopNav,
    Scatter,
    Network,
    SideNav
  },
  mounted() {
    updateResources();
  }
}
</script>

<style>
a {
  color: #42b983;
}

.simple-plot {
  position: relative;
  float:left;
  width: 600px;
  height: 470px;
  border:1px solid darkslategrey;
}

#spinner {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 50%;
}

</style>
