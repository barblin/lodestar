<template>
  <div id="view-header" class="view-header">
    <span class="view-header-title">{{ title }}</span>
    <span class="toolbar">
      <div class="tooltip">
        <font-awesome-icon class="tool select-red" v-if="exclude" v-on:click="exclusiveSelect" icon="vector-square"/>
        <span class="tooltiptext">Exclude selected clusters</span>
      </div>
      <!--<div class="tooltip">
        <font-awesome-icon class="tool select-green" v-if="include" v-on:click="inclusiveSelect" icon="vector-square"/>
        <span class="tooltiptext">Exclude select clusters</span>
      </div>-->
      <div class="tooltip">
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
      <!--<div class="tooltip">
        <div class="fa-alpha" v-if="alpha" v-on:click="inspectJoins"
             v-bind:class="{ 'strike-through': isModeAlpha() }"/>
        <span v-if="!isModeAlpha()" class="tooltiptext">Open change alpha value</span>
        <span v-else class="tooltiptext">Close change alpha value</span>
      </div>-->
      <div class="tooltip">
        <font-awesome-icon class="tool" v-if="noise" v-on:click="toggleNoise" icon="braille"/>
        <span class="tooltiptext">Toogle noise</span>
      </div>
      <!--
      <div class="tooltip">
        <font-awesome-icon class="tool" v-if="parentSelected()" v-on:click="minimize" icon="compress-arrows-alt"/>
        <font-awesome-icon class="tool" v-else v-on:click="maximize" icon="expand-arrows-alt"/>
        <span class="tooltiptext">Resize</span>
      </div>
      -->
    </span>
    <span class="nav-bar">
      <div class="tooltip-nav-bar">
        <font-awesome-icon class="check" v-if="isModeLevelSet()" v-on:click="goBack" icon="backward"/>
        <span class="tooltiptext">Go back to alpha and density selection</span>
      </div>
      <div class="tooltip-nav-bar">
        <font-awesome-icon class="check" v-if="isModeCluster()"
                           v-on:click="exitAndSaveClusterDetails" icon="backward"/>
        <span class="tooltiptext">Go back to previous view</span>
      </div>
      <div class="tooltip-nav-bar">
        <font-awesome-icon class="check" v-if="isModeAlpha()"
                           v-on:click="continueWithSelection" icon="forward"/>
        <span class="tooltiptext">Continue with current alpha and density selection</span>
      </div>
      <div class="tooltip-nav-bar" v-if="$store.getters.level != null && !isModeCluster()">
        <a :href="'http://localhost:5000/api/v1/exports/' + $store.getters.currentResource + '?level='
        + $store.getters.level + '&alpha=' + $store.getters.alpha"
           :download="$store.getters.currentResource + '_labeled.csv'"
        >
          <font-awesome-icon class="export" icon="file-export"/>
        </a>
        <span class="tooltiptext">Export current alpha and density selection (clustering) to file</span>
      </div>
      <div class="tooltip-nav-bar">
        <font-awesome-icon class="rerun"
                           v-on:click="rerun" icon="arrow-rotate-right"/>
        <span class="tooltiptext">Restart algorithm run</span>
      </div>
    </span>
  </div>
</template>

<script>

import {modes} from "../../config/modes";
import {computeColorLabels} from "../../services/colors";
import {updateCurrentCluster, updateCurrentLabels} from "../../services/data/datasource";

