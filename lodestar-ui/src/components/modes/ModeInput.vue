<template>
  <top-nav></top-nav>
</template>

<script>
import {modes} from "../../services/modes";
import TopNav from "../menu/TopNav.vue";
import {updateResources} from "../../services/datasource";

export default {
  name: "ModeInput",
  data() {
    return {
      modes: modes
    };
  },
  components: {
    TopNav,
  },
  mounted() {
    updateResources();
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

#hrd {
  order: 2;
}

#network {
  order: 3;
}

.space {
  position: relative;
  float: left;
  width: 50%;
  height: 600px;
  border: 1px solid darkslategrey;
  margin-bottom: 10px;
  margin-right: 5px;
}

.velocity {
  position: relative;
  margin-right: 5px;
  float: left;
  width: 30%;
  height: 500px;
  border: 1px solid darkslategrey;
  margin-bottom: 10px;
}


.hrd {
  position: relative;
  float: left;
  width: 18%;
  height: 500px;
  border: 1px solid darkslategrey;
  margin-bottom: 10px;
}

.network {
  position: relative;
  float: left;
  width: 98%;
  height: 300px;
  border: 1px solid darkslategrey;
  margin-bottom: 10px;
}

</style>