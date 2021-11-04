<template>
  <div id="alpha_pane">
    <div id="spinner" v-if="$store.getters.loadingNetwork">
      <ScaleLoader v-if="$store.getters.loadingNetwork"></ScaleLoader>
    </div>
  </div>
  <table>
    <tbody>
    <tr>
      <td>&lt;td></td>
      <td>&lt;td></td>
      <td>&lt;td></td>
    </tr>
    <tr>
      <td>&lt;td></td>
      <td>&lt;td></td>
      <td>&lt;td></td>
    </tr>
    <tr>
      <td>&lt;td></td>
      <td>&lt;td></td>
      <td>&lt;td></td>
    </tr>
    </tbody>
  </table>
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
table {
  width: 100%;
  height: 100%;
}
</style>
