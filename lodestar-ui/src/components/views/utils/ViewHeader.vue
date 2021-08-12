<template>
  <div id="view-header" class="view-header">
    <span class="view-header-title">{{ title }}</span>
  </div>
</template>

<script>


export default {
  name: "Header",
  props: ['title'],
  components: {},
}

</script>

<style scoped>
.view-header {
  background-color: #d5e7c9;
}

.view-header-title {
  font-size: 12px;
  margin-left: 5px;
}
</style>