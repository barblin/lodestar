<template>
  <ViewHeader :title='"Two velocity features clustering"' :parent=parent
              :drawPolygon="true" :disease="true" :noise="true" @updateNet="updateNet"
              @updateScatter="updateScatter"></ViewHeader>
  <div :id="PANE_NAME" v-if="!includeThirdVelocityDimension()"></div>
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
      let parent = document.getElementById(this.parent)

      if (!parent) {
        parent = document.getElementById('main')
      }

      if (includeThirdVelocityDimension()) {
        d3.select("#" + PANE_NAME_3D).selectAll("svg").remove();

        const margin = {top: 20, right: 10, bottom: 10, left: 0},
            width = parent.clientWidth - margin.left - margin.right,
            height = parent.clientHeight - margin.top - margin.bottom;

        let scatterData = []
        let dataX = []
        let dataY = []
        let dataZ = []

        for (let i = 0; i < data.length; i++) {
          let row = data[i];
          dataX.push(row.x)
          dataY.push(row.y)
          dataZ.push(row.z)
        }

        scatterData.push({
          x: dataX,
          y: dataY,
          z: dataZ,
          mode: 'markers',
          type: 'scatter3d',
          marker: {
            color: 'rgb(23, 190, 207)',
            size: 2
          }
        }, /*{
          alphahull: 7,
          opacity: 0.1,
          type: 'mesh3d',
          x: dataX,
          y: dataY,
          z: dataZ
        }*/)

        var layout = {
          autosize: true,
          height: height,
          margin: {
            l: 0,
            r: 0,
            b: 0,
            t: 0,
            pad: 0
          },
          scene: {
            aspectratio: {
              x: 1,
              y: 1,
              z: 1
            },
            camera: {
              center: {
                x: 0,
                y: 0,
                z: 0
              },
              eye: {
                x: 1.25,
                y: 1.25,
                z: 1.25
              },
              up: {
                x: 0,
                y: 0,
                z: 1
              }
            },
            xaxis: {
              type: 'linear',
              zeroline: false
            },
            yaxis: {
              type: 'linear',
              zeroline: false
            },
            zaxis: {
              type: 'linear',
              zeroline: false
            }
          },
          width: width
        };

        Plotly.react(PANE_NAME_3D, scatterData, layout);

      } else {
        d3.select("#" + PANE_NAME).selectAll("svg").remove();

        const margin = {top: 10, right: 10, bottom: 50, left: 35},
            width = parent.clientWidth - margin.left - margin.right,
            height = parent.clientHeight - margin.top - margin.bottom;

        const svg = d3.select("#" + PANE_NAME)
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform",
                "translate(" + margin.left + "," + margin.top + ")");

        let minx = 0;
        let maxx = 0;
        let miny = 0;
        let maxy = 0;

        for (let i = 0; i < data.length; i++) {
          if (this.colorLabels.length <= i) {
            data[i].label = col_map[0]
          } else {
            data[i].label = this.colorLabels[i]
          }
        }

        for (let i = 0; i < data.length; i++) {
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
}

</script>

<style scoped>
</style>