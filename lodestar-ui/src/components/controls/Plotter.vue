<template>
  <button type="button" :disabled="$store.getters.loadingAny" @click="click()" class="nav-el">Plot</button>
</template>

<script>
import {updateNetwork, updateScatter, updateLevelScatter} from "../../services/datasource";

export default {
  name: "Plotter",
  methods: {
    click() {
      updateScatter(this.$store.getters.currentResource);
      updateNetwork(this.$store.getters.currentResource);
      updateLevelScatter(this.$store.getters.currentResource);
    }
  }
}
</script>

<style scoped>
</style>