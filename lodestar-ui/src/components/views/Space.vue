<template>
   <div :id="PANE_NAME" class="default">
    <div id="spinner" v-if="$store.getters.loadingSpace">
      <ScaleLoader v-if="$store.getters.loadingSpace"></ScaleLoader>
    </div>
  </div>
</template>

<script>
import ScaleLoader from 'vue-spinner/src/ScaleLoader.vue'
import ViewHeader from "../nav/ViewHeader.vue";
import {modes} from "../../services/modes";
import {col_map} from "../../services/colors";
import * as d3 from "d3";

const PANE_NAME = "space_pane"

export default {
  name: "SpacePlot",
  props: ['spaceData', 'parent', 'drawNet', 'drawScatter', 'magnify', 'colorLabels'],
  components: {
    ScaleLoader,
    ViewHeader
  },
  mounted() {
    if (this.$store.getters.spaceData) {
      this.redraw(this.$store.getters.spaceData)
    }
  },
  data: function () {
    return {
      PANE_NAME: PANE_NAME,
      colors: col_map
    }
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
    },
    colorLabels: function () {
      this.redraw(this.$store.getters.spaceData)
    },
    magnify: function () {
      if (this.$store.getters.inspectCluster) {
        document.getElementById(PANE_NAME).className += ' magnify';
      } else {
        document.getElementById(PANE_NAME).className = document.getElementById(PANE_NAME).className.replace('magnify', '');
      }
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
      d3.select("#" + PANE_NAME).selectAll("svg").remove();

      let parent = document.getElementById(this.parent)

      if (!parent) {
        parent = document.getElementById('main')
      }

      const margin = {top: 20, right: 10, bottom: -20, left: 0},
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
            color: this.colorLabels,
            size: 2
          }
        }, /*{
          alphahull: 7,
          opacity: 0.1,
          type: 'mesh3d',
          x: dataX,
          y: dataY,
          z: dataZ
        }*/)
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

      Plotly.react(PANE_NAME, data, layout);

      let myDiv = document.getElementById(PANE_NAME);

      const store = this.$store
      myDiv.on('plotly_click', function (data) {
        if (store.getters.inspectCluster == true) {
          store.commit('updateInspectCluster', !store.getters.inspectCluster)
          store.commit('updateCurrentMode', modes.CLUSTER)
        }
      });
    }
  }
}

</script>

<style scoped>
.magnify {
  cursor: zoom-in;
}

.default {
}
</style>