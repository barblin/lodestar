<template>
  <div class="hello">
    <side-nav></side-nav>
    <span v-if="$store.getters.loadingMain" class="center">
      <RingLoader :size="'200px'" v-if="$store.getters.loadingMain"></RingLoader>
    </span>
    <h3>Include online resource</h3>
    <br/>
    <input style="width: 400px" type="url" placeholder="https://www.example.com/indigo.csv" v-model="url" @input="change($event)"
           @change="change($event)"/>
    <div class="error" v-if="!isValid">You must copy and paste a valid URL (link address)</div>
    <div class="error" v-if="$store.getters.uploadFinished">Resource successfully added</div>
    <div class="calculate">
      <br><br>
      <button type="button" :disabled="$store.getters.loadingAny && !isValid" @click="click()">
        Add resource
      </button>
    </div>
    <br><br>
    <a href="https://people.sc.fsu.edu/~jburkardt/data/csv/csv.html" target="_blank">Visit this page to copy valid test URLs</a>
  </div>
</template>

<script>
import {downloadResource} from "../services/datasource";
import SideNav from "./menu/SideNav.vue";
import {store} from "../store/cluster-state-store";

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
  unmounted() {
    this.$store.commit('updateUploadFinished', false)
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