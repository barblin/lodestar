<template>
  <div class="hello">
    <side-nav></side-nav>
    <h1>Tutorial</h1>
    <h3>Summary / short Description</h3>
    <p>This tool is designed to explore the results of the ScoCen-X algorithm and is directed towards users with an
      astronomy background.</p><br>
    <h3>Results</h3>
    <p>By using this tool an expert user should be able to traverse the solution space of the algorithm. The solution
      space
      is created by using different combinations of alpha and density values. An expert user is able to change either
      alpha,
      density or both and explore a unique result for a specific combination of those parameters and inspect
      characteristics of a full clustering or a specific cluster. </p>
    <p>After reading this tutorial you should have an understanding of how the color coding works, what alpha and
      density is and how the stability view works. This tutorial is work in progress.</p>

    <br>
    <h2>Parameters</h2>
    <h3>Alpha</h3>
    <p>Describes an area of significance, a threshold, that serves to decide if a density path between two clusters
    is significant enough to merge them together or not. Choosing a smaller alpha will lead to higher likelihood
    that clusters will merge.</p>

    <h3>Density</h3>
    <p>Describes the amount of neighbours that will be considered for the underlying density skeleton. A higher level
    in density means more neighbours -> higher density.</p>
    <br>
    <h2>Color encoding</h2>
    <p>The color for a specific cluster is consistent over all views. The color is assigned according to a clusters
      stability within the density level set tree. This means, that the clusters are sorted by their amount of
      occurrences within a level set tree - the amount of levels the cluster occurs in.</p>

    <img width='500px' src="DensityTree.png" alt="Density Tree Colors">
    <p>The color palette only supports 11 distinct colors, as soon as no color is available for assignment the tool
      will color the remaining clusters as black. If noise is enabled, it will be labeled as grey.</p>
    <br>
    <h2>Views</h2>
    <h3>Stability view</h3>
    <img width='500px' src="Stability.png" alt="Stability">
    <p>The stability view encodes the number of clusters a certain combination of alpha and density produces.
    Meaning, on the y-Axis we have the number of clusters, on the x-Axis the index of a specific combination of
    alpha and density. The current selection of alpha and density is marked as bright green and enlarged.
    We always iterate over density first and then change the alpha value and restart.</p>
    <br>
    <h3>Alpha view</h3>
    <img width='500px' src="Alpha.png" alt="Stability">
    <p>The alpha view encodes the changes of the clusters for the currently selected density level if you change alpha.
    This will show you the development of the clusters if alpha is changed but only for the currently selected density level.
    It also encodes if clusters will merge into one if a change to alpha is applied.</p>
    <br>
  </div>
</template>

<script>
import {downloadResource} from "../services/data/datasource";
import SideNav from "./menu/SideNav.vue";

export default {
  name: "ResourceManager",
  data() {
    return {
      url: "",
      isValid: false,
      regex: new RegExp(/[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)?/gi)
    };
  },
  mounted() {
  },
  components: {
    SideNav
  },
  methods: {
    change: function (e) {
      const url = e.target.value
      this.isURLValid(url);
    },
    isURLValid: function (inputUrl) {
      this.isValid = inputUrl.match(this.regex)
    },
    click() {
      downloadResource(this.url);
    },
  }
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