<template>
  <ViewHeader class="header" :title='"Density Navigation - Use zooming and panning to navigate"' :branch="true" :trash="true"
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
</template>

<script>
import {views} from "../../services/views";
import Space from "../views/Space.vue";
import Velocity from "../views/Velocity.vue";
import ViewHeader from "../nav/ViewHeader.vue";
import HRD from "../views/detail/HRD.vue";
import DensityExplorer from "../views/DensityExplorer.vue";
import {getAllTrees, updateResourceHeaders} from "../../services/datasource";

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
    HRD,
    ViewHeader,
  },
  mounted() {
    updateResourceHeaders(this.$store.getters.currentResource)
    getAllTrees()
  }
}
</script>


<style lang="css" scoped>
#header {
  order: -1
}

#space {
  order: 0
}

#velocity {
  order: 1;
}

#hrd {
  order: 2;
}

#network {
  order: 3;
}

.space {
  position: relative;
  float: left;
  width: 50%;
  height: 480px;
  border: 1px solid darkslategrey;
  margin-bottom: 5px;
  margin-right: 5px;
}

.velocity {
  position: relative;
  margin-right: 5px;
  float: left;
  width: 30%;
  height: 480px;
  border: 1px solid darkslategrey;
  margin-bottom: 5px;
}


.hrd {
  position: relative;
  float: left;
  width: 17%;
  height: 480px;
  border: 1px solid darkslategrey;
  margin-bottom: 5px;
}

.network {
  position: relative;
  float: left;
  width: 98%;
  height: 430px;
  border: 1px solid darkslategrey;
  margin-bottom: 5px;
}

</style>