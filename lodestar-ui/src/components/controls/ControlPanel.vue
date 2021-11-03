<template>
  <div v-if="$store.getters.currentMode != modes.CLUSTER">
    <ResourceSelector :selection="$store.getters.currentResource" :headerSelection="$store.getters.resourceHeaders[0]">
    </ResourceSelector>
    <div class="calculate">
      <button type="button" :disabled="$store.getters.loadingAny || !includeSecondVelocityDimension()" @click="click()"
              class="calculate">Calculate
      </button>
    </div>
  </div>
  <div v-else>
    <button type="button" @click="exitClusterDetails()" class="nav-el">Exit cluster details</button>
  </div>
</template>

<script>
import {updateHrd, updateNetwork, updateSpace, updateVelocityScatter} from "../../services/datasource";
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
      this.$store.commit('updateCurrentMode', modes.DEFAULT)
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

.calculate {
  font-size: large;
  position: absolute;
  width: 97%;
  height: 50px;
  top: 87%;
}
</style>