<template>
  <ControlPanel></ControlPanel>
</template>

<script>
import ControlPanel from "../controls/ControlPanel.vue";

export default {
  name: "TopNav",
  components: {
    ControlPanel
  }
}
</script>

<style>
.nav-el {
  float: left;
  margin-right: 5px;
}
</style>