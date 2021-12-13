<template>
  <span class="details">Cluster: {{ label }}, Name: {{ name }}, Size: {{ size }}, Level: {{ level }}
    <button type="button" class="save-exit" @click="exitClusterDetails()">Exit cluster details</button>
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
  <div :id="views.NETWORK" v-if="!$store.getters.loadingNetwork" class="network">
    <DensityExplorer :networkData="$store.getters.networkData" :parent="views.NETWORK"/>
  </div>
  <div :id="views.CLUSTER_DETAIL" class="cluster_detail">
    <ClusterDetails :networkData="$store.getters.drawScatter" :parent="views.NETWORK"/>
  </div>
  <div :id="views.HISTOGRAMS" class="histograms">
    <Histogram :plotData="$store.getters.velocityScatterData" :parent="views.HISTOGRAMS"/>
  </div>
</template>

<script>
import {views} from "../../services/views";
import Space from "../views/Space.vue";
import Velocity from "../views/Velocity.vue";
import DensityExplorer from "../views/DensityExplorer.vue";
import ClusterDetails from "../views/cluster/ClusterDetails.vue";
import Histogram from "../views/detail/Histogram.vue";
import {updateCurrentLabels, updateResources} from "../../services/datasource";
import {modes} from "../../services/modes";

export default {
  name: "ModeCluster",
  data() {
    return {
      updateKeys: {},
      label: this.$store.getters.currentCluster.label,
      name: this.$store.getters.currentCluster.name,
      size: this.$store.getters.currentCluster.size,
      level: this.$store.getters.currentCluster.level,
      views: views
    };
  },
  components: {
    Space,
    Velocity,
    DensityExplorer,
    ClusterDetails,
    Histogram
  },
  methods: {
    exitClusterDetails() {
      this.$store.commit('updateCurrentMode', modes.DEFAULT)
      updateCurrentLabels(this.$store.getters.currentResource, {level: this.$store.getters.level})
    }
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
  width: 32%;
  height: 430px;
  border: 1px solid darkslategrey;
  margin-bottom: 10px;
  margin-right: 10px;
}

.cluster_detail {
  position: relative;
  float: left;
  width: 35%;
  height: 430px;
  border: 1px solid darkslategrey;
  margin-bottom: 10px;
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
  margin-bottom: 5px;
}
</style>