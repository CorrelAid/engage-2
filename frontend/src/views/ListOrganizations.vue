<template>
  <v-container>
    <v-row class="justify-center">
      <v-col cols="12" md="10" lg="8">
        <v-breadcrumbs :items="breadcrumbs" class="px-0"></v-breadcrumbs>
        <div class="d-flex align-center justify-space-between mb-5">
          <h1>Organizations</h1>
          <v-btn :to="{ name: 'CreateOrganization' }" color="secondary">
            Add Organization
          </v-btn>
        </div>
        <v-text-field
          v-model="search"
          prepend-inner-icon="mdi-magnify"
          density="compact"
          variant="outlined"
          class="my-2"
          clearable
          hide-details
        ></v-text-field>
        <v-skeleton-loader
          v-if="isLoading"
          type="list-item, list-item, list-item"
        ></v-skeleton-loader>
        <v-list v-else density="comfortable">
          <v-list-item
            v-for="organization in filteredOrganizations"
            :key="organization.id"
            :title="organization.name"
          >
            <template v-slot:prepend>
              <v-avatar rounded="lg" color="secondary">
                <strong>{{ organization.name.charAt(0).toUpperCase() }}</strong>
              </v-avatar>
            </template>
            <template v-slot:append>
              <v-btn
                variant="tonal"
                color="secondary"
                rounded="lg"
                size="small"
                icon="mdi-arrow-right"
                :to="{
                  name: 'Organization',
                  params: { organizationId: organization.id },
                }"
              >
              </v-btn>
            </template>
          </v-list-item>
        </v-list>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { VSkeletonLoader } from "vuetify/labs/VSkeletonLoader";
import { computed, ref } from "vue";
import { OrganizationRead } from "@/services";
import { apiClient } from "@/plugins/api";
import { onBeforeMount } from "vue";

interface Organization {
  id: string;
  name: string;
}

const breadcrumbs = [
  { title: "Organizations", to: { name: "ListOrganizations" }, disabled: true },
];

const isLoading = ref(false);

const organizations = ref<OrganizationRead[]>([]);

const fetchOrganizations = async () => {
  isLoading.value = true;
  const startTime = new Date();
  try {
    organizations.value = await apiClient.organizations.listOrganizations();
  } finally {
    const duration = new Date().getTime() - startTime.getTime();
    if (duration < 400) {
      setTimeout(() => {
        isLoading.value = false;
      }, 400 - duration);
    }
  }
};

const search = ref<string>();

const filteredOrganizations = computed<Organization[]>(() =>
  organizations.value.filter(
    (organization) =>
      !search.value ||
      organization.name.toLowerCase().includes(search.value?.toLowerCase()),
  ),
);

onBeforeMount(async () => {
  await fetchOrganizations();
});
</script>
