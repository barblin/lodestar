<template>
  <ViewHeader class="header" :title='""'
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
  <div v-if="!$store.getters.erroredHrd" :id="views.HRD" class="hrd">
    <HRD :plotData="$store.getters.hrd" :color-labels="$store.getters.colorLabels" :parent="views.HRD"
         :highlight="$store.getters.highlightCluster"/>
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
import {updateCurrentLabels} from "../../services/datasource";

export default {
  name: "ModeLevelSet",
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
    updateCurrentLabels({
      level: this.$store.getters.level,
      alpha: this.$store.getters.alpha
    })
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
  width: 40%;
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
  width: 25%;
  height: 300px;
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