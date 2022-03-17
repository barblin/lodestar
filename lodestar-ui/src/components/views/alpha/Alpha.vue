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
import {percentChange} from "../../../services/views";
import {getCurrentTree, updateCurrentLabels} from "../../../services/datasource";
import {createLevelLabels} from "../../../services/d3-tools";

const PANE_NAME = "alpha_pane"

export default {
  name: "Alpha",
  props: ['parent', 'significantRoots', 'maxX', 'clusterLabel'],
  data: function () {
    return {
      PANE_NAME: PANE_NAME,
      svg: {},
      widthFactor: 1,
    }
  },
  components: {
    ScaleLoader
  },
  mounted() {
    this.redraw(this.$store.getters.significantRoots)
  },
  watch: {
    significantRoots: function (data) {
      this.redraw(data)
    },
    clusterLabel: function () {
      this.redraw(this.$store.getters.significantRoots)
    },
  },
  methods: {
    redraw(significantRoots) {
      d3.select("#" + PANE_NAME).selectAll("svg").remove();

      let parent = document.getElementById(this.parent)

      const margin = {top: 0, right: 20, bottom: 0, left: 10},
          width = parent.clientWidth - margin.left - margin.right,
          height = parent.clientHeight - margin.top - margin.bottom;

      this.widthFactor = percentChange(this.maxX, width)

      this.svg = d3.select("#" + PANE_NAME)
          .append("svg")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top);

      let multiples = []
      let single = parent.clientHeight / this.$store.getters.alphas.length

      for (let i = 0; i < this.$store.getters.alphas.length; i++) {
        multiples.push([(i + 1) * single, this.$store.getters.alphas[i]])
      }

      this.createLevelLines(parent, multiples)
      this.createSignificantRootsLines(parent, significantRoots, this.$store.getters.alphas, this.$store)
      this.createLevelButtons(this.$store, multiples, single)
      createLevelLabels(this.svg, multiples, single/2)
    },
    createLevelLines(parent, multiples) {
      return this.svg.append('g')
          .selectAll("line")
          .data(multiples)
          .enter()
          .append('line')
          .style("stroke-dasharray", ("3, 3"))
          .style("stroke", "grey")
          .style("stroke-width", 1)
          .attr("x1", 0)
          .attr("y1", (d) => d[0])
          .attr("x2", parent.clientWidth)
          .attr("y2", (d) => d[0]);
    },
    createLevelButtons(store, multiples, single) {
      let context = this;

      return this.svg.append('g')
          .selectAll("line")
          .data(multiples)
          .enter()
          .append("line")
          .attr("class", "alphaButtons")
          .style("stroke", ("3, 3"))
          .style("stroke", (d) => {
            if (String(d[1]) === String(store.getters.alpha)) {
              return 'rgba(0,255,0,0.67)'
            } else {
              return "rgba(105,179,162,0.80)"
            }
          })
          .style("stroke-width", 58)
          .attr("x1", 7)
          .attr("y1", (d) => (d[0]) - single)
          .attr("x2", 7)
          .attr("y2", (d) => (d[0]))
          .on("mouseover", function (d) {
            if (!context.storedAlphaEqualsCurrent(d, store)) {
              d3.select(this).style("cursor", "pointer");
              d3.select(this).style('stroke', '#ccac00');
            }
          })
          .on("mouseout", function (d) {
            if (!context.storedAlphaEqualsCurrent(d, store)) {
              d3.select(this).style("stroke", "rgba(105,179,162,0.80)");
            }
          })
          .on("click", function (d) {
            if (!context.storedAlphaEqualsCurrent(d, store)) {
              d3.selectAll('.alphaButtons').style("stroke", "rgba(105,179,162,0.80)")


              store.commit('updateAlpha', d.target.__data__[1])
              getCurrentTree();
              updateCurrentLabels({
                level: store.getters.level,
                alpha: store.getters.alpha
              })

              d3.select(this).style("stroke", "rgba(0,255,0,0.67)");
            }
          })
    },
    createSignificantRootsLines(parent, significantRoots, alphas, store) {
      let roots = Object.values(significantRoots)

      let multiples = []
      let multiplesAlpha = []

      let singleWidth = (parent.clientWidth - 36) / roots.length
      let singleHeight = parent.clientHeight / alphas.length


      for (let i = 0; i < roots.length; i++) {
        multiples.push(([i, roots[i]]))
      }

      for (let i = 0; i < alphas.length; i++) {
        multiplesAlpha.push([i, alphas[i]])
      }

      this.svg.append('g')
          .selectAll("line")
          .data(multiples)
          .enter()
          .append('line')
          .style("stroke-dasharray", ("3, 3"))
          .style("stroke", "grey")
          .style("stroke-width", 1)
          .attr("x1", (d) => {
            return (singleWidth * d[0]) + 36
          })
          .attr("y1", 0)
          .attr("x2", (d) => {
            let correctedWidth = (singleWidth * d[0]) + 36
            return correctedWidth;
          })
          .attr("y2", parent.clientHeight);

      //Container for the gradients
      var defs = this.svg.append("defs");

      //Code taken from http://stackoverflow.com/questions/9630008/how-can-i-create-a-glow-around-a-rectangle-with-svg
      //Filter for the outside glow
      var filter = defs.append("filter")
          .attr("id","glow");

      filter.append("feGaussianBlur")
          .attr("class", "blur")
          .attr("stdDeviation","3")
          .attr("result","coloredBlur");

      var feMerge = filter.append("feMerge");
      feMerge.append("feMergeNode")
      feMerge.append("feMergeNode")
          .attr("in","coloredBlur")
          .attr("in","SourceGraphic");

      let smaller = singleWidth
      if(singleHeight < singleWidth){
        smaller = singleHeight
      }

      for (const multi of multiplesAlpha) {
        this.svg.append("g")
            .selectAll("circle")
            .data(multiples)
            .enter()
            .append("circle")
            .attr("fill", (d) => {
              return store.getters.alphaColorMap[multi[1]][d[1]]
            })
            .attr("stroke", "none")
            .attr("cx", (d) => d[0] * singleWidth + (singleWidth / 2) + 36)
            .attr("cy", (d) => multi[0] * singleHeight + (singleHeight / 2))
            .attr("r", ((smaller / 2) - 2))
            .style("filter" , (d) => {

              if(d[1] === store.getters.currentCluster.label) {
                return "url(#glow)";
              }

              return ""
            });
      }
    },
    correctedWidth(width) {
      return (width) * this.widthFactor + 20
    },
    storedAlphaEqualsCurrent(d, store) {
      let storedAlpha = String(store.getters.alpha)
      let currentAlpha = String(d.target.__data__[1])
      return storedAlpha === currentAlpha;
    }
  }
}


</script>

<style scoped>
</style>
