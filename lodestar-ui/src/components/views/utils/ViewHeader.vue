<template>
  <div id="view-header" class="view-header">
    <span class="view-header-title">{{ title }}</span>
    <span class="toolbar">
      <font-awesome-icon class="tool" v-if="trash" v-on:click="trashCallback" icon="trash"/>
      <font-awesome-icon class="tool" v-if="branch" icon="level-down-alt"/>
    </span>
  </div>
</template>

<script>


export default {
  name: "Header",
  props: ['title', 'trash', 'branch', 'trashCallback'],
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

.toolbar {
  float: right;
  opacity: 0.5;
}

.tool {
  margin-right: 5px;
  margin-top: 4px;
  border: solid gray 1px;
}
</style>