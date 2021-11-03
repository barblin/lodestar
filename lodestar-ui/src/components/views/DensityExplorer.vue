<template>
  <ViewHeader :title='"Density Navigation"' :branch="true" :trash="true"
              :trash-callback="trashCallback" :alpha="true" :exclude="true" :include="true"
              :parent=parent></ViewHeader>
  <div :id="PANE_NAME">
    <div id="spinner" v-if="$store.getters.loadingNetwork">
      <ScaleLoader v-if="$store.getters.loadingNetwork"></ScaleLoader>
    </div>
  </div>
</template>

<script>
import * as d3 from "d3";
import ScaleLoader from 'vue-spinner/src/ScaleLoader.vue'
import ViewHeader from "../nav/ViewHeader.vue";
import {modes} from "../../services/modes"

const PANE_NAME = "network_pane"

let rects = []
let rect = {
  opacity: 0.2
}
let circles = []
export default {
  name: "DensityExplorer",
  props: ['networkData', 'parent'],
  data: function () {
    return {
      PANE_NAME: PANE_NAME
    }
  },
  components: {
    ScaleLoader,
    ViewHeader
  },
  mounted() {
    if (this.$store.getters.networkData) {
      this.redraw(this.$store.getters.networkData)
    }
  },
  computed: {
    networkData: function () {
      this.redraw(this.$store.getters.networkData)
    }
  },
  watch: {
    networkData: function () {
      this.redraw(this.$store.getters.networkData)
    },
    parent: function () {
      this.redraw(this.$store.getters.networkData)
    }
  },
  methods: {
    redraw(network) {
      d3.select("#" + PANE_NAME).selectAll("svg").remove();

      let parent = document.getElementById(this.parent)

      if (!parent) {
        parent = document.getElementById('main')
      }

      const margin = {top: 10, right: 20, bottom: 30, left: 10},
          width = parent.clientWidth - margin.left - margin.right,
          height = parent.clientHeight - margin.top - margin.bottom;

      let heightFactor = this.percentChange(network.max_y, height);
      let widthFactor = this.percentChange(network.max_x, width)

      const svg = d3.select("#" + PANE_NAME)
          .append("svg")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
          .on("mousedown", mousedown)
          .on("mouseup", mouseup);

      let store = this.$store;

      function mousedown(event, d) {
        var m = d3.pointer(event);

        let color = store.getters.selectInclude ? "lightgreen" : "red"
        rect = svg.append("rect")
            .attr("x", m[0])
            .attr("y", m[1])
            .attr("fill", color)
            .attr("stroke", "grey")
            .style("opacity", 0.2)
            .attr("height", 0)
            .attr("width", 0)
            .on("contextmenu", function (event, d) {
              event.preventDefault();
              let cur = d3.select(this).remove()

              rects.filter(function (ele) {
                if (ele != cur) {
                } else {
                }

                return ele != cur;
              })
            });
        ;
        svg.on("mousemove", mousemove);
      }

      function mousemove(event, d) {
        var m = d3.pointer(event);

        rect.attr("width", Math.max(0, m[0] - +rect.attr("x")))
            .attr("height", Math.max(0, m[1] - +rect.attr("y")));
      }

      function mouseup(event) {
        svg.on("mousemove", null);
        rects.push(rect)

        circles.forEach(circle => {
          circle.attr("fill", '#69b3a2')
          rects.forEach(curRect => {
            let circBox = circle.node().getBBox();
            let rectBox = curRect.node().getBBox();

            let minX = rectBox.x
            let maxX = rectBox.x + rectBox.width

            let minY = rectBox.y
            let maxY = rectBox.y + rectBox.height

            let color = curRect.attr("fill") == "red" ? "red" : "green"
            if (minX <= circBox.x && circBox.x <= maxX && minY <= circBox.y && circBox.y <= maxY) {
              circle.attr("fill", color)
            }
          })
        });
      }

      // create a tooltip
      var Tooltip = d3.select("#" + PANE_NAME)
          .append("div")
          .style("opacity", 0)
          .attr("class", "tooltip")
          .style("background-color", "white")
          .style("float", "left")
          .style("position", "relative")
          .style("border", "solid")
          .style("border-width", "2px")
          .style("border-radius", "5px")

      // Three function that change the tooltip when user hover / move / leave a cell
      var tmouseover = function (d) {
        Tooltip
            .style("opacity", 1)
        d3.select(this)
            .style("stroke", "black")
            .style("opacity", 1)
      }
      var tmousemove = function (event, d) {
        var m = d3.pointer(event);
        Tooltip
            .html("Similarity: " + Math.random() * 6)
            .style("top", m[1] - parent.clientHeight + "px")
            .style("left", m[0] + "px")
      }
      var tmouseleave = function (d) {
        Tooltip
            .style("opacity", 0)
      }

      for (const [start, end] of Object.entries(network.edges)) {
        let pos1 = network.pos[start]
        let pos2 = network.pos[end]

        let simi = Math.random() * 6
        svg.append('line')
            .style("stroke", "black")
            .style("stroke-width", simi)
            .attr("x1", (pos1[0] + 5) * widthFactor)
            .attr("y1", (pos1[1] + 10) * heightFactor)
            .attr("x2", (pos2[0] + 5) * widthFactor)
            .attr("y2", (pos2[1] + 10) * heightFactor)
            .on("mouseover", tmouseover)
            .on("mousemove", tmousemove)
            .on("mouseleave", tmouseleave);
      }
      ;

      let heights = new Set();
      for (const [node, location] of Object.entries(network.pos)) {
        heights.add(location[1])

        circles.push(svg.append("circle")
            .attr("fill", '#69b3a2')
            .attr("stroke", "none")
            .attr("cx", (location[0] + 5) * widthFactor)
            .attr("cy", (location[1] + 10) * heightFactor)
            .attr("r", 8)
            .on("click", () => this.selectCluster())
            .on("mouseover", function (d) {

              d3.select(this).style("cursor", "pointer").attr("fill", '#ccac00');
            })
            .on("mouseout", function (d) {
              d3.select(this).style("cursor", "default").attr("fill", '#69b3a2');
            }));
      }

      let level = 0;
      for (let curHeight of heights) {
        svg.append('line')
            .style("stroke-dasharray", ("3, 3"))
            .style("stroke", "grey")
            .style("stroke-width", 1)
            .attr("x1", 0)
            .attr("y1", (curHeight - 25) * heightFactor)
            .attr("x2", parent.clientWidth)
            .attr("y2", (curHeight - 25) * heightFactor)

        svg.append("text")
            .attr("x", 2)
            .attr("y", (curHeight + 10) * heightFactor)
            .attr("dy", ".35em")
            .text(function (d) {
              return level;
            });

        ;

        level += 1
      }

      let drag = d3.drag().on("drag", dragmove);

      let slider = svg.append('g').call(drag);

      slider.append('line')
          .style("stroke", ("3, 3"))
          .style("stroke", "grey")
          .style("stroke-width", 2)
          .attr("x1", 0 - margin.left)
          .attr("y1", height)
          .attr("x2", parent.clientWidth)
          .attr("y2", height);

      svg.append('g').append('line')
          .style("stroke", ("3, 3"))
          .style("stroke", "grey")
          .style("stroke-width", 2)
          .attr("x1", 15)
          .attr("y1", 0)
          .attr("x2", 15)
          .attr("y2", height + margin.top);

      slider.append("circle")
          .attr("fill", "lightgrey")
          .attr("stroke", "grey")
          .attr("cx", parent.clientWidth - 10)
          .attr("cy", height)
          .attr("r", 10)
          .on("mouseover", function (d) {
            d3.select(this).style("cursor", "pointer").attr("fill", '#ccac00');
          })
          .on("mouseout", function (d) {
            d3.select(this).style("cursor", "default").attr("fill", '#69b3a2');
          });

      function dragmove(event, d) {
        d3.select(this).select('circle')
            .attr("cy", Math.min(height, Math.max(10, event.y)))
        d3.select(this).select('line')
            .attr("y1", Math.min(height, Math.max(10, event.y)))
            .attr("y2", Math.min(height, Math.max(10, event.y)))
      };
    },
    trashCallback() {
      rects.forEach(curRect => {
        curRect.node().remove();
      })
      circles.forEach(circle => {
        circle.attr("fill", '#69b3a2')
      })
      rects = []
    },
    selectCluster() {
      this.$store.commit('updateCurrentMode', modes.CLUSTER)
    },
    percentChange(solution, screen) {
      if (solution < screen) {
        return screen / solution
      } else if (screen < solution) {
        return screen / solution;
      }

      return -1
    }
  }
}


</script>

<style scoped>
</style>
