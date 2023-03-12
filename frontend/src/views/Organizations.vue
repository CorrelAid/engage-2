<template>
  <v-container>
    <v-row class="justify-center">
      <v-col cols="12" md="10" lg="8">
        <v-breadcrumbs :items="breadcrumbs" class="px-0"></v-breadcrumbs>
        <h1 class="mb-5">Organizations</h1>
        <v-btn color="secondary">Add Organization</v-btn>
        <v-text-field
          v-model="search"
          prepend-inner-icon="mdi-magnify"
          density="compact"
          variant="outlined"
          class="my-2"
          clearable
          hide-details
        ></v-text-field>
        <v-list density="comfortable">
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
import { computed, ref } from "vue";

interface Organization {
  id: string;
  name: string;
}

const breadcrumbs = [
  { title: "Organizations", to: { name: "Organizations" }, disabled: true },
];

const organizations = ref<Organization[]>([
  {
    id: "2345a5a1-5e4a-445e-b3e8-9179c978476a",
    name: "Deutscher Caritasverband e.V.",
  },
  {
    id: "a9e1db78-5958-41c3-b323-2870f2b75db1",
    name: "Social Entrepreneurship Netzwerk Deutschland e.V.",
  },
  {
    id: "3f6a4c64-a63b-46ac-86c8-f11ce3e9c2eb",
    name: "Deutscher Pfadfinderbund e.V.",
  },
]);

const search = ref<string>();

const filteredOrganizations = computed<Organization[]>(() =>
  organizations.value.filter(
    (organization) =>
      !search.value ||
      organization.name.toLowerCase().includes(search.value?.toLowerCase())
  )
);
</script>
