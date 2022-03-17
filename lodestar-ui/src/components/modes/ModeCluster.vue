<template>
  <ViewHeader class="header" :title='"Density Navigation - Use zooming and panning to navigate"' :branch="true" :trash="true"
              :trash-callback="trashCallback" :alpha="true" :exclude="true" :include="true" :noise="true"
              :inspect="true" :disease="true" :draw-polygon="true"></ViewHeader>
  <span class="details">
    <button type="button" class="save-exit" @click="exitClusterDetails()">Exit & Save Cluster</button>
    Name: <input v-model="cluster_name"
                 :placeholder="$store.getters.currentCluster.name">
  </span>
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
  <div :id="views.NETWORK" v-if="!$store.getters.loadingMain" class="network">
    <DensityExplorer :networkData="$store.getters.networkData" :parent="views.NETWORK"
                     :labels="$store.getters.labels" :filter-for-cluster="true"/>  </div>
  <div :id="views.CLUSTER_DETAIL" class="cluster_detail">
    <ClusterDetails :plotData="$store.getters.hrd" :selections="$store.getters.resourceHeaders"
                    :parent="views.CLUSTER_DETAIL"
                    :colorLabels="$store.getters.colorLabels"/>
  </div>
  <div :id="views.HISTOGRAMS" class="histograms">
    <Histogram :plotData="$store.getters.velocityScatterData" :parent="views.HISTOGRAMS"
               :labels="$store.getters.colorLabels"/>
  </div>
</template>

<script>
import {views} from "../../services/views";
import Space from "../views/Space.vue";
import Velocity from "../views/Velocity.vue";
import DensityExplorer from "../views/DensityExplorer.vue";
import ClusterDetails from "../views/cluster/ClusterDetails.vue";
import Histogram from "../views/detail/Histogram.vue";
import ViewHeader from "../nav/ViewHeader.vue";
import {updateCurrentCluster, updateResources} from "../../services/datasource";
import {modes} from "../../services/modes";
import {store} from "../../store/cluster-state-store";

export default {
  name: "ModeCluster",
  data() {
    return {
      updateKeys: {},
      views: views,
      cluster_name: ""
    };
  },
  components: {
    Space,
    Velocity,
    DensityExplorer,
    ClusterDetails,
    Histogram,
    ViewHeader
  },
  beforeUnmount() {
    let cluster = this.$store.getters.levelSet[this.$store.getters.currentCluster.level]
        [this.$store.getters.currentCluster.label]
    cluster.name = this.cluster_name
    this.$store.commit("addNode", cluster)
    this.$store.commit('updateCurrentClusterName', this.cluster_name)
    this.cluster_name = ""
  },
  methods: {
    exitClusterDetails() {
      let cluster = this.$store.getters.levelSet[this.$store.getters.currentCluster.level]
          [this.$store.getters.currentCluster.label]
      cluster.name = this.cluster_name
      this.$store.commit("addNode", cluster)
      this.$store.commit('updateCurrentClusterName', this.cluster_name)
      this.$store.commit('updateCurrentMode', modes.DEFAULT)
      updateCurrentCluster()
    }
  },

  mounted() {
    updateResources();
    store.commit('updateLoadingMain', false)
  },
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

#network {
  order: 2;
}

#cluster_detail {
  order: 3;
}

#histograms {
  order: 4;
}

.details {
  margin-top: -10px;
  display: block;
  width: 100%;
}

.space {
  position: relative;
  float: left;
  width: 50%;
  height: 460px;
  border: 1px solid darkslategrey;
  margin-bottom: 5px;
  margin-right: 5px;
}

.velocity {
  position: relative;
  float: left;
  width: 40%;
  height: 460px;
  border: 1px solid darkslategrey;
  margin-bottom: 5px;
}

.network {
  position: relative;
  float: left;
  width: 32%;
  height: 430px;
  border: 1px solid darkslategrey;
  margin-bottom: 5px;
  margin-right: 10px;
}

.cluster_detail {
  position: relative;
  float: left;
  width: 35%;
  height: 430px;
  border: 1px solid darkslategrey;
  margin-bottom: 5px;
  margin-right: 10px;
}

.histograms {
  position: relative;
  float: left;
  width: 30%;
  height: 430px;
  border: 1px solid darkslategrey;
}

.save-exit {
  margin-bottom: 0px;
  margin-top: 5px;
}
</style>