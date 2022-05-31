<template>
  <div :id="PANE_NAME" class="default">
    <div id="spinner" v-if="$store.getters.loadingSpace">
      <ScaleLoader v-if="$store.getters.loadingSpace"></ScaleLoader>
    </div>
  </div>
</template>

<script>
import ScaleLoader from 'vue-spinner/src/ScaleLoader.vue'
import ViewHeader from "../nav/ViewHeader.vue";
import {col_map} from "../../config/colors";
import * as d3 from "d3";
import {inspect} from "../../services/cluster";
import {createSpaceTraces} from "../../services/trace_service";
import {THREE_DIMENSION_LAYOUT} from "../../config/plotly_layouts";

const PANE_NAME = "space_pane"

export default {
  name: "SpacePlot",
  props: ['spaceData', 'parent', 'magnify', 'colorLabels', 'highlight'],
  components: {
    ScaleLoader,
    ViewHeader
  },
  data: function () {
    return {
      PANE_NAME: PANE_NAME,
      colors: col_map,
      traces: []
    }
  },
  watch: {
    spaceData: function (spaceData) {
      this.draw(spaceData)
    },
    colorLabels: function () {
      this.draw(this.spaceData)
    },
    magnify: function () {
      if (this.$store.getters.inspectCluster) {
        document.getElementById(PANE_NAME).className += ' magnify';
      } else {
        document.getElementById(PANE_NAME).className = document.getElementById(PANE_NAME).className.replace('magnify', '');
      }
    },
    highlight: function () {
      this.traces = createSpaceTraces(PANE_NAME, this.spaceData.solution, this.colorLabels, this.traces)
    }
  },
  methods: {
    maximize() {
      this.$emit('maximize')
    },
    updateScatter() {
      this.$store.commit('updateDrawSpaceScatter', !this.$store.getters.drawSpaceScatter)
    },
    draw(data) {
      if (data == undefined || data.solution == undefined) {
        return
      }

      Plotly.purge(PANE_NAME);

      d3.select("#" + PANE_NAME).selectAll("svg").remove();

      let parent = document.getElementById(this.parent)

      if (!parent) {
        parent = document.getElementById('main')
      }

      const margin = {top: 20, right: 10, bottom: -20, left: 0},
          width = parent.clientWidth - margin.left - margin.right,
          height = parent.clientHeight - margin.top - margin.bottom;

      const store = this.$store

      Plotly.react(PANE_NAME, [], THREE_DIMENSION_LAYOUT(height, width))
      this.traces = createSpaceTraces(PANE_NAME, data.solution, this.colorLabels, [])

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
.magnify {
  cursor: zoom-in;
}

.default {
}
</style>