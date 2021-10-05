<template>
  <button type="button" :disabled="$store.getters.loadingAny" @click="click()" class="nav-el">Plot</button>
  <button type="button" @click="changeViewCluster()" class="nav-el">Change to Cluster</button>
  <button type="button" @click="changeViewAlpha()" class="nav-el">Change to Alpha</button>
  <button type="button" @click="changeViewBack()" class="nav-el">Change back</button>
</template>

<script>
import {updateNetwork, updateScatter, updateSpace, updateVelocityScatter, updateVelocityNet} from "../../services/datasource";
import {modes} from "../../services/modes";

export default {
  name: "Plotter",
  methods: {
    click() {
      updateScatter(this.$store.getters.currentResource);
      updateNetwork(this.$store.getters.currentResource);
      updateSpace();
      updateVelocityScatter();
      updateVelocityNet()
    },
    changeViewCluster() {
      this.$store.commit('updateCurrentMode', modes.CLUSTER)
    },
    changeViewAlpha() {
      this.$store.commit('updateCurrentMode', modes.ALPHA)
    },
    changeViewBack() {
      this.$store.commit('updateCurrentMode', modes.DEFAULT)
    }
  }
}
</script>

<style scoped>
</style>