<template>
  <ResourceSelector :selection="$store.getters.resources[0]"></ResourceSelector>
  <Plotter></Plotter>
</template>

<script>
import ResourceSelector from '../controls/ResourceSelector.vue'
import Plotter from "../controls/Plotter.vue";

export default {
  name: "TopNav",
  components: {
    ResourceSelector,
    Plotter
  }
}
</script>

<style>
.nav-el {
  float: left;
  margin-right: 5px;
}
</style>