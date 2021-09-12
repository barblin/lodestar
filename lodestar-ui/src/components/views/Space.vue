<template>
  <ViewHeader :title='"Three space features clustering"' :parent=parent @maximize="maximize"></ViewHeader>
  <div id="level_scatter_pane"></div>
</template>

<script>
import ScaleLoader from 'vue-spinner/src/ScaleLoader.vue'
import ViewHeader from "./utils/ViewHeader.vue";
import * as d3 from "d3";

export default {
  name: "SpacePlot",
  props: ['plotData', 'parent'],
  components: {
    ScaleLoader,
    ViewHeader
  },
  mounted() {
    let parent = document.getElementById(this.parent)

    if (!parent) {
      parent = document.getElementById('main')
    }

    const margin = {top: 0, right: 10, bottom: 30, left: 0},
        width = parent.clientWidth - margin.left - margin.right,
        height = parent.clientHeight - margin.top - margin.bottom;

    d3.csv('https://raw.githubusercontent.com/plotly/datasets/master/alpha_shape.csv').then(function(rows){
      function unpack(rows, key) {
        return rows.map(function(row) { return row[key]; });
      }

      var data = [{
        x: unpack(rows, 'x'),
        y: unpack(rows, 'y'),
        z: unpack(rows, 'z'),
        mode: 'markers',
        type: 'scatter3d',
        marker: {
          color: 'rgb(23, 190, 207)',
          size: 2
        }
      },{
        alphahull: 7,
        opacity: 0.1,
        type: 'mesh3d',
        x: unpack(rows, 'x'),
        y: unpack(rows, 'y'),
        z: unpack(rows, 'z')
      }];

      var layout = {
        autosize: true,
        height: height,
        margin: {
          l: 0,
          r: 0,
          b: 0,
          t: 0,
          pad: 4
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

      Plotly.react('level_scatter_pane', data, layout);
    });

  }
  ,
  methods: {
    maximize() {
      this.$emit('maximize')
    }
  }
}

</script>

<style scoped>
</style>