<template>
  <top-nav></top-nav>
  <side-nav></side-nav>
  <br>
  <Scatter :plotData="$store.getters.plotData" />
  <Distribution/>
  <Network :network="$store.getters.network"/>
  <LevelScatter :plotData="$store.getters.plotData" />
</template>

<script>
import {defineProps} from 'vue'
import {updateResources} from "../services/datasource";
import Scatter from "./views/Scatter.vue"
import Network from "./views/Network.vue"
import SideNav from "./menu/SideNav.vue";
import TopNav from "./menu/TopNav.vue";
import Distribution from "./views/Distribution.vue";
import LevelScatter from "./views/LevelScatter.vue";

defineProps({
  msg: String
})

export default {
  name: "Dashboard",
  components: {
    Distribution,
    TopNav,
    Scatter,
    Network,
    SideNav,
    LevelScatter
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
  float: left;
  width: 600px;
  height: 460px;
  border: 1px solid darkslategrey;
  margin-bottom: 10px;
}

#spinner {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 50%;
}

</style>
