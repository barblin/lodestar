<template>
  <div :id="PANE_NAME">
    <div id="spinner" v-if="$store.getters.loadingMain">
      <ScaleLoader v-if="$store.getters.loadingMain"></ScaleLoader>
    </div>
  </div>
</template>

<script>
import ScaleLoader from 'vue-spinner/src/ScaleLoader.vue'
import * as d3 from "d3";
import {updateBatch} from "../../../services/data/datasource";
import {density_max, highlight} from "../../../services/colors";

const PANE_NAME = "heat_map_pane"

export default {
  name: "HeatMap",
  props: ['parent', 'heatmap', 'level', 'alpha'],
  data: function () {
    return {
      PANE_NAME: PANE_NAME,
      tooltip: {}
    }
  },
  components: {
    ScaleLoader
  },
  mounted() {
    this.redraw(this.$store.getters.heatmap)
  },
  watch: {
    heatmap: function (data) {
      this.redraw(data)
    },
    level: function () {
      this.redraw(this.$store.getters.heatmap)
    },
    alpha: function () {
      this.redraw(this.$store.getters.heatmap)
    },
  },
  methods: {
    redraw(data) {
      if (data.heatmap == undefined) {
        return
      }

      let parent = document.getElementById(this.parent)

      if (!parent) {
        parent = document.getElementById('main')
      }

      d3.select("#" + PANE_NAME).selectAll("svg").remove();
      this.tooltip = this.createTooltip();

      const margin = {top: 50, right: 50, bottom: 19, left: 25},
          width = parent.clientWidth - margin.left - margin.right,
          height = parent.clientHeight - margin.top - margin.bottom;

      var svg = d3.select("#" + PANE_NAME)
          .append("svg")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
          .append("g")
          .attr("transform",
              "translate(" + margin.left + "," + 0 + ")");

      var legend = svg.append('g')
      legend.append("circle").attr("cx",0).attr("cy", 10).attr("r", 6).style("fill", "white").style("stroke", "black")
      legend.append("circle").attr("cx",170).attr("cy", 10).attr("r", 6).style("fill", density_max).style("border", "1px solid black")
      legend.append("text").attr("x", 10).attr("y", 11).text("Much delta (unstable)").style("font-size", "11").attr("alignment-baseline","middle")
      legend.append("text").attr("x", 180).attr("y", 11).text("Little delta (stable)").style("font-size", "11").attr("alignment-baseline","middle")

      legend.attr("transform",
          "translate(" + width/2 + "," + 0 + ")")

      var myGroups = []
      var myVars = []

      data.heatmap.forEach(d => {
        myGroups.push(d.group)
        myVars.push(d.variable)
      })

      svg.append("text")
          .attr("class", "x label")
          .attr("text-anchor", "end")
          .attr("font-size", 11)
          .attr("x", width)
          .attr("y", 15)
          .text("Delta in density")

      svg.append("text")
          .style("transform", function (d) {
            return "rotate(90deg)";
          })
          .attr("class", "x label")
          .attr("text-anchor", "end")
          .attr("font-size", 11)
          .attr("x", 125)
          .attr("y", -width - 40)
          .text("Delta in alpha")


      var x = d3.scaleBand()
          .range([0, width])
          .domain(myGroups)
          .padding(0.01);
      svg.append("g")
          .attr("transform",
              "translate(" + 0 + "," + (height + margin.top) + ")")
          .call(d3.axisBottom(x))

      var y = d3.scaleBand()
          .range([height, 0])
          .domain(myVars)
          .padding(0.01);
      svg.append("g")
          .attr("transform",
              "translate(" + 0 + "," + margin.top + ")")
          .call(d3.axisLeft(y));

      var myColor = d3.scalePow()
          .exponent(0.5)
          .range(["white", density_max])
          .domain([data.max_value, data.min_value])


      let self = this;

      self.createAlphaHistogram(svg, parent, data.density_histo, data.dmin, data.dmax)
      self.createDensityHistogram(svg, parent, data.alpha_histo, data.amin, data.amax)

      let store = this.$store
      let tooltip = this.tooltip
      svg.append('g')
          .attr("transform",
              "translate(" + 0 + "," + margin.top + ")")
          .selectAll()
          .data(data.heatmap, function (d) {
            return d.group + ':' + d.variable;
          })
          .enter()
          .append("rect")
          .attr("x", function (d) {
            return x(d.group)
          })
          .attr("y", function (d) {
            return y(d.variable)
          })
          .attr("width", x.bandwidth())
          .attr("height", y.bandwidth())
          .style("fill", function (d) {
            if (d.alpha == store.getters.alpha &&
                d.level == store.getters.level) {
              return highlight;
            }

            return myColor(d.value)
          })
          .on("mouseover", function (d) {
              d3.select(this).style("cursor", "pointer");
            tooltip
                .html("alpha: " + event.target.__data__.alpha + ", density: " + event.target.__data__.level)
                .style("position", "absolute")
                .style("top", "0%")
                .style("left", "40%")

            tooltip.style("opacity", 1)
          }).on("mouseout", function (d){
             tooltip.style("opacity", 0)
          })
          .on("click", function (event) {
            if(!store.getters.loadingAny) {
              tooltip.style("opacity", 0)
              store.commit('updateAlpha', event.target.__data__.alpha)
              store.commit('updateLevel', event.target.__data__.level)

              updateBatch();
            }
          })
    },
    createDensityHistogram(svg, parent, data, min, max) {
      const margin = {top: parent.clientHeight, right: 0, bottom: -50, left: 0},
          width = parent.clientWidth - margin.left - margin.right,
          height = parent.clientHeight - margin.top - margin.bottom;

      var x = d3.scaleLinear()
          .range([0, width - 75]);

      var y = d3.scaleLinear()
          .domain([min, max])
          .range([height, 0]);

      svg.append("g").selectAll("rect")
          .data(data)
          .enter()
          .append("rect")
          .attr("x", 0)
          .attr("transform", function (d, i) {
            return "translate(" + x((i) / data.length) + "," + y(d) + ")";
          })
          .attr("width", function () {
            return x(1 / data.length);
          })
          .attr("height", function (d) {
            return height - y(d);
          })
          .style("fill", "#FF7F7F")
    },
    createAlphaHistogram(svg, parent, data, min, max) {
      const margin = {top: parent.clientHeight, right: 0, bottom: -50, left: 0},
          height = parent.clientHeight - margin.top - margin.bottom;

      var x = d3.scaleLinear()
          .range([0, parent.clientHeight - 70]);

      // Y axis: scale and draw:
      var y = d3.scaleLinear()
          .range([height, 0]);
      y.domain([min, max]);   // d3.hist has to be called before the Y axis obviously

      let histo = Array.from(data).reverse()
      svg.append("g")
          .style("transform", function (d) {
            return "rotate(90deg)";
          })
          .selectAll("rect")
          .data(histo)
          .enter()
          .append("rect")
          .attr("x", 1)
          .attr("transform", function (d, i) {
            return "translate(" + (x((i) / data.length) + 50) + "," + (y(d) - parent.clientWidth + 25) + ")";
          })
          .attr("width", function (d) {
            return x(1 / data.length);
          })
          .attr("height", function (d) {
            return height - y(d);
          })
          .style("fill", "#FF7F7F")
    },
    createTooltip() {
      return d3.select("#" + PANE_NAME)
          .append("div")
          .style("opacity", 0)
          .attr("class", "tooltip")
          .style("background-color", "white")
          .style("float", "left")
          .style("position", "relative")
          .style("border", "solid")
          .style("border-width", "1px")
          .style("border-radius", "5px")
          .style("padding-left", "15px")
          .style("padding-right", "15px")
          .style("line-height", "25px")
    },
  }
}


</script>

<style scoped>
</style>
