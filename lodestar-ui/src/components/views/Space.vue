<template>
  <ViewHeader :title='"Three space features clustering"' :parent=parent :drawPolygon="true" :disease="true"
              @maximize="maximize" @updateNet="updateNet" @updateScatter="updateScatter" @redraw="redraw"></ViewHeader>
  <div id="space_pane">
    <div id="spinner" v-if="$store.getters.loadingSpace">
      <ScaleLoader v-if="$store.getters.loadingSpace"></ScaleLoader>
    </div>
  </div>
</template>

<script>
import ScaleLoader from 'vue-spinner/src/ScaleLoader.vue'
import ViewHeader from "./utils/ViewHeader.vue";

export default {
  name: "SpacePlot",
  props: ['spaceData', 'parent', 'drawNet', 'drawScatter'],
  components: {
    ScaleLoader,
    ViewHeader
  },
  watch: {
    spaceData: function (spaceData) {
      this.redraw(spaceData)
    },
    drawNet: function () {
      this.redraw(this.$store.getters.spaceData)
    },
    drawScatter: function () {
      this.redraw(this.$store.getters.spaceData)
    }
  },
  methods: {
    maximize() {
      this.$emit('maximize')
    },
    updateNet() {
      this.$store.commit('updateDrawSpaceNet', !this.$store.getters.drawSpaceNet)
    },
    updateScatter() {
      this.$store.commit('updateDrawSpaceScatter', !this.$store.getters.drawSpaceScatter)
    },
    redraw(spaceData) {
      let parent = document.getElementById(this.parent)

      if (!parent) {
        parent = document.getElementById('main')
      }

      const margin = {top: 0, right: 10, bottom: 30, left: 0},
          width = parent.clientWidth - margin.left - margin.right,
          height = parent.clientHeight - margin.top - margin.bottom;

      let data = []
      let dataX = []
      let dataY = []
      let dataZ = []

      for (let i = 0; i < spaceData.length; i++) {
        let row = spaceData[i];
        dataX.push(row.x)
        dataY.push(row.y)
        dataZ.push(row.z)
      }

      if (this.drawScatter) {
        data.push({
          x: dataX,
          y: dataY,
          z: dataZ,
          mode: 'markers',
          type: 'scatter3d',
          marker: {
            color: 'rgb(23, 190, 207)',
            size: 2
          }
        }, {
          alphahull: 7,
          opacity: 0.1,
          type: 'mesh3d',
          x: dataX,
          y: dataY,
          z: dataZ
        })
      }

      if (this.drawNet) {
        data.push({
          x: dataX,
          y: dataY,
          z: dataZ,
          mode: 'lines',
          marker: {
            color: '#1f77b4',
            size: 12,
            symbol: 'circle',
            line: {
              color: 'rgb(0,0,0)',
              width: 0
            }
          },
          line: {
            color: '#1f77b4',
            width: 1
          },
          type: 'scatter3d'
        })
      }

      var layout = {
        autosize: true,
        height: height,
        margin: {
          l: 0,
          r: 0,
          b: 0,
          t: 0,
          pad: 0
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

      Plotly.react('space_pane', data, layout);
    }
  }
}

</script>

<style scoped>
</style>