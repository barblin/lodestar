<template>
  <sidebar-menu :menu="menu" @itemClick="onItemClick" :collapsed="collapsed"/>
</template>

<script>
import {SidebarMenu} from 'vue-sidebar-menu'
import '@fortawesome/fontawesome-free/css/all.css'
import 'vue-sidebar-menu/dist/vue-sidebar-menu.css'
import {updateResources} from "../../services/datasource";
import {modes} from "../../services/modes";

export default {
  components: {
    SidebarMenu
  },
  name: "SideNav",
  data() {
    return {
      menu: [
        {
          header: "Lodestar",
          title: 'Main Navigation',
          hiddenOnCollapse: true
        },
        {
          href: '/',
          title: 'Cluster Explorer',
          icon: 'fa fa-eye'
        },
        {
          href: '/charts',
          title: 'How to use?',
          icon: 'fa fa-chart-area'
        },
        {
          href: '/resources',
          title: 'Manage resources',
          icon: 'fa fa-database'
        }
      ],
      collapsed: true
    }
  },
  methods: {
    onItemClick(event, item) {
      if(item.href = "/resources"){
        this.$store.commit('updateCurrentMode', modes.INPUT)
        this.$router.push('/resources')
      } else {
        updateResources();
        this.$store.commit('updateCurrentMode', modes.INPUT)
        this.$router.push('/')
      }
    }
  }
}
</script>

<style scoped lang="scss">

</style>