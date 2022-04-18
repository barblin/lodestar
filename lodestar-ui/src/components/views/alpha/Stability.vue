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

const PANE_NAME = "stability_pane"

export default {
  name: "Stability",
  props: ['parent', 'heatmap', 'level', 'alpha'],
  components: {
    ScaleLoader
  },
  data: function () {
    return {
      PANE_NAME: PANE_NAME,
      tooltip: {}
    }
  },
  mounted() {
    this.draw(this.$store.getters.heatmap)
  },
  watch: {
    heatmap: function (data) {
      this.draw(data)
    },
    level: function () {
      this.draw(this.$store.getters.heatmap)
    },
    alpha: function () {
      this.draw(this.$store.getters.heatmap)
    },
  },
  methods: {
    draw(data) {
      this.tooltip = this.createTooltip();


      if (data.domain == undefined) {
        return
      }

      let parent = document.getElementById(this.parent)

      if (!parent) {
        parent = document.getElementById('main')
      }

      d3.select("#" + PANE_NAME).selectAll("svg").remove();

      const margin = {top: 10, right: 10, bottom: 25, left: 25},
          width = parent.clientWidth - margin.left - margin.right,
          height = parent.clientHeight - margin.top - margin.bottom;

      const svg = d3.select("#" + PANE_NAME)
          .append("svg")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
          .append("g")
          .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");

      // Add X axis

      let array = Array.from(data.domain)

      svg.append("g").append("text")
          .attr("class", "x label")
          .attr("text-anchor", "end")
          .attr("font-size", 11)
          .attr("x", width - 20)
          .attr("y", 10)
          .text("(alpha, delta) combination")

      svg.append("g")
          .style("transform", function (d) {
            return "rotate(90deg)";
          })
          .append("text")
          .attr("class", "x label")
          .attr("text-anchor", "end")
          .attr("font-size", 11)
          .attr("x", 100)
          .attr("y", -width + 5)
          .text("num clusters")

      var linearScale = d3.scaleLinear()
          .domain([0, array.length])
          .range([0, width]);
      svg.append("g")
          .attr("transform", "translate(0," + height + ")")
          .call(d3.axisBottom(linearScale));

      // Add Y axis
      var y = d3.scaleLinear()
          .domain([0, data.cmax])
          .range([height, 0]);
      svg.append("g")
          .call(d3.axisLeft(y));

      let circles = []
      data.cluster.forEach((d, i) => circles.push({'x': array[i], 'y': d.num_cluster, 'level': d.level, 'alpha': d.alpha}))

      // Add dots
      let store = this.$store;
      let tooltip = this.tooltip
      svg.append('g')
          .selectAll("dot")
          .data(circles)
          .enter()
          .append("circle")
          .attr("cx", function (d, i) {
            return linearScale(i);
          })
          .attr("cy", function (d) {
            return y(d.y);
          })
          .attr("r", function (d) {
            if (d.alpha == store.getters.alpha &&
                d.level == store.getters.level) {
              return 5;
            }
            return 1.5
          })
          .style("fill", function (d) {
            if (d.alpha == store.getters.alpha &&
                d.level == store.getters.level) {
              return "rgba(0,255,0,0.67)";
            }

            return "#155849";
          }).on("mouseover", function (d) {
            let name = d.target.__data__.x

            d3.select(this).style("cursor", "pointer").attr("fill", '#ccac00');
            tooltip
                .html(name)
                .style("position", "absolute")
                .style("top", "0%")
                .style("left", "25%")

            tooltip.style("opacity", 1)
          })
            .on("mouseout", function (d) {
                d3.select(this).style("cursor", "default").attr("fill", "black");
              tooltip.style("opacity", 0)
          })
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
