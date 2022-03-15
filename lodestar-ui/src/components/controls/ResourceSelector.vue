<template>
  <label class="feature-label">Select from available resources</label>
  <vue-select v-model="selection" placeholder="Select source file"
              :closeOnSelect="true"
              :searchable="true"
              :options="$store.getters.resources"
              class="nav-el"></vue-select>
  <br><br><br>
  <!--<input class="radial" type="checkbox" id="checkbox" v-model="plotRadial">
  <label class="radial rad-label" for="checkbox">Include radial velocity</label>-->
  <br>
  <br>
  <br>
  <span>
    <label class="feature-label">Select alpha value</label>
    <vue-select v-model="alpha"
                :closeOnSelect="true"
                :selected="$store.getters.alphas[alpha]"
                :placeholder="$store.getters.alphas[alpha]"
                :options="$store.getters.alphas" class="nav-el"></vue-select>
  </span>
  <span v-if="includeFirstSpaceDimension()">
    <label class="feature-label">First space</label>
    <vue-select v-model="s1"
                :searchable="true"
                :closeOnSelect="true"
                :selected="$store.getters.resourceHeaders[s1]"
                :placeholder="$store.getters.resourceHeaders[s1]"
                :options="$store.getters.resourceHeaders" class="nav-el"></vue-select>
  </span>
  <span v-if="includeSecondSpaceDimension()">
    <label class="feature-label">Second space</label>
    <vue-select v-model="s2"
                :closeOnSelect="true"
                :searchable="true"
                :empty-model-value="$store.getters.resourceHeaders[s2]"
                :placeholder="$store.getters.resourceHeaders[s2]"
                :options="$store.getters.resourceHeaders" class="nav-el"></vue-select>
  </span>
  <span v-if="includeThirdSpaceDimension()">
    <label class="feature-label">Third space</label>
    <vue-select v-model="s3"
                :closeOnSelect="true"
                :searchable="true"
                :empty-model-value="$store.getters.resourceHeaders[s3]"
                :placeholder="$store.getters.resourceHeaders[s3]"
                :options="$store.getters.resourceHeaders" class="nav-el"></vue-select>
  </span>
  <span v-if="includeFirstVelocityDimension()">
    <label class="feature-label">First velocity</label>
    <vue-select v-model="v1"
                :closeOnSelect="true"
                :searchable="true"
                :empty-model-value="$store.getters.resourceHeaders[v1]"
                :placeholder="$store.getters.resourceHeaders[v1]"
                :options="$store.getters.resourceHeaders" class="nav-el"></vue-select>
  </span>
  <span v-if="includeSecondVelocityDimension()">
    <label class="feature-label">Second velocity</label>
    <vue-select v-model="v2"
                :closeOnSelect="true"
                :searchable="true"
                :empty-model-value="$store.getters.resourceHeaders[v2]"
                :placeholder="$store.getters.resourceHeaders[v2]"
                :options="$store.getters.resourceHeaders" class="nav-el"></vue-select>
  </span>
  <span v-if="includeThirdVelocityDimension()">
      <label class="feature-label">Radial velocity</label>
    <vue-select v-model="v3"
                :closeOnSelect="true"
                :searchable="true"
                :empty-model-value="$store.getters.resourceHeaders[v3]"
                :placeholder="$store.getters.resourceHeaders[v3]"
                :options="$store.getters.resourceHeaders" class="nav-el"></vue-select>
  </span>
  <span v-if="includeThirdVelocityDimension()">
      <label class="feature-label">Radial velocity error</label>
    <vue-select v-model="rad_error"
                :closeOnSelect="true"
                :searchable="true"
                :empty-model-value="$store.getters.resourceHeaders[rad_error]"
                :placeholder="$store.getters.resourceHeaders[rad_error]"
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
      s1: 18,
      s2: 19,
      s3: 20,
      v1: 24,
      v2: 25,
      v3: 14,
      rad_error: 68,
      plotRadial: false,
      alpha: 0
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
    },
    rad_error: function (sel) {
      let selection = this.getSelection()
      selection.rad_error = this.getColumnIndex(sel)
      this.updateSelection(selection)
    },
    alpha: function (sel) {
      if(sel != undefined) {
        this.$store.commit('updateAlpha', sel)
      }
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
  margin-top: 30px;
  margin-right: 2px;
  float: left;
}

input {
  top: 5px;
}

.radial {
  margin-top: 30px;
  float: left;
}

.nav-el {
  float: left;
  width: 100%;
}
</style>