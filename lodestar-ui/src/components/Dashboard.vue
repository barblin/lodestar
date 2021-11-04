<template>
  <side-nav></side-nav>
  <div id="flex">
    <ModeInput v-if="$store.getters.currentMode == modes.INPUT"></ModeInput>
    <ModeDefault v-if="$store.getters.currentMode == modes.DEFAULT"></ModeDefault>
    <ModeCluster v-if="$store.getters.currentMode == modes.CLUSTER"></ModeCluster>
    <ModeAlpha v-if="$store.getters.currentMode == modes.ALPHA"></ModeAlpha>
  </div>
</template>

<script>
import SideNav from "./menu/SideNav.vue";
import ModeDefault from "./modes/ModeDefault.vue";
import ModeCluster from "./modes/ModeCluster.vue";
import ModeAlpha from "./modes/ModeAlpha.vue";
import ModeInput from "./modes/ModeInput.vue";
import {modes} from "../services/modes";

export default {
  name: "Dashboard",
  data() {
    return {
      modes: modes
    };
  },
  components: {
    SideNav,
    ModeDefault,
    ModeCluster,
    ModeAlpha,
    ModeInput
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
