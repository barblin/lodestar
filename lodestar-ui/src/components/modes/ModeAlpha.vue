<template>
  <ViewHeader id="header" class="header" :title='""'
              :branch="false" :trash="false"
              :trash-callback="trashCallback" :alpha="true" :exclude="false" :include="true" :noise="true"
              :inspect="true" :disease="false" :draw-polygon="false"></ViewHeader>
  <div :id="views.SPACE" class="space">
    <Space :parent="views.SPACE" :drawScatter="$store.getters.drawSpaceScatter"
           :magnify="$store.getters.inspectCluster"
           :spaceData="$store.getters.spaceData"
           :colorLabels="$store.getters.colorLabels"
           :highlight="$store.getters.highlightCluster"/>
  </div>
  <div :id="views.VELOCITY" class="velocity">
    <Velocity :parent="views.VELOCITY"
              :scatData="$store.getters.velocityScatterData"
              :colorLabels="$store.getters.colorLabels"
              :highlight="$store.getters.highlightCluster"/>
  </div>
  <div :id="views.HRD" class="hrd">
    <HRD :plotData="$store.getters.hrd" :color-labels="$store.getters.colorLabels" :parent="views.HRD"
         :highlight="$store.getters.highlightCluster"/>
  </div>
  <div :id="views.SELECTOR" class="selector">
    <Selector :plotData="$store.getters.selector" :selections="$store.getters.resourceHeaders" :parent="views.SELECTOR"
         :color-labels="$store.getters.colorLabels" :highlight="$store.getters.highlightCluster"/>
  </div>
  <div :id="views.NETWORK" v-if="!$store.getters.loadingMain" class="network">
    <DensityExplorer :networkData="$store.getters.networkData" :parent="views.NETWORK"
                     :labels="$store.getters.labels" :exclusion="$store.getters.selectExclude" />
  </div>
  <div :id="views.ALPHA" class="alpha">
    <Alpha :parent="views.ALPHA" :allLabels="$store.getters.allLabels"/>
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
import HRD from "../views/detail/HRD.vue";
import {updateCurrentLabels, updateResourceHeaders, updateResources} from "../../services/data/datasource";
import Selector from "../views/detail/Selector.vue";

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
    Selector,
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

#selector {
  order: 4;
}

#network {
  order: 5;
}

#alpha {
  order: 6;
}

#heat_map {
  order: 7;
}

#stability {
  order: 8;
}

.space {
  position: relative;
  float: left;
  width: 400px;
  height: 300px;
  border: 1px solid darkslategrey;
  margin-bottom: 5px;
  margin-right: 5px;
}

.velocity {
  position: relative;
  float: left;
  width: 375px;
  height: 300px;
  border: 1px solid darkslategrey;
  margin-bottom: 5px;
  margin-right: 5px;
}

.hrd {
  position: relative;
  float: left;
  width: 375px;
  height: 300px;
  margin-right: 5px;
  border: 1px solid darkslategrey;
  margin-bottom: 5px;
}

.selector {
  position: relative;
  float: left;
  width: 375px;
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
  margin-top: 8px;
  margin-left: -3px;
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