<template>
  <v-app>
    <v-main>
      <the-navigation-drawer></the-navigation-drawer>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { onBeforeMount } from "vue";
import TheNavigationDrawer from "./components/TheNavigationDrawer.vue";
import { apiClient } from "./plugins/api";

// be sure to get the csrf token before the app is mounted
// do not delete
onBeforeMount(async () => {
  await apiClient.csrf.getCsrfCsrfGet();
});
</script>
