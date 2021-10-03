<template>
  <top-nav></top-nav>
  <side-nav></side-nav>
  <br>
  <div id="flex">
    <!--<div :id="views.SCATTER" class="simple-plot">
      <Scatter :key="updateKeys[views.SCATTER]" :plotData="$store.getters.plotData" :parent="views.SCATTER"
               @maximize="maximize(views.SCATTER)"/>
    </div>
    <div :id="views.DISTRIBUTION" class="simple-plot">
      <Distribution :key="updateKeys[views.DISTRIBUTION]" :parent="views.DISTRIBUTION"
                    @maximize="maximize(views.DISTRIBUTION)"/>
    </div>-->
    <div :id="views.NETWORK" class="density-plot">
      <Network :key="updateKeys[views.NETWORK]" :network="$store.getters.network" :parent="views.NETWORK"
               @maximize="maximize(views.NETWORK)"/>
    </div>
    <div :id="views.SPACE" class="simple-plot">
      <Space :key="updateKeys[views.SPACE]" :parent="views.SPACE" :drawScatter="$store.getters.drawSpaceScatter"
             :drawNet="$store.getters.drawSpaceNet"
             :spaceData="$store.getters.spaceData"
             @maximize="maximize(views.SPACE)"/>
    </div>
    <div :id="views.VELOCITY" class="simple-plot">
      <Velocity :key="updateKeys[views.VELOCITY]" :parent="views.VELOCITY"
                :drawScatter="$store.getters.drawVelocityScatter"
                :drawNet="$store.getters.drawVelocityNet"
                :netData="$store.getters.velocityNetworkData"
                :scatData="$store.getters.velocityScatterData"
                @maximize="maximize(views.VELOCITY)"/>
    </div>
  </div>
</template>

<script>
import {updateResources} from "../services/datasource";
import Scatter from "./views/cluster/Scatter.vue"
import Network from "./views/DensityExplorer.vue"
import SideNav from "./menu/SideNav.vue";
import TopNav from "./menu/TopNav.vue";
import Distribution from "./views/cluster/Distribution.vue";
import Space from "./views/Space.vue";
import Velocity from "./views/Velocity.vue";
import {views} from "../services/views"
import {modes} from "../services/modes"

export default {
  name: "Dashboard",
  props: ['currentMode'],
  components: {
    Distribution,
    TopNav,
    Scatter,
    Network,
    SideNav,
    Space,
    Velocity
  },
  data() {
    return {
      updateKeys: {},
      views: views
    };
  },
  mounted() {
    updateResources();
    this.updateKeys[views.SCATTER] = 0;
    this.updateKeys[views.SPACE] = 0;
    this.updateKeys[views.DISTRIBUTION] = 0;
    this.updateKeys[views.NETWORK] = 0;
    this.updateKeys[views.VELOCITY] = 0;

    this.maximize(views.SPACE)
  },
  watch: {
    currentMode: function (currentMode) {

      console.log("MODE has changed")
      if (currentMode == modes.DEFAULT) {

      } else if (currentMode == modes.ALPHA) {

      } else if (currentMode == modes.CLUSTER) {
        let densityNav = document.getElementById(views.NETWORK.toString());
        densityNav.className = "density-plot-slim"
      }
    }
  },
  methods: {
    maximize: function (selectionId) {
      let element = document.getElementById("main");
      let selection = document.getElementById(selectionId);

      if (element) {
        element.id = this.$store.getters.currentViewSelection
        this.updateKeys[this.$store.getters.currentViewSelection]++;
        element.className = "simple-plot"
      }

      if (selection) {
        selection.id = "main"
        selection.className = "selected-main"
        this.$store.commit('updateCurrentViewSelection', selectionId)
      }

      this.updateKeys[selectionId]++;
    }
  }
}
</script>

<style lang="css">
#flex {
  display: flex;
  flex-flow: row wrap;
}

#main {
  order: 0
}

#space {
  order: 1;
}

#velocity {
  order: 2;
}

#network {
  order: 3;
}

#scatter {
  order: 4;
}

#distribution {
  order: 5;
}


.simple-plot {
  position: relative;
  float: left;
  width: 600px;
  height: 460px;
  border: 1px solid darkslategrey;
  margin-bottom: 10px;
}

.density-plot {
  position: relative;
  float: left;
  width: 100%;
  height: 300px;
  border: 1px solid darkslategrey;
  margin-bottom: 10px;
}

.density-plot-slim {
  position: relative;
  float: left;
  width: 10%;
  height: 300px;
  border: 1px solid darkslategrey;
  margin-bottom: 10px;
}

.selected-main {
  position: relative;
  float: left;
  width: 50%;
  height: 600px;
  border: 1px solid darkslategrey;
  margin-bottom: 10px;
  margin-right: 5px;
}

#spinner {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 50%;
}

</style>
