<template>
  <div :id="PANE_NAME" v-if="true"></div>
  <div :id="PANE_NAME_3D" v-else></div>
  <div id="spinner" v-if="$store.getters.loadingVelocity">
    <ScaleLoader v-if="$store.getters.loadingVelocity"></ScaleLoader>
  </div>
</template>

<script>
import ScaleLoader from 'vue-spinner/src/ScaleLoader.vue'
import ViewHeader from "../nav/ViewHeader.vue";
import * as d3 from "d3";
import {includeThirdVelocityDimension} from "../../services/dimension-util";
import {inspect} from "../../services/cluster";
import {createTwoDimensionalTraces} from "../../services/trace_service";
import {TWO_DIMENSION_LAYOUT} from "../../config/plotly_layouts";
import {store} from "../../store/cluster-state-store";

const PANE_NAME = "velocity_pane"
const PANE_NAME_3D = "velocity_pane_3D"

export default {
  name: "VelocityPlot",
  props: ['parent', 'scatData', 'colorLabels', 'highlight'],
  components: {
    ScaleLoader,
    ViewHeader
  },
  data: function () {
    return {
      PANE_NAME: PANE_NAME,
      PANE_NAME_3D: PANE_NAME_3D,
      traces: []
    }
  },
  watch: {
    colorLabels: function () {
      this.draw(this.scatData)
    },
    scatData: function (data) {
      this.draw(data)
    },
    highlight: function () {
      this.traces = createTwoDimensionalTraces(PANE_NAME, this.scatData.solution, this.colorLabels, this.traces)
    }
  },
  methods: {
    includeThirdVelocityDimension() {
      return includeThirdVelocityDimension()
    },
    updateNet() {
      this.$store.commit('updateDrawVelocityNet', !this.$store.getters.drawVelocityNet)
    },
    updateScatter() {
      this.$store.commit('updateDrawVelocityScatter', !this.$store.getters.drawVelocityScatter)
    },
    draw(data) {
      if (data == undefined || data.solution == undefined) {
        return
      }

      let parent = document.getElementById(this.parent)

      if (!parent) {
        parent = document.getElementById('main')
      }

      const margin = {top: 0, right: 5, bottom: 0, left: 0},
          width = parent.clientWidth - margin.left - margin.right,
          height = parent.clientHeight - margin.top - margin.bottom;

      Plotly.purge(PANE_NAME);

      d3.select("#" + PANE_NAME).selectAll("svg").remove();

      Plotly.react(PANE_NAME, [], TWO_DIMENSION_LAYOUT(height, width, 'Velocity',
          store.getters.resourceHeaders[store.getters.currentColumnSelection.v1],
          store.getters.resourceHeaders[store.getters.currentColumnSelection.v2]
      ));
      this.traces = createTwoDimensionalTraces(PANE_NAME, data.solution, this.colorLabels, [])

      let myDiv = document.getElementById(PANE_NAME);
      myDiv.on('plotly_click', function (data) {
        if (store.getters.inspectCluster == true) {
          store.commit('updateInspectCluster', !store.getters.inspectCluster)
          inspect(store.getters.level, data.points[0].data.labels[data.points[0].pointNumber])
        }
      });
    }
  }
}

</script>

<style scoped>
</style>