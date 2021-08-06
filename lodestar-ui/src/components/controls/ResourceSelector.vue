<template>
  <vue-select v-model="selection"  :options="$store.getters.resources" class="nav-el"></vue-select>
</template>

<script>

export default {
  name: "ResourceSelector",
  props: ['selection'],
  watch: {
    selection: function (selection) {
      this.$store.commit('updateCurrentResource', selection)
    }
  }
}
</script>

<style scoped>

</style>