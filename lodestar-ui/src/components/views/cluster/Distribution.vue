<template>
  <div id="distribution_plane">
    <ViewHeader :title='"Noise vs. Cluster Distribution"' :parent=parent @maximize="maximize"></ViewHeader>
  </div>
</template>

<script>
import * as d3 from "d3";
import ScaleLoader from 'vue-spinner/src/ScaleLoader.vue'
import ViewHeader from "../../nav/ViewHeader.vue";
import jStat from 'jstat'

export default {
  name: "Distribution",
  props: ['parent'],
  components: {
    ScaleLoader,
    ViewHeader
  },
  mounted() {
    let parent = document.getElementById(this.parent)

    if(!parent) {
      parent = document.getElementById('main')
    }

    const margin = {top: 10, right: 10, bottom: 50, left: 20},
        width = parent.clientWidth - margin.left - margin.right,
        height = parent.clientHeight - margin.top - margin.bottom;

    let array1 = this.random_normal_dist(60, 14);
    let array2 = this.random_normal_dist(30, 8);

    var x = d3.scaleLinear()
        .rangeRound([0, width]);

    //Min q
    var d1 = d3.min(array1, function (d) {
      return d.q;
    });
    var d2 = d3.min(array2, function (d) {
      return d.q;
    });
    var min_d = d3.min([d1, d2]);

    //Max q
    d1 = d3.max(array1, function (d) {
      return d.q;
    });
    d2 = d3.max(array2, function (d) {
      return d.q;
    });
    var max_d = d3.max([d1, d2]);

    //Max p
    d1 = d3.max(array1, function (d) {
      return d.p;
    });
    d2 = d3.max(array2, function (d) {
      return d.p;
    });
    var max_p = d3.max([d1, d2]);

    x.domain([min_d, max_d]).nice;

    var y = d3.scaleLinear()
        .domain([0, max_p])
        .range([height, 0]);

    x.domain([min_d, max_d]).nice;

    const svg = d3.select("#distribution_plane")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    let gX = svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

    let line = d3.line()
        .x(function (d) {
          return x(d.q);
        })
        .y(function (d) {
          return y(d.p);
        });

    svg.append("text")
        .attr("x", 265)
        .attr("y", height / 2 + 30)
        .attr("dy", ".35em")
        .text("Cluster")

    svg.append("text")
        .attr("x", 125)
        .attr("y", height / 2 + 30)
        .attr("dy", ".35em")
        .text("Noise")

    svg.append("path")
        .datum(array1)
        .attr("class", "line")
        .attr("d", line)
        .style("fill", "#fdae61")
        .style("opacity", "0.5");

    svg.append("path")
        .datum(array2)
        .attr("class", "line")
        .attr("d", line)
        .style("fill", "#4393c3")
        .style("opacity", "0.5");

    let drag = d3.drag().on("drag", dragmove);

    let slider = svg.append('g').call(drag);

    slider.append('line')
        .style("stroke-dasharray", ("3, 3"))
        .style("stroke", "grey")
        .style("stroke-width", 2)
        .attr("x1", 218)
        .attr("y1", height)
        .attr("x2", 218)
        .attr("y2", 0);

    slider.append("circle")
        .attr("fill", "lightgrey")
        .attr("stroke", "grey")
        .attr("cx", 218)
        .attr("cy", height)
        .attr("r", 10);

    function dragmove(event, d) {
      d3.select(this).select('circle')
          .attr("cx", Math.min(280, Math.max(100, event.x)))
      d3.select(this).select('line')
          .attr("x1", Math.min(280, Math.max(100, event.x)))
          .attr("x2", Math.min(280, Math.max(100, event.x)))
    };
  },
  methods: {
    random_normal_dist: function (mean, sd) {
      let data = [];
      for (let i = mean - 4 * sd; i < mean + 4 * sd; i += 1) {
        let q = i
        let p = jStat.normal.pdf(i, mean, sd);
        let arr = {
          "q": q,
          "p": p
        }
        data.push(arr);
      }
      ;
      return data;
    },
    maximize() {
      this.$emit('maximize')
    }
  }
}


</script>

<style scoped>

.line {
  stroke: #000;
  stroke-width: 1.5px;
}

.axis path,
.axis line {
  fill: none;
  stroke: #000;
  shape-rendering: crispEdges;
}
</style>