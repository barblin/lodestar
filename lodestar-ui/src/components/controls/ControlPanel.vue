<template>
  <div v-if="$store.getters.currentMode != modes.CLUSTER">
    <ResourceSelector :selection="$store.getters.currentResource" :headerSelection="$store.getters.resourceHeaders[0]">
    </ResourceSelector>
    <!--<button type="button" @click="changeViewCluster()" class="nav-el">Change to Cluster</button>
    <button type="button" @click="changeViewAlpha()" class="nav-el">Change to Alpha</button>
    <button type="button" @click="changeViewBack()" class="nav-el">Change back</button>-->
    <button type="button" :disabled="$store.getters.loadingAny || !includeSecondVelocityDimension()" @click="click()"
            class="nav-el">Plot
    </button>
  </div>
  <div v-else>
    <button type="button" @click="exitClusterDetails()" class="nav-el">Exit cluster details</button>
  </div>
</template>

<script>
import {
  updateHrd,
  updateNetwork,
  updateSpace,
  updateVelocityScatter
} from "../../services/datasource";
import {modes} from "../../services/modes";
import ResourceSelector from "./ResourceSelector.vue";
import {includeSecondVelocityDimension} from '../../services/dimension-util';

export default {
  name: "Plotter",
  components: {
    ResourceSelector: ResourceSelector
  },
  data: function () {
    return {
      modes: modes
    }
  },
  methods: {
    click() {
      updateNetwork(this.$store.getters.currentResource);
      updateSpace(this.$store.getters.currentResource);
      updateVelocityScatter(this.$store.getters.currentResource);
      updateHrd(this.$store.getters.currentResource);
    },
    includeSecondVelocityDimension() {
      return includeSecondVelocityDimension()
    },
    exitClusterDetails() {
      this.$store.commit('updateCurrentMode', modes.DEFAULT)
    }
  }
}
</script>

<style scoped>
</style>