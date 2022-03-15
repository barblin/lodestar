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

const PANE_NAME = "alpha_pane"

export default {
  name: "Alpha",
  props: ['parent', 'significantRoots', 'maxX'],
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
      console.log("registered significant roots")
      console.log(data)
      this.redraw(data)
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

      this.createLevelLines(parent, this.$store.getters.alphas)
      this.createSignificantRootsLines(parent, significantRoots, this.$store.getters.alphas, this.$store)
      this.createLevelButtons(this.$store.getters.alphas, this.$store, parent)
    },
    createLevelLines(parent, alphas) {
      let single = parent.clientHeight / alphas.length
      let multiples = []

      for (let i = 0; i < alphas.length - 1; i++) {
        multiples.push((i + 1))
        console.log("Hello")
      }

      return this.svg.append('g')
          .selectAll("line")
          .data(multiples)
          .enter()
          .append('line')
          .style("stroke-dasharray", ("3, 3"))
          .style("stroke", "grey")
          .style("stroke-width", 1)
          .attr("x1", 0)
          .attr("y1", (d) => d * single)
          .attr("x2", parent.clientWidth)
          .attr("y2", (d) => d * single);
    },
    createLevelButtons(alphas, store, parent) {
      let multiples = []

      let single = parent.clientHeight / alphas.length

      for (let i = 0; i < alphas.length; i++) {
        multiples.push(([i, alphas[i]]))
      }

      let context = this;

      return this.svg.append('g')
          .selectAll("line")
          .data(multiples)
          .enter()
          .append("line")
          .style("stroke", ("3, 3"))
          .style("stroke", (d) => {
            console.log(d)
            if (String(d[1]) === String(store.getters.alpha)) {
              return '#ccac00'
            } else {
              return "rgba(105,179,162,0.80)"
            }
          })
          .style("stroke-width", 15)
          .attr("x1", 7)
          .attr("y1", (d) => (d[0] * single))
          .attr("x2", 7)
          .attr("y2", (d) => (d[0] * single) + single)
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
              store.commit('updateAlpha', d.target.__data__[1])
              getCurrentTree();
              updateCurrentLabels({
                level: store.getters.level,
                alpha: store.getters.alpha
              })
            }
            d3.select(this).style("stroke", "rgba(105,179,162,0.80)");
          })
    },
    createSignificantRootsLines(parent, significantRoots, alphas, store) {
      let roots = Object.values(significantRoots)

      let multiples = []
      let multiplesAlpha = []

      let singleWidth = (parent.clientWidth - 14) / roots.length
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
            return (singleWidth * d[0]) + 14
          })
          .attr("y1", 0)
          .attr("x2", (d) => {
            let correctedWidth = (singleWidth * d[0]) + 14
            return correctedWidth;
          })
          .attr("y2", parent.clientHeight);

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
            .attr("cx", (d) => d[0] * singleWidth + (singleWidth / 2) + 14)
            .attr("cy", (d) => multi[0] * singleHeight + (singleHeight / 2))
            .attr("r", 6)
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
