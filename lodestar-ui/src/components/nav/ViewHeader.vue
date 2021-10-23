<template>
  <div id="view-header" class="view-header">
    <span class="view-header-title">{{ title }}</span>
    <span class="toolbar">
      <div class="tooltip">
        <div class="tooltip">
        <font-awesome-icon class="tool select-red" v-if="exclude" v-on:click="exclusiveSelect" icon="vector-square"/>
        <span class="tooltiptext">Inclusive select clusters</span>
      </div>
      <div class="tooltip">
        <font-awesome-icon class="tool select-green" v-if="include" v-on:click="inclusiveSelect" icon="vector-square"/>
        <span class="tooltiptext">Exclude select clusters</span>
      </div>
        <font-awesome-icon class="tool" v-if="trash" v-on:click="trashCallback" icon="trash"/>
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
      <div class="tooltip">
        <font-awesome-icon class="tool" v-if="inspect" v-on:click="inspectCluster" icon="search-plus"/>
        <span class="tooltiptext">Inspect cluster</span>
      </div>
      <div class="tooltip">
        <div class="fa-alpha" v-if="alpha" v-on:click="inspectJoins"
             v-bind:class="{ 'strike-through': isModeAlpha() }"/>
        <span v-if="!isModeAlpha()" class="tooltiptext">Open change alpha value</span>
        <span v-else class="tooltiptext">Close change alpha value</span>
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

import {modes} from "../../services/modes";

export default {
  name: "Header",
  props: ['title', 'trash', 'branch', 'trashCallback', 'selector', 'parent', 'drawPolygon', 'disease', 'inspect', 'alpha',
    'include', 'exclude'],
  components: {},
  methods: {
    updateNet() {
      this.$emit('updateNet')
      this.$store.commit('updateInspectCluster', !this.$store.getters.inspectCluster)
    },
    updateScatter() {
      this.$emit('updateScatter')
      this.$store.commit('updateInspectCluster', !this.$store.getters.inspectCluster)
    },
    inspectCluster() {
      this.$store.commit('updateInspectCluster', !this.$store.getters.inspectCluster)
    },
    inspectJoins() {
      if (this.isModeAlpha()) {
        this.$store.commit('updateCurrentMode', modes.DEFAULT)
      } else {
        this.$store.commit('updateCurrentMode', modes.ALPHA)
      }
    },
    isModeAlpha() {
      return this.$store.getters.currentMode == modes.ALPHA;
    },
    inclusiveSelect() {
      this.$store.commit('updateSelectInclude', true)
    },
    exclusiveSelect() {
      this.$store.commit('updateSelectInclude', false)
    },
  }
}

</script>

<style scoped>

.fa-alpha:before {
  font-weight: 900;
  font-size: 21px;
  color: black;
  content: 'α';
  margin-right: 5px;
  line-height: 5px;
  padding-left: 3px;
  padding-right: 3px;
  opacity: 0.5;
  cursor: pointer;
}

.strike-through {
  text-decoration: line-through;
}


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

.select-red {
  background-color: red;
}

.select-green {
  background-color: green;
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