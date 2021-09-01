<template>
  <div class="scatter-plot">
    <ViewHeader :title='"Original / Optimal Clustering"'></ViewHeader>
    <div id="scatter_pane">
      <div id="spinner" v-if="$store.getters.loadingScatter">
        <ScaleLoader v-if="$store.getters.loadingScatter"></ScaleLoader>
      </div>
    </div>
  </div>
</template>

<script>
import * as d3 from "d3";
import {col_map} from "../../services/colors";
import ScaleLoader from 'vue-spinner/src/ScaleLoader.vue'
import ViewHeader from "./utils/ViewHeader.vue";


export default {
  name: "Scatter",
  props: ['plotData'],
  components: {
    ScaleLoader,
    ViewHeader
  },
  watch: {
    plotData: function (plotData) {
      const margin = {top: 10, right: 30, bottom: 40, left: 30},
          width = this.$store.getters.width - margin.left - margin.right,
          height = this.$store.getters.height - margin.top - margin.bottom;

      const svg = d3.select("#scatter_pane")
          .append("svg")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
          .append("g")
          .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");

      const x = d3.scaleLinear()
          .domain([0, plotData.max_x])
          .range([0, width]);
      svg.append("g")
          .attr("transform", "translate(0," + height + ")")
          .call(d3.axisBottom(x));

      const y = d3.scaleLinear()
          .domain([0, plotData.max_y])
          .range([height, 0]);
      svg.append("g")
          .call(d3.axisLeft(y));

      svg.append('g')
          .selectAll("dot")
          .data(plotData.data)
          .enter()
          .append("circle")
          .attr("cx", function (d) {
            return x(d[0]);
          })
          .attr("cy", function (d) {
            return y(d[1]);
          })
          .attr("r", 1.0)
          .style("fill", function (d) {
            return col_map[d[2]];
          })
    }

  }
}

</script>

<style scoped>
.scatter-plot {
  position: relative;
  display: block;
  width: 600px;
  height: 460px;
  border: 1px solid darkslategrey;
  margin-bottom: 10px;
}
</style>