<template>
  <div :id="PANE_NAME"></div>
  <div id="spinner" v-if="$store.getters.loadingVelocity">
    <ScaleLoader v-if="$store.getters.loadingVelocity"></ScaleLoader>
  </div>
</template>

<script>
import ScaleLoader from 'vue-spinner/src/ScaleLoader.vue'
import ViewHeader from "../../nav/ViewHeader.vue";
import * as d3 from "d3";
import {col_map} from "../../../services/colors";

const PANE_NAME = "histogram"

export default {
  name: "Histogram",
  props: ['plotData', 'parent', 'labels'],
  components: {
    ScaleLoader,
    ViewHeader
  },
  mounted() {
    this.draw(this.$store.getters.velocityScatterData);
  },
  data: function () {
    return {
      PANE_NAME: PANE_NAME
    }
  },
  watch: {
    plotData: function (data) {
      this.draw(data)
    }
  },
  methods: {
    draw(data) {
      if(data === undefined || data === null){
        return
      }

      d3.select("#" + PANE_NAME).selectAll("svg").remove();

      let parent = document.getElementById(this.parent)

      if (!parent) {
        parent = document.getElementById('main')
      }

      let minx = 0;
      let maxx = 0;
      let miny = 0;
      let maxy = 0;
      let minz = 0;
      let maxz = 0;

      let dataX = []
      let dataY = []
      let dataZ = []

      for (let i = 0; i < data.length; i++) {
        let row = data[i];

        if (this.labels[i] == 'rgba(162,162,162,0)') {
          continue
        }

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

        if (row.z < minz) {
          minz = row.z
        }

        if (maxz < row.z) {
          maxz = row.z
        }

        dataX.push(row.x)
        dataY.push(row.y)
        dataZ.push(row.z)
      }

      this.histogram(dataX, minx, maxx, parent.clientWidth, 10, 15, 'v_alpha')
      this.histogram(dataY, miny, maxy, parent.clientWidth, 10, 15, 'v_delta')
      this.histogram(dataZ, minz, maxz, parent.clientWidth, 10, 25, 'radial')
    },
    histogram(data, min, max, parentWidth, marginTop, marginBottom, label) {
      const margin = {top: marginTop, right: 20, bottom: marginBottom, left: 40},
          width = parentWidth - margin.left - margin.right,
          height = 130 - margin.top - margin.bottom;

      const svg = d3.select("#" + PANE_NAME)
          .append("svg")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
          .append("g")
          .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");

      var x = d3.scaleLinear()
          .domain([min, max])     // can use this instead of 1000 to have the max of data: d3.max(data, function(d) { return +d.price })
          .range([0, width]);
      svg.append("g")
          .attr("transform", "translate(0," + height + ")")
          .call(d3.axisBottom(x));

      // set the parameters for the histogram
      var histogram = d3.histogram()
          .value(function (d) {
            return d;
          })   // I need to give the vector of value
          .domain(x.domain())  // then the domain of the graphic
          .thresholds(x.ticks(70)); // then the numbers of bins

      // And apply this function to data to get the bins
      var bins = histogram(data);

      // Y axis: scale and draw:
      var y = d3.scaleLinear()
          .range([height, 0]);
      y.domain([0, d3.max(bins, function (d) {
        return d.length;
      })]);   // d3.hist has to be called before the Y axis obviously

      let leftAxis = d3.axisLeft(y).ticks(5, "f")
      svg.append("g")
          .call(leftAxis);

      // append the bar rectangles to the svg element
      let color = col_map[0]
      if (this.$store.getters.levelSet[this.$store.getters.currentCluster.level]
          [this.$store.getters.currentCluster.label] !== undefined) {
        color = this.$store.getters.levelSet[this.$store.getters.currentCluster.level]
            [this.$store.getters.currentCluster.label].color
      }
      svg.selectAll("rect")
          .data(bins)
          .enter()
          .append("rect")
          .attr("x", 1)
          .attr("transform", function (d) {
            return "translate(" + x(d.x0) + "," + y(d.length) + ")";
          })
          .attr("width", function (d) {
            return x(d.x1) - x(d.x0) - 1;
          })
          .attr("height", function (d) {
            return height - y(d.length);
          })
          .style("fill", color)
    }
  }
}

</script>

<style scoped>
select {
  width: 40%;
  margin-right: 10px;
  margin-left: 5px;
}
</style>