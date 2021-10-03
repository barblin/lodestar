<template>
  <div id="view-header" class="view-header">
    <span class="view-header-title">{{ title }}</span>
    <span class="toolbar">
      <div class="tooltip">
        <font-awesome-icon class="tool tooltip" v-if="trash" v-on:click="trashCallback" icon="trash"/>
        <span class="tooltiptext">Clear current selection</span>
      </div>
      <div class="tooltip">
        <font-awesome-icon class="tool" v-if="branch" icon="level-down-alt"/>
        <span class="tooltiptext">Select subtree</span>
      </div>
      <div class="tooltip">
        <font-awesome-icon class="tool" v-if="disease" v-on:click="updateScatter" icon="disease"/>
        <span class="tooltiptext">Enable/Disable cluster</span>
      </div>
      <div class="tooltip">
        <font-awesome-icon class="tool" v-if="drawPolygon" v-on:click="updateNet" icon="draw-polygon"/>
        <span class="tooltiptext">Enable/Disable network</span>
      </div>
      <!--
      <div class="tooltip">
        <font-awesome-icon class="tool" v-if="parentSelected()" v-on:click="minimize" icon="compress-arrows-alt"/>
        <font-awesome-icon class="tool" v-else v-on:click="maximize" icon="expand-arrows-alt"/>
        <span class="tooltiptext">Resize</span>
      </div>
      -->
    </span>
  </div>
</template>

<script>

export default {
  name: "Header",
  props: ['title', 'trash', 'branch', 'trashCallback', 'selector', 'parent', 'drawPolygon', 'disease'],
  components: {},
  methods: {
    updateNet() {
      this.$emit('updateNet')
    },
    updateScatter() {
      this.$emit('updateScatter')
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
  opacity: 1;
  color: black;
}

.tool {
  margin-right: 5px;
  margin-top: 4px;
  border: solid gray 1px;
  cursor: pointer;
  opacity: 0.5;
}

.tool:active {
  background-color: yellow;
}

/* Tooltip container */
.tooltip {
  position: relative;
  display: inline-block;
}

/* Tooltip text */
.tooltip .tooltiptext {
  bottom: 30px;
  right: 0px;
  visibility: hidden;
  width: 200px;
  background-color: gray;
  color: #fff;
  text-align: center;
  padding: 5px 0;
  border-radius: 6px;
  font-size: 12px;

  /* Position the tooltip text - see examples below! */
  position: absolute;
  z-index: 1;
}

/* Show the tooltip text when you mouse over the tooltip container */
.tooltip:hover .tooltiptext {
  visibility: visible;
}
</style>