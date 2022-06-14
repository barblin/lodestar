<template>
  <select id="selectX">
    <option value="$store.getters.selectorSelection.x" disabled selected>{{
        $store.getters.selectorSelection.x
      }}
    </option>
  </select>
  <select id="selectY">
    <option value="$store.getters.selectorSelection.y" disabled selected>{{
        $store.getters.selectorSelection.y
      }}
    </option>
  </select>
  <svg :id="PANE_NAME" width="350" height="300"></svg>
  <div id="spinner" v-if="$store.getters.loadingAny">
    <ScaleLoader v-if="$store.getters.loadingAny"></ScaleLoader>
  </div>
</template>

<script>
import ScaleLoader from 'vue-spinner/src/ScaleLoader.vue'
import ViewHeader from "../../nav/ViewHeader.vue";
import * as d3 from "d3";
import {updateSelection} from "../../../services/data/datasource";
import {inspect} from "../../../services/cluster";
import {createTwoDimensionalTraces} from "../../../services/trace-service";
import {TWO_DIMENSION_LAYOUT} from "../../../config/plotly-layouts";
import {store} from "../../../store/cluster-state-store";

const PANE_NAME = "selector"

export default {
  name: "Selector",
  props: ['plotData', 'colorLabels', 'parent', 'highlight'],
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
      this.draw(data, this.$store.getters.resourceHeaders)
    },
    selections: function () {
      this.draw(this.$store.getters.selector, this.$store.getters.resourceHeaders)
    },
    colorLabels: function () {
      this.draw(this.$store.getters.selector, this.$store.getters.resourceHeaders)
    },
    highlight: function () {
      this.traces = createTwoDimensionalTraces(PANE_NAME, this.$store.getters.selector, this.colorLabels, this.traces)
    }
  },
  methods: {
    draw(selectorData, allColumns) {
      if (selectorData == undefined || Object.keys(selectorData).length === 0) {
        return
      }

      d3.selectAll(".deletableSel").remove()
      d3.selectAll(".deletableOpt").remove()


      d3.select("#selectX")
          .selectAll('myOptions')
          .data(allColumns)
          .enter()
          .append('option')
          .attr("class", "deletableOpt")
          .text(function (d) {
            return d;
          }) // text showed in the menu
          .attr("value", function (d) {
            return d;
          }) // corresponding value returned by the button

      d3.select("#selectY")
          .selectAll('myOptions')
          .data(allColumns)
          .enter()
          .append('option')
          .attr("class", "deletableOpt")
          .text(function (d) {
            return d;
          }) // text showed in the menu
          .attr("value", function (d) {
            return d;
          }) // corresponding value returned by the button

      let parent = document.getElementById(this.parent)

      if (!parent) {
        parent = document.getElementById('main')
      }

      const margin = {top: 30, right: 0, bottom: 0, left: 0},
          width = parent.clientWidth - margin.left - margin.right,
          height = parent.clientHeight - margin.top - margin.bottom;

      Plotly.purge(PANE_NAME);

      d3.select("#" + PANE_NAME).selectAll("svg").remove();

      Plotly.react(PANE_NAME, [], TWO_DIMENSION_LAYOUT(height, width, '',
          this.$store.getters.selectorSelection.x,
          this.$store.getters.selectorSelection.y
      ));
      this.traces = createTwoDimensionalTraces(PANE_NAME, selectorData, this.colorLabels, [])

      let myDiv = document.getElementById(PANE_NAME);
      myDiv.on('plotly_click', function (data) {
        if (store.getters.inspectCluster == true) {
          store.commit('updateInspectCluster', !store.getters.inspectCluster)
          inspect(store.getters.level, data.points[0].data.labels[data.points[0].pointNumber])
        }
      });

      let self = this;
      d3.select("#selectX").on("change", function (d) {
        let selection = self.getSelection()
        selection.x = this.value
        self.updateSelection(selection)
      })

      d3.select("#selectY").on("change", function (d) {
        let selection = self.getSelection()
        selection.y = this.value
        self.updateSelection(selection)
      })
    },
    getSelection() {
      return this.$store.getters.selectorSelection
    },
    updateSelection(selection) {
      this.$store.commit('updateSelectorSelection', selection)
      updateSelection(this.$store.getters.currentResource);
    },
  }
}

</script>

<style scoped>
select {
  width: 46%;
  margin-right: 10px;
  margin-left: 5px;
}
</style>