<template>
  <sidebar-menu :menu="menu" :collapsed="collapsed" />
</template>

<script>
import { SidebarMenu } from 'vue-sidebar-menu'

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
          title: 'Explorer',
          icon: 'fa fa-user'
        },
        {
          href: '/charts',
          title: 'Tutorial',
          icon: 'fa fa-chart-area',
          child: [
            {
              href: '/charts/sublink',
              title: 'Sub Link'
            }
          ]
        }
      ],
      collapsed: {
        type: Boolean,
        default: true
      }
    }
  }
}
</script>

<style scoped lang="scss">

</style>