<template>
  <ViewHeader :title='"Cluster join tree"' :branch="true" :trash="true" :trash-callback="trashCallback"
              :parent=parent @maximize="maximize"></ViewHeader>
  <div id="network_pane">
    <div id="spinner" v-if="$store.getters.loadingNetwork">
      <ScaleLoader v-if="$store.getters.loadingNetwork"></ScaleLoader>
    </div>
  </div>
</template>

<script>
import * as d3 from "d3";
import ScaleLoader from 'vue-spinner/src/ScaleLoader.vue'
import ViewHeader from "./utils/ViewHeader.vue";

let rects = []
let circles = []
export default {
  name: "Network",
  props: ['network', 'parent'],
  components: {
    ScaleLoader,
    ViewHeader
  },
  watch: {
    network: function (network) {
      let parent = document.getElementById(this.parent)

      if (!parent) {
        parent = document.getElementById('main')
      }

      const margin = {top: 10, right: 10, bottom: 50, left: 20},
          width = parent.clientWidth - margin.left - margin.right,
          height = parent.clientHeight - margin.top - margin.bottom;

      let rect = {
        opacity: 0.2
      }

      const svg = d3.select("#network_pane")
          .append("svg")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
          .on("mousedown", mousedown)
          .on("mouseup", mouseup);

      function mousedown(event, d) {
        var m = d3.pointer(event);

        rect = svg.append("rect")
            .attr("x", m[0])
            .attr("y", m[1])
            .attr("fill", "lightgrey")
            .attr("stroke", "grey")
            .style("opacity", 0.2)
            .attr("height", 0)
            .attr("width", 0)
            .on("contextmenu", function (event, d) {
              event.preventDefault();
              let cur = d3.select(this).remove()

              rects.filter(function (ele) {
                if (ele != cur) {
                  console.log("REMOVED ELEMENT")
                } else {
                  console.log("DELETED!")
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

            if (minX <= circBox.x && circBox.x <= maxX && minY <= circBox.y && circBox.y <= maxY) {
              circle.attr("fill", "green")
            }
          })
        });
      }

      // create a tooltip
      var Tooltip = d3.select("#network_pane")
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
            .attr("x1", pos1[0] + 30)
            .attr("y1", pos1[1] + 30)
            .attr("x2", pos2[0] + 30)
            .attr("y2", pos2[1] + 30)
            .on("mouseover", tmouseover)
            .on("mousemove", tmousemove)
            .on("mouseleave", tmouseleave);
      }
      ;

      for (const [node, location] of Object.entries(network.pos)) {
        circles.push(svg.append("circle")
            .attr("fill", '#69b3a2')
            .attr("stroke", "none")
            .attr("cx", location[0] + 30)
            .attr("cy", location[1] + 30)
            .attr("r", 10));
      }

      let drag = d3.drag().on("drag", dragmove);

      let slider = svg.append('g').call(drag);

      slider.append('line')
          .style("stroke-dasharray", ("3, 3"))
          .style("stroke", "grey")
          .style("stroke-width", 2)
          .attr("x1", 0 - margin.left)
          .attr("y1", height + margin.top)
          .attr("x2", width + margin.left)
          .attr("y2", height + margin.top);

      slider.append("circle")
          .attr("fill", "lightgrey")
          .attr("stroke", "grey")
          .attr("cx", width + margin.left)
          .attr("cy", height + margin.top)
          .attr("r", 10);

      function dragmove(event, d) {
        d3.select(this).select('circle')
            .attr("cy", Math.min(height + margin.top, Math.max(0, event.y)))
        d3.select(this).select('line')
            .attr("y1", Math.min(height + margin.top, Math.max(0, event.y)))
            .attr("y2", Math.min(height + margin.top, Math.max(0, event.y)))
      };
    }
  },
  methods: {
    trashCallback() {
      console.log("Hello")
      rects.forEach(curRect => {
        curRect.node().remove();
      })
      circles.forEach(circle => {
        circle.attr("fill", '#69b3a2')
      })
      rects = []
    },
    maximize() {
      this.$emit('maximize')
    }
  }
}


</script>

<style scoped>
</style>
