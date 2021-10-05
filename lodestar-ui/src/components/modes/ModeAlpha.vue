<template>
  <div :id="views.SPACE" class="space">
    <Space :key="updateKeys[views.SPACE]" :parent="views.SPACE" :drawScatter="$store.getters.drawSpaceScatter"
           :drawNet="$store.getters.drawSpaceNet"
           :spaceData="$store.getters.spaceData"/>
  </div>
  <div :id="views.VELOCITY" class="velocity">
    <Velocity :key="updateKeys[views.VELOCITY]" :parent="views.VELOCITY"
              :drawScatter="$store.getters.drawVelocityScatter"
              :drawNet="$store.getters.drawVelocityNet"
              :netData="$store.getters.velocityNetworkData"
              :scatData="$store.getters.velocityScatterData"/>
  </div>
  <div :id="views.NETWORK" class="network">
    <Network :key="updateKeys[views.NETWORK]" :network="$store.getters.network" :parent="views.NETWORK"/>
  </div>
  <div :id="views.ALPHA" class="alpha">
    <Alpha :key="updateKeys[views.ALPHA]" :parent="views.ALPHA"/>
  </div>
</template>

<script>
import {views} from "../../services/views";
import Space from "../views/Space.vue";
import Velocity from "../views/Velocity.vue";
import Network from "../views/DensityExplorer.vue";
import Alpha from "../views/alpha/Alpha.vue";
import {updateResources} from "../../services/datasource";

export default {
  name: "ModeDefault",
  data() {
    return {
      updateKeys: {},
      views: views,
    };
  },
  components: {
    Space,
    Velocity,
    Network,
    Alpha,
  },
  mounted() {
    updateResources();
    this.updateKeys[views.SCATTER] = 0;
    this.updateKeys[views.SPACE] = 0;
    this.updateKeys[views.DISTRIBUTION] = 0;
    this.updateKeys[views.NETWORK] = 0;
    this.updateKeys[views.VELOCITY] = 0;
    this.updateKeys[views.ALPHA] = 0;
  },
}
</script>


<style lang="css" scoped>
#space {
  order: 0
}

#velocity {
  order: 1;
}

#network {
  order: 2;
}

#alpha {
  order: 3;
}

.space {
  position: relative;
  float: left;
  width: 50%;
  height: 460px;
  border: 1px solid darkslategrey;
  margin-bottom: 10px;
  margin-right: 5px;
}

.velocity {
  position: relative;
  float: left;
  width: 49%;
  height: 460px;
  border: 1px solid darkslategrey;
  margin-bottom: 10px;
}

.network {
  position: relative;
  float: left;
  width: 100%;
  height: 250px;
  border: 1px solid darkslategrey;
}

.alpha {
  position: relative;
  float: left;
  width: 100%;
  height: 200px;
  border-right: 1px solid darkslategrey;
  border-bottom: 1px solid darkslategrey;
  border-left: 1px solid darkslategrey;
}

</style>