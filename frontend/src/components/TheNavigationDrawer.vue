<template>
  <v-navigation-drawer :rail="isRail" permanent>
    <v-list>
      <v-list-item title="Frie Preu" subtitle="Administrator">
        <template v-slot:prepend>
          <v-avatar
            :size="isRail ? 24 : undefined"
            :rounded="isRail || 'lg'"
            color="primary"
          >
            <strong class="text-white">FP</strong>
          </v-avatar>
        </template>
      </v-list-item>
    </v-list>
    <v-divider></v-divider>
    <v-list density="compact" nav>
      <v-list-item
        :to="{ name: 'LandingPage' }"
        prepend-icon="mdi-home"
        title="Dashboard"
      ></v-list-item>
    </v-list>
    <v-divider></v-divider>
    <v-list density="compact" nav>
      <v-list-item prepend-icon="mdi-account" title="Users"></v-list-item>
      <v-list-item prepend-icon="mdi-account-group" title="Teams"></v-list-item>
    </v-list>
    <v-divider></v-divider>
    <v-list density="compact" nav>
      <v-list-item
        prepend-icon="mdi-view-dashboard-variant"
        title="Projects"
      ></v-list-item>
      <v-list-item
        :to="{ name: 'Organizations' }"
        prepend-icon="mdi-domain"
        title="Organizations"
      ></v-list-item>
    </v-list>
    <v-divider></v-divider>

    <template v-slot:append>
      <v-divider></v-divider>
      <v-list density="compact" nav>
        <v-list-item
          :prepend-icon="isRail ? 'mdi-chevron-right' : 'mdi-chevron-left'"
          title="Collapse Navigation"
          @click="isRail = !isRail"
        ></v-list-item>
      </v-list>
    </template>
  </v-navigation-drawer>
</template>

<script setup lang="ts">
import { ref } from "vue";

const isRail = ref(true);
</script>
