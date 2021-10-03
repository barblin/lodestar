<template>
  <ViewHeader :title='"Two velocity features clustering"' :parent=parent @maximize="maximize"
              :drawPolygon="true" :disease="true" @updateNet="updateNet" @updateScatter="updateScatter"></ViewHeader>
  <div id="velocity_pane">
    <div id="spinner" v-if="$store.getters.loadingVelocity">
      <ScaleLoader v-if="$store.getters.loadingVelocity"></ScaleLoader>
    </div>
  </div>
</template>

<script>
import ScaleLoader from 'vue-spinner/src/ScaleLoader.vue'
import ViewHeader from "./utils/ViewHeader.vue";
import * as d3 from "d3";

export default {
  name: "VelocityPlot",
  props: ['plotData', 'parent', 'drawNet', 'drawScatter', 'netData', 'scatData'],
  components: {
    ScaleLoader,
    ViewHeader
  },
  mounted() {
    this.draw(this.$store.getters.velocityScatterData);
  },
  watch: {
    drawNet: function () {
      this.draw(this.$store.getters.velocityScatterData)
    },
    drawScatter: function () {
      //this.draw(this.$store.getters.velocityScatterData)
    },
    netData: function (data) {
      //this.draw(data)
    },
    scatData: function (data) {
      this.draw(data)
    }
  },
  methods: {
    maximize() {
      this.$emit('maximize')
    },
    updateNet() {
      this.$store.commit('updateDrawVelocityNet', !this.$store.getters.drawVelocityNet)
    },
    updateScatter() {
      this.$store.commit('updateDrawVelocityScatter', !this.$store.getters.drawVelocityScatter)
    },
    draw(data) {
      let parent = document.getElementById(this.parent)

      if (!parent) {
        parent = document.getElementById('main')
      }

      const margin = {top: 20, right: 20, bottom: 50, left: 50},
          width = parent.clientWidth - margin.left - margin.right,
          height = parent.clientHeight - margin.top - margin.bottom;

      const svg = d3.select("#velocity_pane")
          .append("svg")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
          .append("g")
          .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");

      // Add X axis
      var x = d3.scaleLinear()
          .domain([0, 4000])
          .range([0, width]);
      svg.append("g")
          .attr("transform", "translate(0," + height + ")")
          .call(d3.axisBottom(x));

      // Add Y axis
      var y = d3.scaleLinear()
          .domain([0, 500000])
          .range([height, 0]);
      svg.append("g")
          .call(d3.axisLeft(y));

      // Add dots
      svg.append('g')
          .selectAll("dot")
          .data(data)
          .enter()
          .append("circle")
          .attr("cx", function (d) {
            return x(d.GrLivArea);
          })
          .attr("cy", function (d) {
            return y(d.SalePrice);
          })
          .attr("r", 1.5)
          .style("fill", "#69b3a2")
    }
  }
}

</script>

<style scoped>
</style>