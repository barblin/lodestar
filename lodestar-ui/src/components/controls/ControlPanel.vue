<template>
  <div v-if="$store.getters.currentMode != modes.CLUSTER">
    <ResourceSelector :selection="$store.getters.currentResource" :headerSelection="$store.getters.resourceHeaders[0]">
    </ResourceSelector>
    <div class="calculate">
      <button type="button" class="calculate" :disabled="$store.getters.loadingAny || !includeSecondVelocityDimension()"
              @click="click()">
        Calculate (May take up to 20 min)
      </button>
    </div>
  </div>
</template>

<script>
import {updateHrd, updateNetwork, updateSpace, updateVelocity} from "../../services/datasource";
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
  position: absolute;
  width: 97%;
  height: 50px;
  top: 87%;
}
</style>