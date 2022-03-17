<template>
  <ViewHeader id="header" class="header" :title='"Density Navigation - Use zooming and panning to navigate"' :branch="true" :trash="true"
              :trash-callback="trashCallback" :alpha="true" :exclude="true" :include="true" :noise="true"
              :inspect="true" :disease="true" :draw-polygon="true"></ViewHeader>
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
           :max-x="$store.getters.networkData.max_x" :clusterLabel="$store.getters.currentCluster.label"/>
  </div>
</template>

<script>
import {views} from "../../services/views";
import Space from "../views/Space.vue";
import Velocity from "../views/Velocity.vue";
import DensityExplorer from "../views/DensityExplorer.vue";
import ViewHeader from "../nav/ViewHeader.vue";
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
    ViewHeader
  },
  mounted() {
    updateResources();
    getSignificantRoots();
  },
}
</script>


<style lang="css" scoped>
#header {
  order: 0
}

#space {
  order: 1
}

#velocity {
  order: 2;
}

#network {
  order: 3;
}

#alpha {
  order: 4;
}

.space {
  position: relative;
  float: left;
  width: 50%;
  height: 300px;
  border: 1px solid darkslategrey;
  margin-bottom: 5px;
  margin-right: 5px;
}

.velocity {
  position: relative;
  float: left;
  width: 49%;
  height: 300px;
  border: 1px solid darkslategrey;
  margin-bottom: 5px;
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