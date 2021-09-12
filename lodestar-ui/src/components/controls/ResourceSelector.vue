<template>
  <vue-select v-model="selection" placeholder="Select source file" :options="$store.getters.resources" class="nav-el"></vue-select>
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