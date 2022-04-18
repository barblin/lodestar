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
import {col_map} from "../../services/colors";

const PANE_NAME = "velocity_pane"
const PANE_NAME_3D = "velocity_pane_3D"

export default {
  name: "VelocityPlot",
  props: ['parent', 'drawNet', 'drawScatter', 'netData', 'scatData', 'colorLabels'],
  components: {
    ScaleLoader,
    ViewHeader
  },
  mounted() {
    if (this.$store.getters.velocityScatterData) {
      this.draw(this.$store.getters.velocityScatterData)
    }
  },
  data: function () {
    return {
      PANE_NAME: PANE_NAME,
      PANE_NAME_3D: PANE_NAME_3D
    }
  },
  watch: {
    drawNet: function () {
      this.draw(this.$store.getters.velocityScatterData)
    },
    drawScatter: function () {
      this.draw(this.$store.getters.velocityScatterData)
    },
    colorLabels: function () {
      this.draw(this.$store.getters.velocityScatterData)
    },
    netData: function (data) {
      //this.draw(data)
    },
    scatData: function (data) {
      this.draw(data)
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
      if(data == undefined){
        return
      }

      let parent = document.getElementById(this.parent)

      if (!parent) {
        parent = document.getElementById('main')
      }

      d3.select("#" + PANE_NAME).selectAll("svg").remove();

      const margin = {top: 10, right: 10, bottom: 20, left: 35},
          width = parent.clientWidth - margin.left - margin.right,
          height = parent.clientHeight - margin.top - margin.bottom;

      const svg = d3.select("#" + PANE_NAME)
          .append("svg")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
          .append("g")
          .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");

      let minx = 10000000;
      let maxx = 0;
      let miny = 10000000;
      let maxy = 0;

      for (let i = 0; i < data.length; i++) {
        if (this.colorLabels.length <= i) {
          data[i].label = col_map[0]
        } else {
          data[i].label = this.colorLabels[i]
        }

        if(data[i].label !== col_map[12]) {
          let row = data[i];

          if (row.x < minx) {
            minx = row.x
          }

          if (maxx < row.x) {
            maxx = row.x
          }

          if (row.y < miny) {
            miny = row.y
          }

          if (maxy < row.y) {
            maxy = row.y
          }
        }
      }

      // Add X axis
      var x = d3.scaleLinear()
          .domain([minx, maxx])
          .range([0, width]);
      svg.append("g")
          .attr("transform", "translate(0," + height + ")")
          .call(d3.axisBottom(x));

      // Add Y axis
      var y = d3.scaleLinear()
          .domain([miny, maxy])
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
            return x(d.x);
          })
          .attr("cy", function (d) {
            return y(d.y);
          })
          .attr("r", 1.5)
          .style("fill", function (d) {
            return d.label;
          })
    }
  }
}

</script>

<style scoped>
</style>