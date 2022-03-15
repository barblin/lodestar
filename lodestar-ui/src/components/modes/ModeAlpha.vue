<template>
  <div :id="views.SPACE" class="space">
    <Space :parent="views.SPACE" :drawScatter="$store.getters.drawSpaceScatter"
           :drawNet="$store.getters.drawSpaceNet"
           :magnify="$store.getters.inspectCluster"
           :spaceData="$store.getters.spaceData"
           :colorLabels="$store.getters.colorLabels"/>
  </div>
  <div :id="views.VELOCITY" class="velocity">
    <Velocity :parent="views.VELOCITY"
              :drawScatter="$store.getters.drawVelocityScatter"
              :drawNet="$store.getters.drawVelocityNet"
              :netData="$store.getters.velocityNetworkData"
              :scatData="$store.getters.velocityScatterData"
              :colorLabels="$store.getters.colorLabels"/>
  </div>
  <div :id="views.NETWORK" class="network">
    <DensityExplorer :networkData="$store.getters.networkData" :parent="views.NETWORK"
      :colorLabels="$store.getters.colorLabels"/>
  </div>
  <div :id="views.ALPHA" class="alpha">
    <Alpha :parent="views.ALPHA" :significantRoots="$store.getters.significantRoots"
           :max-x="$store.getters.networkData.max_x"/>
  </div>
</template>

<script>
import {views} from "../../services/views";
import Space from "../views/Space.vue";
import Velocity from "../views/Velocity.vue";
import DensityExplorer from "../views/DensityExplorer.vue";
import Alpha from "../views/alpha/Alpha.vue";
import {getSignificantRoots, updateResources} from "../../services/datasource";

export default {
  name: "ModeDefault",
  data() {
    return {
      updateKeys: {},
      views: views,
    };
  },
  components: {
    Space,
    Velocity,
    DensityExplorer,
    Alpha,
  },
  mounted() {
    updateResources();
    getSignificantRoots();
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

#alpha {
  order: 3;
}

.space {
  position: relative;
  float: left;
  width: 50%;
  height: 300px;
  border: 1px solid darkslategrey;
  margin-bottom: 10px;
  margin-right: 5px;
}

.velocity {
  position: relative;
  float: left;
  width: 49%;
  height: 300px;
  border: 1px solid darkslategrey;
  margin-bottom: 10px;
}

.network {
  position: relative;
  float: left;
  width: 98%;
  height: 450px;
  border: 1px solid darkslategrey;
}

.alpha {
  position: relative;
  float: left;
  width: 98%;
  height: 150px;
  border-top: 10px solid darkgrey;
  border-right: 1px solid darkslategrey;
  border-bottom: 1px solid darkslategrey;
  border-left: 1px solid darkslategrey;
}

</style>