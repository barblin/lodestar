<template>
  <vue-select v-model="selection" placeholder="Select source file" :options="$store.getters.resources"
              class="nav-el"></vue-select>
  <input class="radial" type="checkbox" id="checkbox" v-model="plotRadial">
  <label class="radial rad-label" for="checkbox">With Radial </label>
  <span v-if="includeFirstSpaceDimension()">
    <label class="feature-label">S1</label>
    <vue-select v-model="s1"
                :placeholder="$store.getters.resourceHeaders[s1]"
                :options="$store.getters.resourceHeaders" class="nav-el"></vue-select>
  </span>
  <span v-if="includeSecondSpaceDimension()">
    <label class="feature-label">S2</label>
    <vue-select v-model="s2"
                :placeholder="$store.getters.resourceHeaders[s2]"
                :options="$store.getters.resourceHeaders" class="nav-el"></vue-select>
  </span>
  <span v-if="includeThirdSpaceDimension()">
    <label class="feature-label">S3</label>
    <vue-select v-model="s3"
                :placeholder="$store.getters.resourceHeaders[s3]"
                :options="$store.getters.resourceHeaders" class="nav-el"></vue-select>
  </span>
  <span v-if="includeFirstVelocityDimension()">
    <label class="feature-label">V1</label>
    <vue-select v-model="v1"
                :placeholder="$store.getters.resourceHeaders[v1]"
                :options="$store.getters.resourceHeaders" class="nav-el"></vue-select>
  </span>
  <span v-if="includeSecondVelocityDimension()">
    <label class="feature-label">V2</label>
    <vue-select v-model="v2"
                :placeholder="$store.getters.resourceHeaders[v2]"
                :options="$store.getters.resourceHeaders" class="nav-el"></vue-select>
  </span>
  <span v-if="includeThirdVelocityDimension()">
      <label class="feature-label">V3</label>
    <vue-select v-model="v3"
                :placeholder="$store.getters.resourceHeaders[v3]"
                :options="$store.getters.resourceHeaders" class="nav-el"></vue-select>
  </span>
</template>

<script>
import {updateResourceHeaders} from "../../services/datasource";
import {
  includeFirstSpaceDimension,
  includeFirstVelocityDimension,
  includeSecondSpaceDimension,
  includeSecondVelocityDimension,
  includeThirdSpaceDimension,
  includeThirdVelocityDimension
} from "../../services/dimension-util";

export default {
  name: "ResourceSelector",
  props: ['selection'],
  data: function () {
    return {
      s1: 0,
      s2: 1,
      s3: 2,
      v1: 3,
      v2: 4,
      v3: 5,
      plotRadial: false,
    }
  },
  watch: {
    plotRadial: function (plotRadial) {
      this.$store.commit('updatePlotRadial', plotRadial)
    },
    selection: function (selection) {
      this.$store.commit('updateCurrentResource', selection)
      updateResourceHeaders(this.$store.getters.currentResource);

      if (includeFirstSpaceDimension()) {
        this.s1 = this.$store.getters.currentColumnSelection.s1;
      }

      if (includeSecondSpaceDimension()) {
        this.s2 = this.$store.getters.currentColumnSelection.s2;
      }

      if (includeThirdSpaceDimension()) {
        this.s3 = this.$store.getters.currentColumnSelection.s3;
      }

      if (includeFirstVelocityDimension()) {
        this.v1 = this.$store.getters.currentColumnSelection.v1;
      }

      if (includeSecondVelocityDimension()) {
        this.v2 = this.$store.getters.currentColumnSelection.v2;
      }

      if (includeThirdVelocityDimension()) {
        this.v3 = this.$store.getters.currentColumnSelection.v3;
      }
    },
    s1: function (sel) {
      let selection = this.getSelection()
      selection.s1 = this.getColumnIndex(sel)
      this.updateSelection(selection)
    },
    s2: function (sel) {
      let selection = this.getSelection()
      selection.s2 = this.getColumnIndex(sel)
      this.updateSelection(selection)
    },
    s3: function (sel) {
      let selection = this.getSelection()
      selection.s3 = this.getColumnIndex(sel)
      this.updateSelection(selection)
    },
    v1: function (sel) {
      let selection = this.getSelection()
      selection.v1 = this.getColumnIndex(sel)
      this.updateSelection(selection)
    },
    v2: function (sel) {
      let selection = this.getSelection()
      selection.v2 = this.getColumnIndex(sel)
      this.updateSelection(selection)
    },
    v3: function (sel) {
      let selection = this.getSelection()
      selection.v3 = this.getColumnIndex(sel)
      this.updateSelection(selection)
    }
  },
  methods: {
    getColumnIndex(sel) {
      return this.$store.getters.resourceHeaders.indexOf(sel)
    },
    getSelection() {
      return this.$store.getters.currentColumnSelection
    },
    updateSelection(selection) {
      this.$store.commit('updateCurrentColumnSelection', selection)
    },
    includeFirstSpaceDimension() {
      return includeFirstSpaceDimension();
    },
    includeSecondSpaceDimension() {
      return includeSecondSpaceDimension();
    },
    includeThirdSpaceDimension() {
      return includeThirdSpaceDimension();
    },
    includeFirstVelocityDimension() {
      return includeFirstVelocityDimension();
    },
    includeSecondVelocityDimension() {
      return includeSecondVelocityDimension();
    },
    includeThirdVelocityDimension() {
      return includeThirdVelocityDimension();
    },
  }
}
</script>

<style scoped>
.rad-label {
  font-size: 0.9rem;
  margin-right: 30px;
}

.feature-label {
  font-size: 0.9rem;
  margin-top: 3px;
  margin-right: 2px;
  float: left;
}

input {
  top: 5px;
}

.radial {
  margin-top: 3px;
  float: left;
}
</style>