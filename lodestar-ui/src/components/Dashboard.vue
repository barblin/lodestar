<template>
  <top-nav></top-nav>
  <side-nav></side-nav>
  <br>
  <div id="flex">
    <ModeDefault v-if="$store.getters.currentMode == modes.DEFAULT"></ModeDefault>
    <ModeCluster v-if="$store.getters.currentMode == modes.CLUSTER"></ModeCluster>
    <ModeAlpha v-if="$store.getters.currentMode == modes.ALPHA"></ModeAlpha>
  </div>
</template>

<script>
import SideNav from "./menu/SideNav.vue";
import TopNav from "./menu/TopNav.vue";
import ModeDefault from "./modes/ModeDefault.vue";
import ModeCluster from "./modes/ModeCluster.vue";
import ModeAlpha from "./modes/ModeAlpha.vue";
import {modes} from "../services/modes";

export default {
  name: "Dashboard",
  data() {
    return {
      modes: modes
    };
  },
  components: {
    TopNav,
    SideNav,
    ModeDefault,
    ModeCluster,
    ModeAlpha,
  },

}
</script>

<style lang="css">
#flex {
  display: flex;
  flex-flow: row wrap;
}

#spinner {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 50%;
}
</style>
