<template>
  <v-navigation-drawer
    v-if="authStore.isAuthenticated"
    :rail="isRail"
    permanent
  >
    <v-list v-if="authStore.user">
      <v-list-item :title="authStore.user.name" subtitle="Administrator">
        <template #prepend>
          <v-avatar
            :size="isRail ? 24 : undefined"
            :rounded="isRail || 'lg'"
            color="primary"
          >
            <strong class="text-white">{{ authStore.user.name.at(0) }}</strong>
          </v-avatar>
        </template>
      </v-list-item>
    </v-list>
    <v-divider></v-divider>
    <v-list density="compact" nav>
      <v-list-item
        :to="{ name: 'Dashboard' }"
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
        :to="{ name: 'ListOrganizations' }"
        prepend-icon="mdi-domain"
        title="Organizations"
      ></v-list-item>
    </v-list>
    <v-divider></v-divider>

    <template #append>
      <v-divider></v-divider>
      <v-list density="compact" nav>
        <v-list-item
          prepend-icon="mdi-logout"
          title="Logout"
          @click="logout"
        ></v-list-item>
      </v-list>
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
import { useAuthStore } from "@/store/auth";
import { useRouter } from "vue-router";

const authStore = useAuthStore();
const router = useRouter();

const isRail = ref(true);

const logout = async () => {
  await authStore.logout();
  router.push({ name: "Login" });
};
</script>
