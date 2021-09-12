<template>
  <div id="view-header" class="view-header">
    <span class="view-header-title">{{ title }}</span>
    <span class="toolbar">
      <font-awesome-icon class="tool" v-if="trash" v-on:click="trashCallback" icon="trash"/>
      <font-awesome-icon class="tool" v-if="branch" icon="level-down-alt"/>
      <font-awesome-icon class="tool" v-if="parentSelected()" v-on:click="minimize" icon="compress-arrows-alt"/>
      <font-awesome-icon class="tool" v-else v-on:click="maximize" icon="expand-arrows-alt"/>
    </span>
  </div>
</template>

<script>


export default {
  name: "Header",
  props: ['title', 'trash', 'branch', 'trashCallback', 'selector', 'parent'],
  components: {},
  methods: {
    minimize() {
      this.$emit('maximize')
      this.$store.commit('updateCurrentViewSelection', null)
    },
    maximize() {
      this.$emit('maximize')
    },
    parentSelected() {
      console.log(this.parent)
      return this.parent == this.$store.getters.currentViewSelection
    }
  }
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