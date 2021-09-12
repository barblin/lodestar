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
          title: 'Cluster Explorer',
          icon: 'fa fa-user'
        },
        {
          href: '/charts',
          title: 'How to use?',
          icon: 'fa fa-chart-area',
          child: [
            {
              href: '/charts/sublink',
              title: 'User Guide'
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