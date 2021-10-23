<template>
  <ViewHeader :title='"Hertzsprung-Russel Diagram"' :parent=parent></ViewHeader>
  <div :id="PANE_NAME"></div>
  <select id="selectX">
    <option value="" disabled selected>Magnitude</option>
  </select>
  <select id="selectY">
    <option value="" disabled selected>Spectral Class</option>
  </select>
  <div id="spinner" v-if="$store.getters.loadingHrd">
    <ScaleLoader v-if="$store.getters.loadingHrd"></ScaleLoader>
  </div>
</template>

<script>
import ScaleLoader from 'vue-spinner/src/ScaleLoader.vue'
import ViewHeader from "../../nav/ViewHeader.vue";
import * as d3 from "d3";
import {updateHrd,} from "../../../services/datasource";

const PANE_NAME = "hrd"

export default {
  name: "HRD",
  props: ['plotData', 'parent', 'selections'],
  components: {
    ScaleLoader,
    ViewHeader
  },
  data: function () {
    return {
      PANE_NAME: PANE_NAME
    }
  },
  watch: {
    plotData: function (data) {
      this.draw(data)
    },
    selections: function () {
      this.draw(this.$store.getters.hrd)
    }
  },
  methods: {
    draw(data) {
      d3.select("#" + PANE_NAME).selectAll("svg").remove();

      let parent = document.getElementById(this.parent)

      if (!parent) {
        parent = document.getElementById('main')
      }

      const margin = {top: 10, right: 10, bottom: 75, left: 30},
          width = parent.clientWidth - margin.left - margin.right,
          height = parent.clientHeight - margin.top - margin.bottom;

      let allColumns = this.$store.getters.resourceHeaders;

      d3.select("#selectX")
          .selectAll('myOptions')
          .data(allColumns)
          .enter()
          .append('option')
          .text(function (d) {
            return d;
          }) // text showed in the menu
          .attr("value", function (d) {
            return d;
          }) // corresponding value returned by the button

      d3.select("#selectY")
          .selectAll('myOptions')
          .data(allColumns)
          .enter()
          .append('option')
          .text(function (d) {
            return d;
          }) // text showed in the menu
          .attr("value", function (d) {
            return d;
          }) // corresponding value returned by the button

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
          .style("fill", "#587e1a")

      let self = this;
      d3.select("#selectX").on("change", function (d) {
        let selection = self.getSelection()
        selection.x = this.value
        self.updateSelection(selection)
      })

      d3.select("#selectY").on("change", function (d) {
        let selection = self.getSelection()
        selection.y = this.value
        self.updateSelection(selection)
      })
    },
    getSelection() {
      return this.$store.getters.hrdSelection
    },
    updateSelection(selection) {
      this.$store.commit('updateHrdSelection', selection)
      updateHrd(this.$store.getters.currentResource);
    },
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