export default {
  name: "Header",
  props: ['title', 'trash', 'branch', 'trashCallback', 'selector', 'parent', 'drawPolygon', 'disease', 'inspect', 'alpha',
    'include', 'exclude', 'noise', 'fileExport'],
  methods: {
    updateNet() {
      if (!this.$store.getters.loadingAny) {
        this.$emit('updateNet')
        this.$store.commit('updateInspectCluster', !this.$store.getters.inspectCluster)
      }
    },
    updateScatter() {
      if (!this.$store.getters.loadingAny) {
        this.$emit('updateScatter')
        this.$store.commit('updateInspectCluster', !this.$store.getters.inspectCluster)
      }
    },
    inspectCluster() {
      if (!this.$store.getters.loadingAny) {
        this.$store.commit('updateInspectCluster', !this.$store.getters.inspectCluster)
      }
    },
    inspectJoins() {
      if (this.isModeAlpha()) {
        this.$store.commit('updateCurrentMode', modes.LEVEL_SET)
      } else {
        this.$store.commit('updateCurrentMode', modes.ALPHA)
      }
    },
    isModeAlpha() {
      return this.$store.getters.currentMode == modes.ALPHA;
    },
    isModeLevelSet() {
      return this.$store.getters.currentMode == modes.LEVEL_SET;
    },
    isModeCluster() {
      return this.$store.getters.currentMode == modes.CLUSTER;
    },
    /*inclusiveSelect() {
      this.$store.commit('updateSelectInclude', true)
    },*/
    exclusiveSelect() {
      this.$store.commit('updateSelectExclude', !this.$store.getters.selectExclude)
    },
    toggleNoise() {
      if (!this.$store.getters.loadingAny) {
        this.$store.commit('updateNoise', !this.$store.getters.noise)
        this.$store.commit('updateColorLabels', computeColorLabels(this.$store.getters.labels,
            this.$store.getters.colorMap,
            this.$store.getters.noise))
      }
    },
    continueWithSelection() {
      if (!this.$store.getters.loadingAny) {
        if (this.isModeAlpha()) {
          this.$store.commit('updateCurrentMode', modes.LEVEL_SET)
        } else if (this.isModeLevelSet()) {
          this.$store.commit('updateCurrentMode', modes.CLUSTER)
        }
      }
    },
    goBack() {
      if (!this.$store.getters.loadingAny) {
        if (this.isModeLevelSet()) {
          this.$store.commit('updateCurrentMode', modes.ALPHA)
        } else if (this.isModeCluster()) {
          this.exitAndSaveClusterDetails()
        }
      }
    },
    rerun() {
      if (!this.$store.getters.loadingAny) {
        location.reload()
      }
    },
    exitAndSaveClusterDetails() {
      let cluster = this.$store.getters.levelSet[this.$store.getters.currentCluster.level]
          [this.$store.getters.currentCluster.label]
      cluster.name = this.$store.getters.temporaryClusterName
      this.$store.commit("addNode", cluster)
      updateCurrentCluster()
      this.$store.commit('updateCurrentMode', this.$store.getters.previousMode)
      updateCurrentLabels({
        level: this.$store.getters.level,
        alpha: this.$store.getters.alpha
      })
    }
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
  width: 102%;
  margin: -8px -30px 5px -20px;
}

.view-header-title {
  font-size: 12px;
  margin-left: 5%;
}

.toolbar {
  margin-left: 20px;
  float: left;
}

.nav-bar {
  margin-right: 10px;
  float: right;
}

.tool {
  margin-right: 5px;
  margin-top: 4px;
  border: solid gray 1px;
  cursor: pointer;
  opacity: 0.5;
  height: 30px;
  width: 30px;
}

.check {
  margin-right: 15px;
  margin-top: 4px;
  margin-bottom: -3px;
  cursor: pointer;
  opacity: 1;
  color: green;
  height: 35px;
  width: 35px;
  float: right;
}

.rerun {
  margin-right: 5px;
  margin-left: 5px;
  margin-top: 4px;
  margin-bottom: -3px;
  cursor: pointer;
  opacity: 1;
  color: green;
  height: 34px;
  width: 34px;
  float: right;
}

.export {
  margin-right: 5px;
  margin-top: 4px;
  margin-bottom: -3px;
  cursor: pointer;
  opacity: 1;
  color: cornflowerblue;
  height: 35px;
  width: 35px;
  float: right;
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

.tooltip-nav-bar {
  position: relative;
  display: inline-block;
}

/* Tooltip text */
.tooltip .tooltiptext {
  bottom: -30px;
  left: 10px;
  visibility: hidden;
  width: 500px;
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


/* Tooltip text */
.tooltip-nav-bar .tooltiptext {
  bottom: -30px;
  right: 10px;
  visibility: hidden;
  width: 500px;
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
.tooltip-nav-bar:hover .tooltiptext {
  visibility: visible;
}
</style>