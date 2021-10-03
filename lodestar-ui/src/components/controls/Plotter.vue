<template>
  <button type="button" :disabled="$store.getters.loadingAny" @click="click()" class="nav-el">Plot</button>
</template>

<script>
import {updateNetwork, updateScatter, updateSpace, updateVelocityScatter, updateVelocityNet} from "../../services/datasource";

export default {
  name: "Plotter",
  methods: {
    click() {
      updateScatter(this.$store.getters.currentResource);
      updateNetwork(this.$store.getters.currentResource);
      updateSpace();
      updateVelocityScatter();
      updateVelocityNet()
    }
  }
}
</script>

<style scoped>
</style>