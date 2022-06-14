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
import {getSignificantRoots, updateAllLabels, updateCurrentLabels} from "../../services/data/datasource";
import {percentChange} from "../../services/views";
import {createLevelLabels} from "../../services/d3-tools";
import {inspect} from "../../services/cluster";
import {highlight, selected_el} from "../../services/colors";
import {correctedHeight, positionMapOf} from "../../services/layout/positions";

const PANE_NAME = "network_pane"

let rects = []
let rect = undefined

export default {
  name: "DensityExplorer",
  props: ['networkData', 'parent', 'filterForCluster', 'exclusion'],
  data: function () {
    return {
      PANE_NAME: PANE_NAME,
      widthFactor: 1,
      heightFactor: 1,
      yScale: {},
      svg: {},
      tooltip: {},
      dragtooltip: {},
      currentOffset: 0,
      isDown: false,
      zoom: null,
      currentScale: 1,
      currentHeight: 0
    }
  },
  components: {
    ScaleLoader,
    ViewHeader
  },
  mounted() {
    if (this.$store.getters.networkData) {
      this.redraw(this.$store.getters.networkData)
      this.dragtooltip = this.createDragTooltip();
    }
  },
  watch: {
    networkData: function () {
      this.redraw(this.$store.getters.networkData)
    },
    exclusion: function (data) {
      this.isDown = false;

      if (data) {
        this.svg.on(".zoom", null)
        this.svg.on("mouseup", this.mouseup)
      } else {
        this.svg.call(this.zoom);
        this.svg.on("mouseup", null)
      }
    }
  },
  methods: {
    redraw(network) {
      if (network.nodes == undefined) {
        return
      }

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
          .on("mouseover", this.mouseover)
          .on("mouseout", this.mouseout)
          .on("mousemove", this.mousemove)
          .on("mousedown", this.mousedown)
          .on("mouseup", this.mouseup)

      let level = 0;
      let heightDict = {};
      for (const h of heights) {
        heightDict[h] = level
        level += 1
      }

      let transformed_network = Object.entries(network)
      let clusterLevelInfo = Object.entries(transformed_network[2][1])

      let positionMap = positionMapOf(remainingNodes, width, clusterLevelInfo)

      let edges = this.createEdges(network, remainingEdges);
      this.tooltip = this.createTooltip();
      let circles = this.createNodes(remainingNodes, network, this.tooltip, height / 2, this.dragtooltip, positionMap, clusterLevelInfo);
      let levelLines = this.createLevelLines(parent, heightDict)
      let levelButton = this.createLevelButtons(heightDict, this.$store)
      let levelLabels = createLevelLabels(this.svg, Object.entries(heightDict), -13)
      let heightFactor = this.heightFactor;

      let store = this.$store;
      this.zoom = this.createZoom(store, network, edges, circles, levelLines, levelButton, levelLabels, this.yScale, heightFactor)
      this.svg.append('text')
          .attr('font-family', 'FontAwesome')
          .text(function (d) {
            return '\uf118'
          });

      this.svg.call(this.zoom);
      this.svg.call(this.zoom.transform, d3.zoomIdentity.translate(0, this.currentOffset));
      this.svg.on("dblclick.zoom", null)
    },
    createNodes(nodes, network, tooltip, half_height, positionMap, clusterLevelInfo) {
      let context = this;


      let store = this.$store;
      return this.svg.append("g")
          .selectAll("circle")
          .data(nodes)
          .enter()
          .append("circle")
          .attr("class", "clusters")
          .attr("fill", (d) => {
            let node_index = d[0]
            let node = Object.entries(clusterLevelInfo[node_index][1])
            let level = node[0][1], label = node[2][1]

            if (label == store.getters.currentCluster.label &&
                level == store.getters.currentCluster.level &&
                this.filterForCluster) {
              return highlight
            }

            return store.getters.levelSet[level][label].color
          })
          .attr("stroke", "none")
          .attr("cx", (d) => {
            let node_index = d[0]
            let node = Object.entries(clusterLevelInfo[node_index][1])
            let level = node[0][1], label = node[2][1]

            if (positionMap[level][label] == undefined)
              return 0

            return positionMap[level][label].posX
          })
          .attr("cy", (d) => {
            let cur_height = this.yScale(correctedHeight(d[1][1], this.heightFactor))
            let node_index = d[0]
            let node = Object.entries(clusterLevelInfo[node_index][1])
            let level = node[0][1]

            if (level == store.getters.level) {
              context.currentOffset = -cur_height + half_height
            }

            return cur_height
          })
          .attr("r", 6)
          .on("click", function (d) {
            if (!store.getters.loadingAny) {
              let node = Array.from(clusterLevelInfo[d.target.__data__[0]][1])
              let label = node[2]
              d3.select(this).style("cursor", "default").attr("fill", highlight);

              if (label != store.getters.highlightCluster) {
                store.commit('updateHighlightCluster', label)
              } else {
                store.commit('updateHighlightCluster', null)
              }
            }
          })
          .on("dblclick", function (d) {
            if (!store.getters.loadingAny) {
              if (context.filterForCluster) {
                let node = Array.from(clusterLevelInfo[d.target.__data__[0]][1])
                let level = node[0], label = node[2]

                d3.selectAll('.levelButtons').style("stroke", "rgba(105,179,162,0.80)")
                d3.selectAll('#l' + String(level)).style("stroke", selected_el);
                d3.selectAll(".clusters").attr("fill", String(store.getters.levelSet[level][label].color));
                d3.select(this).style("cursor", "default").attr("fill", highlight);
              }
              store.commit('updateHighlightCluster', null)

              context.selectCluster(Array.from(clusterLevelInfo[d.target.__data__[0]][1]))
            }
          })
          .on("mouseover", function (d) {
            d3.select(this).style("cursor", "pointer").attr("fill", highlight);
            let node = Array.from(clusterLevelInfo[d.target.__data__[0]][1])
            let level = node[0], label = node[2]

            store.commit('updateCurrentClusterLabel', label)
            let name = store.getters.levelSet[level][label].name
            let size = store.getters.levelSet[level][label].size


            tooltip
                .html("Cluster: " + name + " /  Size: " + size + "<br>Click to highlight / Dblclick to inspect")
                .style("position", "absolute")
                .style("font-size", "11px")
                .style("top", "0%")
                .style("left", "25%");


            tooltip.style("opacity", 1)
          })
          .on("mouseout", function (d) {
            let node = Array.from(clusterLevelInfo[d.target.__data__[0]][1])
            let level = node[0], label = node[2]

            if (label != store.getters.currentCluster.label ||
                level != store.getters.currentCluster.level) {
              d3.select(this).style("cursor", "default").attr("fill", String(store.getters.levelSet[level][label].color));
            }
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
          .attr("x1", (d) => {
            {
              if (this.$store.getters.clusterLookup[d[0]] == undefined) {
                return 0
              }

              return this.$store.getters.clusterLookup[d[0]].posX
            }
          })
          .attr("y1", (d) => this.yScale(correctedHeight(network.pos[d[0]][1], this.heightFactor)))
          .attr("x2", (d) => {
            {
              if (this.$store.getters.clusterLookup[d[1]] == undefined) {
                return 0
              }

              return this.$store.getters.clusterLookup[d[1]].posX
            }
          })
          .attr("y2", (d) => this.yScale(correctedHeight(network.pos[d[1]][1], this.heightFactor)));
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
              return highlight;
            } else {
              return "rgba(105,179,162,0.80)";
            }
          })
          .attr("id", (d) => {
            return 'l' + String(d[1]);
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
              d3.select(this).style('stroke', highlight);
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
            if (!store.getters.loadingAny) {
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
                d3.select(this).style("stroke", highlight);
              }
            }
          })
    },
    mousemove(event, d) {
      if (this.exclusion && this.isDown) {
        var m = d3.pointer(event);


        rect.attr("width", Math.max(0, m[0] - +rect.attr("x")))
            .attr("height", (d) => {
              d[3] = Math.max(0, m[1] - +rect.attr("y"))
              return this.yScale(d[3])
            });
      }
    },
    mouseover(event, d) {
      if (this.exclusion) {
        this.svg.style("cursor", "crosshair");
      } else {
        this.svg.style("cursor", "default");
      }
    },
    mouseout(event, d) {
      this.svg.style("cursor", "default");

      if (rect != null && rect != undefined) {
        //rect.remove()
      }
    },
    mouseup(event, d) {

      if (this.exclusion && this.isDown && rect != undefined && event.button === 0) {
        rects.push(rect)

        rect = undefined

        let circles = d3.selectAll('.clusters');
        /*circles.forEach(circle => {
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
        });*/
      }

      this.isDown = false;
    },
    mousedown(event, d) {

      this.dragtooltip.remove()

      if (this.exclusion && event.button === 0) {
        var m = d3.pointer(event);

        let color = this.$store.getters.selectInclude ? "lightgreen" : "red"

        let rect_data = [[m, this.currentScale, m[1] - this.currentHeight, 0]]

        rect = this.svg.append("g").selectAll("rect")
            .data(rect_data)
            .enter()
            .append("rect")
            .attr("x", (d) => d[0][0])
            .attr("y", (d) => this.yScale(correctedHeight(d[0][1], this.heightFactor)))
            .attr("fill", color)
            .attr("class", "exclusions")
            .attr("stroke", "grey")
            .style("opacity", 0.2)
            .attr("height", 0)
            .attr("width", 0)
            .on("contextmenu", function (event, d) {
              event.preventDefault();
              let cur = d3.select(this).remove()

              rects = rects.filter(function (ele) {
                return ele === cur;
              })
            });
        ;

        this.isDown = true
      }
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
          .style("pointer-events", "none");
    },
    createDragTooltip() {
      return d3.select("#" + PANE_NAME)
          .append("div")
          .attr("pointer-events", "none")
          .style("opacity", 1)
          .html("<img width='70px' src=\"drag.png\" alt=\"Italian Trulli\"> <br><img style='margin: 0 auto; " +
              "display: table; padding-bottom: 10px; padding-top:20px;' width='50px' src=\"scrol.png\" alt=\"Italian Trulli\">")
          .attr("class", "tooltip")
          .style("background-color", "white")
          .style("float", "left")
          .style("position", "absolute")
          .style("border", "solid")
          .style("border-width", "1px")
          .style("border-radius", "5px")
          .style("padding-left", "15px")
          .style("padding-right", "15px")
          .style("line-height", "25px")
          .style("top", "0%")
          .style("left", "0%")
          .style("pointer-events", "none")

    },
    createZoom(store, network, edges, circles, levelLines, levelButton, levelLabels, yScale, heightFactor) {
      let context = this;
      return d3.zoom()
          .on('zoom', function (event) {
            context.currentHeight = event.transform.y
            context.currentScale = event.transform.k

            if (!this.exclusion) {
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


              d3.selectAll('.exclusions')
                  .attr("y", (d) => {
                    return new_yScale(correctedHeight(d[2], context.heightFactor))
                  })
                  .attr("height", (d) => {
                    return new_yScale(correctedHeight(d[2] + d[3], context.heightFactor))
                  })
            }
          })
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
      inspect(level, label)
    }
  }
}


</script>

<style scoped>
</style>
