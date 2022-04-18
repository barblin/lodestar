<template>
  <div :id="PANE_NAME">
    <div id="spinner" v-if="$store.getters.loadingAny">
      <ScaleLoader v-if="$store.getters.loadingAny"></ScaleLoader>
    </div>
  </div>
</template>

<script>
import * as d3 from "d3";
import ScaleLoader from 'vue-spinner/src/ScaleLoader.vue'
import ViewHeader from "../nav/ViewHeader.vue";
import {modes} from "../../services/modes"
import {getSignificantRoots, updateAllLabels, updateCurrentLabels} from "../../services/datasource";
import {percentChange} from "../../services/views";
import {createLevelLabels} from "../../services/d3-tools";

const PANE_NAME = "network_pane"

let circles = []
let rects = []
let rect = {
  opacity: 0.2
}

export default {
  name: "DensityExplorer",
  props: ['networkData', 'parent', 'filterForCluster'],
  data: function () {
    return {
      PANE_NAME: PANE_NAME,
      widthFactor: 1,
      heightFactor: 1,
      yScale: {},
      svg: {},
      tooltip: {}
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
    networkData: function (d) {
      this.redraw(d)
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

      const margin = {top: 10, right: 20, bottom: 0, left: 10},
          width = parent.clientWidth - margin.left - margin.right,
          height = parent.clientHeight - margin.top - margin.bottom;

      let heights = new Set();
      let remainingEdges = []
      let remainingNodes = []

      for (const [node, location] of Object.entries(network.pos)) {
        heights.add(location[1])
      }


      let max_x = network.max_x;
      let min_x = 0;

      if (this.filterForCluster) {
        max_x = 0;
        min_x = network.max_x
      }

      for (const [node, node_level_clusters] of Object.entries(network.node_level_clusters)) {
        if (this.filterForCluster) {
          if (node_level_clusters[2] === this.$store.getters.currentCluster.label) {
            if (network.edges[node] !== undefined) {
              remainingEdges.push([parseInt(node), network.edges[node]])
            }

            if (max_x < network.pos[node][0]) {
              max_x = network.pos[node][0]
            }

            if (network.pos[node][0] < min_x) {
              min_x = network.pos[node][0]
            }

            remainingNodes.push([parseInt(node), network.pos[node]])
          }

        } else {
          if (network.edges[node] !== undefined) {
            remainingEdges.push([parseInt(node), network.edges[node]])
          }
          remainingNodes.push([parseInt(node), network.pos[node]])
        }
      }

      this.heightFactor = 1 //this.percentChange(network.max_y, height);
      this.widthFactor = percentChange(max_x + min_x, width)

      this.yScale = d3.scaleLinear().domain([height, 0]).range([height, 0]);

      this.svg = d3.select("#" + PANE_NAME)
          .append("svg")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top)
          .on("mousedown", this.mousedown)
          .on("mouseup", this.mouseup);


      let level = 0;
      let heightDict = {};
      for (const h of heights) {
        heightDict[h] = level
        level += 1
      }

      let edges = this.createEdges(network, remainingEdges);
      this.tooltip = this.createTooltip();
      circles = this.createNodes(remainingNodes, network, this.$store, this.tooltip);
      let levelLines = this.createLevelLines(parent, heightDict)
      let levelButton = this.createLevelButtons(heightDict, this.$store)
      let levelLabels = createLevelLabels(this.svg, Object.entries(heightDict), -13)
      let heightFactor = this.heightFactor;

      let store = this.$store;
      let zoom = this.createZoom(store, network, edges, circles, levelLines, levelButton, levelLabels, this.yScale, heightFactor)
      this.svg.append('text')
          .attr('font-family', 'FontAwesome')
          .text(function(d) { return '\uf118' });

      this.svg.call(zoom)

    },
    createNodes(nodes, network, store, tooltip) {
      let context = this;
      let transformed_network = Object.entries(network)
      let cluster_level_info = Object.entries(transformed_network[2][1])

      return this.svg.append("g")
          .selectAll("circle")
          .data(nodes)
          .enter()
          .append("circle")
          .attr("class", "clusters")
          .attr("fill", (d) => {
            let node_index = d[0]
            let node = Object.entries(cluster_level_info[node_index][1])
            let level = node[0][1], label = node[2][1]

            if (label == store.getters.currentCluster.label &&
                level == store.getters.currentCluster.level &&
                this.filterForCluster) {
              return '#ccac00'
            }

            return store.getters.levelSet[level][label].color
          })
          .attr("stroke", "none")
          .attr("cx", (d) => this.correctedWidth(d[1][0]))
          .attr("cy", (d) => this.yScale(this.correctedHeight(d[1][1])))
          .attr("r", 6)
          .on("click", function (d) {
            if (context.filterForCluster) {
              let node = Array.from(cluster_level_info[d.target.__data__[0]][1])
              let level = node[0], label = node[2]

              d3.selectAll(".clusters").attr("fill", String(store.getters.levelSet[level][label].color));
              d3.select(this).style("cursor", "default").attr("fill", '#ccac00');
            }

            context.selectCluster(Array.from(cluster_level_info[d.target.__data__[0]][1]))
          })
          .on("mouseover", function (d) {
            d3.select(this).style("cursor", "pointer").attr("fill", '#ccac00');
            let node = Array.from(cluster_level_info[d.target.__data__[0]][1])
            let level = node[0], label = node[2]

            store.commit('updateCurrentClusterLabel', label)
            let name = store.getters.levelSet[level][label].name

            tooltip
                .html(name)
                .style("position", "absolute")
                .style("top", "0%")
                .style("left", "45%")

            tooltip.style("opacity", 1)
          })
          .on("mouseout", function (d) {
            let node = Array.from(cluster_level_info[d.target.__data__[0]][1])
            let level = node[0], label = node[2]

            d3.select(this).style("cursor", "default").attr("fill", String(store.getters.levelSet[level][label].color));
            tooltip.style("opacity", 0)
          })
    },
    createEdges(network, edges) {
      return this.svg.append('g')
          .selectAll("line")
          .data(edges)
          .enter()
          .append('line')
          .style("stroke", "black")
          .style("stroke-width", 2)
          .attr("x1", (d) => this.correctedWidth(network.pos[d[0]][0]))
          .attr("y1", (d) => this.yScale(this.correctedHeight(network.pos[d[0]][1])))
          .attr("x2", (d) => this.correctedWidth(network.pos[d[1]][0]))
          .attr("y2", (d) => this.yScale(this.correctedHeight(network.pos[d[1]][1])));
    },
    createLevelLines(parent, heights) {
      return this.svg.append('g')
          .selectAll("line")
          .data(Object.entries(heights))
          .enter()
          .append('line')
          .style("stroke-dasharray", ("3, 3"))
          .style("stroke", "grey")
          .style("stroke-width", 1)
          .attr("x1", 0)
          .attr("y1", (d) => (d[0] - 25) * this.heightFactor)
          .attr("x2", parent.clientWidth)
          .attr("y2", (d) => (d[0] - 25) * this.heightFactor);
    },
    createLevelButtons(heights, store) {
      return this.svg.append('g')
          .selectAll("line")
          .data(Object.entries(heights))
          .enter()
          .append("line")
          .attr("class", "levelButtons")
          .style("stroke", ("3, 3"))
          .style("stroke", (d) => {
            let storedLevel = String(store.getters.level);
            let currentLevel = String(d[1]);

            if (storedLevel == currentLevel) {
              return "rgba(0,255,0,0.67)";
            } else {
              return "rgba(105,179,162,0.80)";
            }
          })
          .style("stroke-width", 15)
          .attr("x1", 7)
          .attr("y1", (d) => (d[0] - 24) * this.heightFactor)
          .attr("x2", 7)
          .attr("y2", (d) => (d[0] + 46) * this.heightFactor)
          .on("mouseover", function (d) {
            let storedLevel = String(store.getters.level)
            let currentLevel = String(d.target.__data__[1])

            if (storedLevel != currentLevel) {
              d3.select(this).style("cursor", "pointer");
              d3.select(this).style('stroke', '#ccac00');
            }
          })
          .on("mouseout", function (d) {
            let storedLevel = String(store.getters.level)
            let currentLevel = String(d.target.__data__[1])

            if (storedLevel != currentLevel) {
              d3.select(this).style("stroke", "rgba(105,179,162,0.80)");
            }
          })
          .on("click", function (d) {
            let storedLevel = String(store.getters.level)
            let currentLevel = String(d.target.__data__[1])

            if (storedLevel != currentLevel) {
              d3.selectAll('.levelButtons').style("stroke", "rgba(105,179,162,0.80)")

              store.commit('updateLevel', currentLevel)
              getSignificantRoots(store.getters.level);
              updateAllLabels();
              updateCurrentLabels({
                level: store.getters.level,
                alpha: store.getters.alpha
              })
              d3.select(this).style("stroke", "rgba(0,255,0,0.67)");
            }
          })
    },
    mousemove(event, d) {
      var m = d3.pointer(event);

      rect.attr("width", Math.max(0, m[0] - +rect.attr("x")))
          .attr("height", Math.max(0, m[1] - +rect.attr("y")));
    },
    mouseup(event) {
      this.svg.on("mousemove", null);
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
    },
    dragmove(event, d) {
      d3.select(this).select('circle')
          .attr("cy", Math.min(height, Math.max(0, event.y)))
      d3.select(this).select('line')
          .attr("y1", Math.min(height, Math.max(0, event.y)))
          .attr("y2", Math.min(height, Math.max(0, event.y)))
    },
    mousedown(event, d) {
      var m = d3.pointer(event);

      let color = this.$store.getters.selectInclude ? "lightgreen" : "red"
      rect = this.svg.append("rect")
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
    },
    createTooltip() {
      return d3.select("#" + PANE_NAME)
          .append("div")
          .style("opacity", 0)
          .attr("class", "tooltip")
          .style("background-color", "white")
          .style("float", "left")
          .style("position", "relative")
          .style("border", "solid")
          .style("border-width", "1px")
          .style("border-radius", "5px")
          .style("padding-left", "15px")
          .style("padding-right", "15px")
          .style("line-height", "25px")
    },
    createZoom(store, network, edges, circles, levelLines, levelButton, levelLabels, yScale, heightFactor) {
      return d3.zoom()
          .on('zoom', function (event) {
            if (!store.getters.selectExclude) {
              var new_yScale = event.transform.rescaleY(yScale);
              circles.attr("cy", function (d) {
                return new_yScale((d[1][1] + 10) * heightFactor)
              });
              edges.attr("y1", function (d) {
                return new_yScale((network.pos[d[0]][1] + 10) * heightFactor)
              });
              edges.attr("y2", function (d) {
                return new_yScale((network.pos[d[1]][1] + 10) * heightFactor)
              });
              levelButton.attr("y1", function (d) {
                return new_yScale((d[0] - 24) * heightFactor)
              });
              levelButton.attr("y2", function (d) {
                return new_yScale((d[0] + 45) * heightFactor)
              });
              levelLines.attr("y1", function (d) {
                return new_yScale((d[0] - 25) * heightFactor)
              });
              levelLines.attr("y2", function (d) {
                return new_yScale((d[0] - 25) * heightFactor)
              });
              levelLabels.attr("y", function (d) {
                return new_yScale(parseInt(d[0]) + 13)
              });
            }
          });
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
    selectCluster(node) {
      this.$store.commit('updateErroredMain', false)

      let level = node[0], label = node[2]
      let cluster = this.$store.getters.levelSet[level][label]

      this.$store.commit('updateCurrentMode', modes.CLUSTER)
      this.$store.commit('updateCurrentClusterLabel', cluster.label)
      this.$store.commit('updateCurrentClusterName', cluster.name != null ? cluster.name : cluster.label)
      this.$store.commit('updateCurrentClusterSize', cluster.size)
      this.$store.commit('updateCurrentClusterLevel', cluster.level)
      this.$store.commit('updateLevel', cluster.level)

      updateCurrentLabels({
        level: cluster.level,
        current_cluster: cluster.label,
        alpha: this.$store.getters.alpha
      })
    },
    correctedWidth(width) {
      return (width) * this.widthFactor + 20
    },
    correctedHeight(height) {
      return (height) * this.heightFactor + 10
    },
  }
}


</script>

<style scoped>
</style>
