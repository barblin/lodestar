<template>
  <div v-if="$store.getters.currentMode != modes.CLUSTER">
    <ResourceSelector :selection="$store.getters.currentResource" :headerSelection="$store.getters.resourceHeaders[0]">
    </ResourceSelector>
    <div class="calculate">
      <button type="button" class="calculate" :disabled="$store.getters.loadingAny || !includeSecondVelocityDimension()"
              @click="click()">
        Run (May take up to 2 hours)
      </button>
    </div>
    <div>
      <button type="button" class="help" :disabled="$store.getters.loadingAny"
              @click="goToTutorial()">
        Need help to get started?
      </button>
    </div>
  </div>
</template>

<script>
import {updateHrd, updateNetwork, updateSelection, updateSpace, updateVelocity} from "../../services/datasource";
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
      updateVelocity(this.$store.getters.currentResource);
      updateHrd(this.$store.getters.currentResource);
      updateSelection(this.$store.getters.currentResource);
    },
    goToTutorial() {
      this.$router.push('/tutorial')
    },
    includeSecondVelocityDimension() {
      return includeSecondVelocityDimension()
    },
  }
}
</script>

<style scoped>

.calculate {
  font-size: large;
  width: 500px;
  height: 50px;
  bottom: 50px;
  float:left;
  position: fixed;
  bottom: 50px;

}

.help {
  font-size: large;
  position: fixed;
  float: right;
  width: 300px;
  height: 50px;
  bottom: 50px;
  left: 800px;
}
</style>