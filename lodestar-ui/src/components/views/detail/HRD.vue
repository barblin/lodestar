<template>
  <svg :id="PANE_NAME" width="350" height="300"></svg>
  <div id="spinner" v-if="$store.getters.loadingAny">
    <ScaleLoader v-if="$store.getters.loadingAny"></ScaleLoader>
  </div>
</template>

<script>
import ScaleLoader from 'vue-spinner/src/ScaleLoader.vue'
import ViewHeader from "../../nav/ViewHeader.vue";
import * as d3 from "d3";
import {TWO_DIMENSION_LAYOUT} from "../../../config/plotly-layouts";
import {store} from "../../../store/cluster-state-store";
import {createTwoDimensionalTraces} from "../../../services/trace-service";

const PANE_NAME = "hrd"

export default {
  name: "HRD",
  props: ['plotData', 'parent', 'colorLabels', 'highlight'],
  components: {
    ScaleLoader,
    ViewHeader
  },
  data: function () {
    return {
      PANE_NAME: PANE_NAME,
      traces: []
    }
  },
  mounted() {
  },
  watch: {
    plotData: function (data) {
      this.draw(data)
    },
    colorLabels: function () {
      this.draw(this.$store.getters.hrd)
    },
    highlight: function () {
      this.traces = createTwoDimensionalTraces(PANE_NAME, this.$store.getters.hrd, this.colorLabels, this.traces)
    }
  },
  methods: {
    draw(hrdData) {
      if (hrdData == undefined || Object.keys(hrdData).length === 0) {
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

      Plotly.react(PANE_NAME, [], TWO_DIMENSION_LAYOUT(height, width, 'HRD',
          store.getters.hrdSelection.x,
          store.getters.hrdSelection.y
      ), 'reversed');
      this.traces = createTwoDimensionalTraces(PANE_NAME, hrdData, this.colorLabels, [])

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
select {
  width: 30%;
  margin-right: 10px;
  margin-left: 5px;
}
</style>