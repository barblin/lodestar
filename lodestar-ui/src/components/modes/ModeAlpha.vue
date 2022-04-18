<template>
  <ViewHeader id="header" class="header" :title='"Density Navigation - Use zooming and panning to navigate"'
              :branch="true" :trash="true"
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
  <div :id="views.HRD" class="hrd">
    <HRD :parent="views.HRD" :plotData="$store.getters.hrd" :selections="$store.getters.resourceHeaders"
         :color-labels="$store.getters.colorLabels"/>
  </div>
  <div :id="views.NETWORK" v-if="!$store.getters.loadingMain" class="network">
    <DensityExplorer :networkData="$store.getters.networkData" :parent="views.NETWORK"
                     :labels="$store.getters.labels"/>
  </div>
  <div :id="views.ALPHA" class="alpha">
    <Alpha :parent="views.ALPHA" :significantRoots="$store.getters.significantRoots"
           :clusterLabel="$store.getters.currentCluster.label"
           :labels="$store.getters.labels"
           :allLabels="$store.getters.allLabels"/>
  </div>
  <div :id="views.HEAT_MAP" class="heat-map">
    <HeatMap :parent="views.HEAT_MAP" :heatmap="$store.getters.heatmap" :level="$store.getters.level"
             :alpha="$store.getters.alpha"/>
  </div>
  <div :id="views.STABILITY" class="stability">
    <Stability :parent="views.STABILITY" :heatmap="$store.getters.heatmap" :level="$store.getters.level"
               :alpha="$store.getters.alpha"/>
  </div>
</template>

<script>
import {views} from "../../services/views";
import Space from "../views/Space.vue";
import Velocity from "../views/Velocity.vue";
import DensityExplorer from "../views/DensityExplorer.vue";
import ViewHeader from "../nav/ViewHeader.vue";
import Alpha from "../views/alpha/Alpha.vue";
import HeatMap from "../views/alpha/HeatMap.vue";
import Stability from "../views/alpha/Stability.vue";
import {updateCurrentLabels, updateResourceHeaders, updateResources} from "../../services/datasource";
import HRD from "../views/detail/HRD.vue";

export default {
  name: "ModeAlpha",
  data() {
    return {
      updateKeys: {},
      views: views,
    };
  },
  components: {
    Space,
    Velocity,
    HRD,
    DensityExplorer,
    Alpha,
    HeatMap,
    Stability,
    ViewHeader
  },
  mounted() {
    updateResources();
    updateCurrentLabels({
      level: this.$store.getters.level,
      alpha: this.$store.getters.alpha
    })
    updateResourceHeaders(this.$store.getters.currentResource);
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

#hrd {
  order: 3;
}

#network {
  order: 4;
}

#alpha {
  order: 5;
}

#heat_map {
  order: 6;
}

#stability {
  order: 7;
}

.space {
  position: relative;
  float: left;
  width: 45%;
  height: 300px;
  border: 1px solid darkslategrey;
  margin-bottom: 5px;
  margin-right: 5px;
}

.velocity {
  position: relative;
  float: left;
  width: 35%;
  height: 300px;
  border: 1px solid darkslategrey;
  margin-bottom: 5px;
  margin-right: 5px;
}

.hrd {
  position: relative;
  float: left;
  width: 18%;
  height: 300px;
  border: 1px solid darkslategrey;
  margin-bottom: 5px;
}


.network {
  position: relative;
  float: left;
  width: 70%;
  height: 350px;
  border: 1px solid darkslategrey;
}

.alpha {
  position: relative;
  float: left;
  width: 29%;
  height: 350px;
  margin-left: 5px;
  border-top: 1px solid darkgrey;
  border-right: 1px solid darkslategrey;
  border-bottom: 1px solid darkslategrey;
  border-left: 1px solid darkslategrey;
}

.heat-map {
  position: relative;
  float: left;
  width: 70%;
  height: 250px;
  margin-top: 5px;
}

.stability {
  position: relative;
  float: right;
  width: 29%;
  height: 250px;
  margin-top: 5px;
  margin-left: 5px;
  border-top: 1px solid darkgrey;
  border-right: 1px solid darkslategrey;
  border-bottom: 1px solid darkslategrey;
  border-left: 1px solid darkslategrey;
}
</style>