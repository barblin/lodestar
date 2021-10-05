<template>
  <div id="alpha_pane">
    <div id="spinner" v-if="$store.getters.loadingNetwork">
      <ScaleLoader v-if="$store.getters.loadingNetwork"></ScaleLoader>
    </div>
  </div>
</template>

<script>
import ScaleLoader from 'vue-spinner/src/ScaleLoader.vue'

export default {
  name: "Alpha",
  props: ['parent'],
  components: {
    ScaleLoader
  },
  watch: {},
  methods: {}
}


</script>

<style scoped>
</style>
