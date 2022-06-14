<template>
  <sidebar-menu :menu="menu" @itemClick="onItemClick" :collapsed="collapsed" :width="'210px'" :hide-toggle="hideToggle"/>
</template>

<script>
import {SidebarMenu} from 'vue-sidebar-menu'
import '@fortawesome/fontawesome-free/css/all.css'
import 'vue-sidebar-menu/dist/vue-sidebar-menu.css'
import {updateResources} from "../../services/data/datasource";
import {modes} from "../../config/modes";

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
          title: 'Run Algorithm',
          icon: 'fa fa-eye'
        },
        {
          href: '/tutorial',
          title: 'Tutorial',
          icon: 'fa fa-chart-area'
        },
        {
          href: '/resources',
          title: 'Resources',
          icon: 'fa fa-database'
        }
      ],
      collapsed: false,
      hideToggle: true
    }
  },
  methods: {
    onItemClick(event, item) {
      if(item.href = "/resources"){
        this.$router.push('/resources')
      } else if(item.href = "/tutorial"){
        this.$router.push('/tutorial')
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