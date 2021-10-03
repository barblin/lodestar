<template>
  <ViewHeader :title='"Original / Optimal Clustering"' :parent=parent @maximize="maximize"></ViewHeader>
  <div id="scatter_pane">
    <div id="spinner" v-if="$store.getters.loadingScatter">
      <ScaleLoader v-if="$store.getters.loadingScatter"></ScaleLoader>
    </div>
  </div>
</template>

<script>
import * as d3 from "d3";
import {col_map} from "../../../services/colors";
import ScaleLoader from 'vue-spinner/src/ScaleLoader.vue'
import ViewHeader from "../utils/ViewHeader.vue";


export default {
  name: "Scatter",
  props: ['plotData', 'parent'],
  components: {
    ScaleLoader,
    ViewHeader
  },
  watch: {
    parent: {
      immediate: true,
      handler(val, oldVal) {
        this.redraw(this.$store.getters.plotData)
      }
    },
    plotData: function (plotData) {
      this.redraw(plotData)
    }

  },
  methods: {
    maximize() {
      this.$emit('maximize')
    },
    redraw(plotData) {
      let parent = document.getElementById(this.parent)

      if (parent == null) {
        parent = document.getElementById('main')
      }

      if (parent == null) {
        return
      }

      if (plotData != null) {
        const margin = {top: 10, right: 10, bottom: 50, left: 30},
            width = parent.clientWidth - margin.left - margin.right,
            height = parent.clientHeight - margin.top - margin.bottom;

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

        let data = []
        let clusters = plotData.clusters

        if (clusters) {
          for (const [key, value] of Object.entries(clusters)) {
            data.push.apply(data, value)

            if (key == 0) continue;

            let points = []

            value.forEach((point) => points.push([x(point[0]), y(point[1])]))
            const hull = d3.polygonHull(points);

            var lineGenerator = d3.line();
            var pathString = lineGenerator(hull);

            svg.append("path")
                .attr('d', pathString)
                .style("fill", function (d) {
                  return col_map[key];
                })
                .attr("stroke", "black");
          }

          svg.append('g')
              .selectAll("dot")
              .data(data)
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