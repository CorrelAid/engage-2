<template>
  <v-app>
    <v-main>
      <the-navigation-drawer></the-navigation-drawer>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import TheNavigationDrawer from "./components/TheNavigationDrawer.vue";
</script>
