<template>
  <div :id="views.SPACE" class="space">
    <Space :parent="views.SPACE" :drawScatter="$store.getters.drawSpaceScatter"
           :drawNet="$store.getters.drawSpaceNet"
           :spaceData="$store.getters.spaceData"/>
  </div>
  <div :id="views.VELOCITY" class="velocity">
    <Velocity :parent="views.VELOCITY"
              :drawScatter="$store.getters.drawVelocityScatter"
              :drawNet="$store.getters.drawVelocityNet"
              :netData="$store.getters.velocityNetworkData"
              :scatData="$store.getters.velocityScatterData"/>
  </div>
  <div :id="views.NETWORK" v-if="!$store.getters.loadingNetwork" class="network">
    <DensityExplorer :networkData="$store.getters.networkData" :parent="views.NETWORK"/>
  </div>
</template>

<script>
import {views} from "../../services/views";
import Space from "../views/Space.vue";
import Velocity from "../views/Velocity.vue";
import DensityExplorer from "../views/DensityExplorer.vue";
import {updateResources} from "../../services/datasource";

export default {
  name: "ModeDefault",
  data() {
    return {
      views: views,
    };
  },
  components: {
    Space,
    Velocity,
    DensityExplorer,
  },
  mounted() {
    updateResources();
  },
}
</script>


<style lang="css" scoped>
#space {
  order: 0
}

#velocity {
  order: 1;
}

#network {
  order: 2;
}

.space {
  position: relative;
  float: left;
  width: 50%;
  height: 600px;
  border: 1px solid darkslategrey;
  margin-bottom: 10px;
  margin-right: 5px;
}

.velocity {
  position: relative;
  float: left;
  width: 40%;
  height: 460px;
  border: 1px solid darkslategrey;
  margin-bottom: 10px;
}

.network {
  position: relative;
  float: left;
  width: 100%;
  height: 300px;
  border: 1px solid darkslategrey;
  margin-bottom: 10px;
}

</style>