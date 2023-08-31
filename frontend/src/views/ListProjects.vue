<template>
  <v-container>
    <v-row class="justify-center">
      <v-col cols="12" md="10" lg="8">
        <v-breadcrumbs :items="breadcrumbs" class="px-0"></v-breadcrumbs>
        <div class="d-flex align-center justify-space-between mb-5">
          <h1>Projects</h1>
          <v-btn :to="{ name: 'CreateProject' }" color="secondary"
            >Add Project</v-btn
          >
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
            v-for="project in filteredProjects"
            :key="project.id"
            :title="project.title"
          >
            <template #prepend>
              <v-avatar rounded="lg" color="secondary">
                <strong>{{ project.title.charAt(0).toUpperCase() }}</strong>
              </v-avatar>
            </template>
            <template #append>
              <v-btn
                variant="tonal"
                color="secondary"
                rounded="lg"
                size="small"
                icon="mdi-arrow-right"
                :to="{
                  name: 'ViewProject',
                  params: { projectId: project.id },
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
import { ReadProject } from "@/services";
import { apiClient } from "@/plugins/api";
import { onBeforeMount } from "vue";

interface Project {
  id: string;
  title: string;
}

const breadcrumbs = [
  { title: "Projects", to: { name: "ListProjects" }, disabled: true },
];

const isLoading = ref(false);

const projects = ref<ReadProject[]>([]);

const fetchProjects = async () => {
  isLoading.value = true;
  const startTime = new Date();
  try {
    projects.value = await apiClient.projects.listProjects();
  } finally {
    const duration = new Date().getTime() - startTime.getTime();
    const timeout = duration >= 300 ? 0 : 300 - duration;
    setTimeout(() => {
      isLoading.value = false;
    }, timeout);
  }
};

const search = ref<string>();

const filteredProjects = computed<Project[]>(() =>
  projects.value.filter(
    (project) =>
      !search.value ||
      project.title.toLowerCase().includes(search.value?.toLowerCase()),
  ),
);

onBeforeMount(async () => {
  await fetchProjects();
  console.log(filteredProjects);
});
</script>
