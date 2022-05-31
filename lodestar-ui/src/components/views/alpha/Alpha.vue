<template>
  <div :id="PANE_NAME">
    <div id="spinner" v-if="$store.getters.loadingAny">
      <ScaleLoader v-if="$store.getters.loadingAny"></ScaleLoader>
    </div>
  </div>
</template>

<script>
import ScaleLoader from 'vue-spinner/src/ScaleLoader.vue'
import * as d3 from "d3";
import {percentChange} from "../../../services/views";
import {createLevelLabels} from "../../../services/d3-tools";
import {updateBatch} from "../../../services/datasource";
import {highlight} from "../../../config/colors";

const PANE_NAME = "alpha_pane"

let pos_map = {}

export default {
  name: "Alpha",
  props: ['parent', 'allLabels'],
  data: function () {
    return {
      PANE_NAME: PANE_NAME,
      svg: {},
      widthFactor: 1,
      tooltip: {}
    }
  },
  components: {
    ScaleLoader
  },
  mounted() {
    this.redraw(this.$store.getters.significantRoots)
  },
  watch: {
    allLabels: function () {
      this.redraw(this.$store.getters.significantRoots)
    },
  },
  methods: {
    redraw(significantRoots) {
      d3.select("#" + PANE_NAME).selectAll(".tooltip").remove();

      this.tooltip = this.createTooltip();
      pos_map = {}

      d3.select("#" + PANE_NAME).selectAll("svg").remove();

      let parent = document.getElementById(this.parent)

      const margin = {top: 0, right: 20, bottom: 0, left: 10},
          width = parent.clientWidth - margin.left - margin.right,
          height = parent.clientHeight - margin.top - margin.bottom - 20;

      this.widthFactor = percentChange(this.maxX, width)

      this.svg = d3.select("#" + PANE_NAME)
          .append("svg")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + 20);

      let multiples = []
      let single = height / this.$store.getters.alphas.length

      let levels = []
      for (let i = 0; i < this.$store.getters.alphas.length; i++) {
        multiples.push([(i + 1) * single, this.$store.getters.alphas[i]])
        levels.push([(i + 1) * single, "α " + i])
      }

      this.createLevelLines(parent, multiples, single)
      this.createSignificantRootsLines(parent, height, significantRoots, this.$store.getters.alphas, this.$store)
      this.createLevelButtons(this.$store, multiples, single)
      createLevelLabels(this.svg, levels, single / 2 - 20)
    },
    createLevelLines(parent, multiples, single) {
      return this.svg.append('g')
          .selectAll("line")
          .data(multiples)
          .enter()
          .append('line')
          .style("stroke-dasharray", ("3, 3"))
          .style("stroke", "grey")
          .style("stroke-width", 1)
          .attr("x1", 0)
          .attr("y1", (d) => d[0] + 20 - single)
          .attr("x2", parent.clientWidth)
          .attr("y2", (d) => d[0] + 20 - single);
    },
    createLevelButtons(store, multiples, single) {
      let context = this;

      let tooltip = this.tooltip
      return this.svg.append('g')
          .selectAll("line")
          .data(multiples)
          .enter()
          .append("line")
          .attr("class", "alphaButtons")
          .style("stroke", ("3, 3"))
          .style("stroke", (d) => {
            if (String(d[1]) === String(store.getters.alpha)) {
              return highlight
            } else {
              return "rgba(105,179,162,0.80)"
            }
          })
          .style("stroke-width", 35)
          .attr("x1", 7)
          .attr("y1", (d) => (d[0]) - single + 20)
          .attr("x2", 7)
          .attr("y2", (d) => (d[0] + 20))
          .on("mouseover", function (d) {
            if (!context.storedAlphaEqualsCurrent(d, store)) {
              d3.select(this).style("cursor", "pointer");
              d3.select(this).style('stroke', '#ccac00');
            }
            tooltip
                .html("alpha: " + String(d.target.__data__[1]))
                .style("position", "absolute")
                .style("top", "0%")
                .style("left", "35%")

            tooltip.style("opacity", 1)
          })
          .on("mouseout", function (d) {
            d3.select("#" + PANE_NAME).selectAll(".tooltip").style("opacity", 0);


            if (!context.storedAlphaEqualsCurrent(d, store)) {
              d3.select(this).style("stroke", "rgba(105,179,162,0.80)");
            }
            //tooltip.style("opacity", 0)
          })
          .on("click", function (d) {
            if (!store.getters.loadingAny) {
              d3.select("#" + PANE_NAME).selectAll(".tooltip").style("opacity", 0);

              if (!context.storedAlphaEqualsCurrent(d, store)) {
                d3.selectAll('.alphaButtons').style("stroke", "rgba(105,179,162,0.80)")


                store.commit('updateAlpha', d.target.__data__[1])
                updateBatch()

                d3.select(this).style("stroke", highlight);
              }
            }
          })
    },
    createSignificantRootsLines(parent, height, significantRoots, alphas, store) {
      let alpha_nodes = Object.values(significantRoots.alpha_nodes)

      let multiples = []
      let multiplesAlpha = []

      let maxLength = 0;

      alpha_nodes.forEach(node => {
        if (maxLength < node.length) {
          maxLength = node.length
        }
      })

      let singleWidth = (parent.clientWidth - 25) / maxLength
      let singleHeight = height / alphas.length
      let radius = 10

      if (singleWidth / 2 <= radius) {
        radius = singleWidth / 2 - 1
      }

      if (singleHeight <= radius) {
        radius = singleHeight - 1
      }

      for (let i = 0; i < alpha_nodes.length; i++) {
        multiples.push(([alphas[i], alpha_nodes[i]]))
      }

      for (let i = 0; i < alphas.length; i++) {
        multiplesAlpha.push([i, alphas[i]])
      }

      //Container for the gradients
      var defs = this.svg.append("defs");

      //Code taken from http://stackoverflow.com/questions/9630008/how-can-i-create-a-glow-around-a-rectangle-with-svg
      //Filter for the outside glow
      var filter = defs.append("filter")
          .attr("id", "glow");

      filter.append("feGaussianBlur")
          .attr("class", "blur")
          .attr("stdDeviation", "1.5")
          .attr("result", "coloredBlur");

      var feMerge = filter.append("feMerge");
      feMerge.append("feMergeNode")
      feMerge.append("feMergeNode")
          .attr("in", "coloredBlur")
          .attr("in", "SourceGraphic");

      let smaller = singleWidth
      if (singleHeight < singleWidth) {
        smaller = singleHeight
      }

      let circles = []
      for (let heightCounter = 0; heightCounter < multiples.length; heightCounter++) {
        let multi = multiples[heightCounter]
        pos_map[multi[0]] = {}

        for (let i = 0; i < multi[1].length; i++) {
          let d = multi[1][i]
          let to = d
          if (heightCounter + 1 < multiples.length) {
            to = store.getters.allLabels[multiples[heightCounter + 1][0]][d];
          }

          let color = -1
          if (d != -1) color = store.getters.alphaColorMap[multi[0]][d]

          pos_map[multi[0]][parseInt(d)] = {
            'x': i * singleWidth + (singleWidth / 2) + 25,
            'y': heightCounter * singleHeight + (singleHeight / 2) + 20,
            'to': to,
            'color': color
          }

          circles.push(pos_map[multi[0]][parseInt(d)])
        }
      }

      let edges = []
      for (let heightCounter = 0; heightCounter < multiples.length; heightCounter++) {
        if (heightCounter + 1 < multiples.length) {
          let start_a = multiples[heightCounter][0]
          let end_a = multiples[heightCounter + 1][0]

          for (const [key, value] of Object.entries(pos_map[start_a])) {
            if (pos_map[end_a][value.to] != undefined) {
              edges.push([value, pos_map[end_a][value.to]])
            }
          }
        }
      }

      this.svg.append('g')
          .selectAll("line")
          .data(edges)
          .enter()
          .append('line')
          .style("stroke", "black")
          .style("stroke-width", 2)
          .attr("x1", (d) => d[0].x)
          .attr("y1", (d) => d[0].y)
          .attr("x2", (d) => d[1].x)
          .attr("y2", (d) => d[1].y);

      this.svg.append("g")
          .selectAll("circle")
          .data(circles)
          .enter()
          .append("circle")
          .attr("fill", (circle, i) => {
            return circle.color
          })
          .attr("stroke", "none")
          .attr("cx", (d, i) => {
                return d.x
              }
          )
          .attr("cy", (d, i) => {
            return d.y
          })
          .attr("r", radius)
          .style("filter", (d) => {

            if (d[1] === store.getters.currentCluster.label) {
              return "url(#glow)";
            }

            return ""
          });

      this.svg.append("g")
          .append("text")
          .style("text-anchor", "middle")
          .attr("x", "50%")
          .attr("font-size", "10px")
          .attr("y", 10)
          .attr("dy", ".25em")
          .text(function (d) {
            return "Clusters per alphas with current density level";
          });
    },
    correctedWidth(width) {
      return (width) * this.widthFactor + 20
    }
    ,
    storedAlphaEqualsCurrent(d, store) {
      let storedAlpha = String(store.getters.alpha)
      let currentAlpha = String(d.target.__data__[1])
      return storedAlpha === currentAlpha;
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
