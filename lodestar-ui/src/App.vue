<template>
  <div class="dashboard">
    <router-view></router-view>
  </div>
</template>

<script setup>
import Dashboard from './components/Dashboard.vue'
// This starter template is using Vue 3 experimental <script setup> SFCs
// Check out https://github.com/vuejs/rfcs/blob/master/active-rfcs/0040-script-setup.md

</script>

<style>
@import url(http://fonts.googleapis.com/css?family=Source+Code+Pro:400,600);
body {
  font-family: "Source Code Pro", Consolas, monaco, monospace;
  font-size: 18px;
  line-height: 1.5;
  font-weight: 400;
}

.dashboard {
  margin-left: 70px;
}

</style>
