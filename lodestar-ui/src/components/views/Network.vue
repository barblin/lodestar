<template>
  <div id="network_pane" class="simple-plot">
    <ViewHeader :title='"Cluster join tree"'></ViewHeader>
    <div id="spinner" v-if="$store.getters.loadingNetwork">
      <ScaleLoader v-if="$store.getters.loadingNetwork"></ScaleLoader>
    </div>
  </div>
</template>

<script>
import * as d3 from "d3";
import ScaleLoader from 'vue-spinner/src/ScaleLoader.vue'
import ViewHeader from "./utils/ViewHeader.vue";


export default {
  name: "Network",
  props: ['network'],
  components: {
    ScaleLoader,
    ViewHeader
  },
  watch: {
    network: function (network) {
      const margin = {top: 10, right: 10, bottom: 30, left: 20},
          width = this.$store.getters.width - margin.left - margin.right,
          height = this.$store.getters.height - margin.top - margin.bottom;

      let rect = {
        opacity: 0.2
      }
      const svg = d3.select("#network_pane")
          .append("svg")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
          .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")")
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
              d3.select(this).remove()
            });;

        svg.on("mousemove", mousemove);
      }

      function mousemove(event, d) {
        var m = d3.pointer(event);

        rect.attr("width", Math.max(0, m[0] - +rect.attr("x")))
            .attr("height", Math.max(0, m[1] - +rect.attr("y")));
      }

      function mouseup(event) {
        svg.on("mousemove", null);
      }

      const x = d3.scaleLinear()
          .domain([0, 1])
          .range([0, network.max_x]);


      const y = d3.scaleLinear()
          .domain([0, 1])
          .range([network.max_y, 0]);


      for (const [start, end] of Object.entries(network.edges)) {
        let pos1 = network.pos[start]
        let pos2 = network.pos[end]

        svg.append('line')
            .style("stroke", "black")
            .style("stroke-width", 2)
            .attr("x1", pos1[0])
            .attr("y1", pos1[1])
            .attr("x2", pos2[0])
            .attr("y2", pos2[1]);
      };

      for (const [node, location] of Object.entries(network.pos)) {
        svg.append("circle")
            .attr("fill", "steelblue")
            .attr("stroke", "none")
            .attr("cx", location[0])
            .attr("cy", location[1])
            .attr("r", 10);
      }

      let drag = d3.drag().on("drag", dragmove);

      let slider = svg.append('g').call(drag);

      slider.append('line')
          .style("stroke-dasharray", ("3, 3"))
          .style("stroke", "grey")
          .style("stroke-width", 2)
          .attr("x1", 0 - margin.left)
          .attr("y1", height)
          .attr("x2", width)
          .attr("y2", height);

      slider.append("circle")
          .attr("fill", "lightgrey")
          .attr("stroke", "grey")
          .attr("cx", width)
          .attr("cy", height)
          .attr("r", 10);

      function dragmove(event, d) {
        d3.select(this).select('circle')
            .attr("cy", Math.min(height, Math.max(0, event.y)))
        d3.select(this).select('line')
            .attr("y1", Math.min(height, Math.max(0, event.y)))
            .attr("y2", Math.min(height, Math.max(0, event.y)))
      };
    }

  }
}


</script>

<style scoped>
</style>