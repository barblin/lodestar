<template>
  <ViewHeader class="header" :title='""'
              :branch="false" :trash="false"
              :trash-callback="trashCallback" :alpha="true" :exclude="false" :include="true" :noise="true"
              :inspect="true" :disease="false" :draw-polygon="false"></ViewHeader>
  <div :id="views.SPACE" class="space">
    <Space :parent="views.SPACE" :drawScatter="$store.getters.drawSpaceScatter"
           :magnify="$store.getters.inspectCluster"
           :spaceData="$store.getters.spaceData"
           :colorLabels="$store.getters.colorLabels"/>
  </div>
  <div :id="views.VELOCITY" class="velocity">
    <Velocity :parent="views.VELOCITY"
              :drawScatter="$store.getters.drawVelocityScatter"
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
import {updateResources} from "../../services/datasource";
import {store} from "../../store/cluster-state-store";

export default {
  name: "ModeCluster",
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
    ClusterDetails,
    Histogram,
    ViewHeader
  },
  methods: {
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
  width: 20%;
  height: 430px;
  border: 1px solid darkslategrey;
  margin-bottom: 5px;
  margin-right: 10px;
}

.cluster_detail {
  position: relative;
  float: left;
  width: 38%;
  height: 430px;
  border: 1px solid darkslategrey;
  margin-bottom: 5px;
  margin-right: 10px;
}

.histograms {
  position: relative;
  float: left;
  width: 38%;
  height: 430px;
  border: 1px solid darkslategrey;
}

.save-exit {
  margin-bottom: 0px;
  margin-top: 5px;
}
</style>