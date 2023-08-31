<template>
  <v-container>
    <v-row class="justify-center">
      <v-col cols="12" md="10" lg="8">
        <v-breadcrumbs :items="breadcrumbs" class="px-0"></v-breadcrumbs>
        <div v-if="isLoading">
          <v-skeleton-loader
            v-if="isLoading"
            type="heading, list-item, list-item, list-item"
          ></v-skeleton-loader>
        </div>

        <div v-if="updatedProject && !isLoading">
          <div class="d-flex align-center justify-space-between mb-5">
            <h1
              id="projectTitle"
              ref="projectTitle"
              class="d-flex flex-grow-1"
              contenteditable="true"
              @keydown.enter="updateTitle"
              @blur="updateTitle"
            >
              {{ updatedProject.title }}
            </h1>
            <v-icon class="ml-2" @click="focusProjectTitle">
              mdi-pencil
            </v-icon>
          </div>

          <div id="details" class="mb-8">
            <h2 class="mb-1">Details</h2>

            <h3 class="mb-1">Status</h3>
            <p class="mb-2">Please select the current status of the Project.</p>
            <v-select
              v-model="updatedProject.status"
              :items="projectStatus"
              label="Project Status"
            ></v-select>

            <h2 class="mb-1">Summary</h2>
            <v-textarea
              box
              label="Summary"
              auto-grow
              v-model="updatedProject.summary"
            ></v-textarea>
          </div>

          <div id="danger-zone" class="mb-8">
            <h2 class="mb-1">Danger Zone</h2>

            <h3 class="mb-1 mt-4">Delete Project</h3>
            <p class="mb-2">
              You can delete the project. This will permanently remove the
              selected project from the workspace. Please note that this action
              cannot be undone, so make sure to back up any important data
              before proceeding.
            </p>
            <view-project-delete-dialog
              :project="project"
            ></view-project-delete-dialog>
          </div>
        </div>
      </v-col>
    </v-row>
  </v-container>
  <v-navigation-drawer :rail="isRail" location="right" permanent>
    <v-list>
      <v-list-item :title="project?.title" subtitle="Project">
        <template #prepend>
          <v-avatar
            :size="isRail ? 24 : undefined"
            :rounded="isRail || 'lg'"
            color="secondary"
          >
            <strong class="text-white">
              {{ project?.title.charAt(0).toUpperCase() }}
            </strong>
          </v-avatar>
        </template>
      </v-list-item>
    </v-list>
    <v-divider></v-divider>
    <v-list v-if="project">
      <v-list-item>
        <v-list-item-subtitle> Status </v-list-item-subtitle>
        <v-list-item-title>
          {{ project.status }}
        </v-list-item-title>
      </v-list-item>
    </v-list>
    <v-divider></v-divider>
    <v-list density="compact" nav>
      <v-list-item
        :to="{ hash: '#details' }"
        title="Details"
        prepend-icon="mdi-text-box-search-outline"
        :active="false"
      ></v-list-item>
    </v-list>
    <template #append>
      <v-divider></v-divider>
      <div class="pa-2">
        <v-btn
          :disabled="_isEqual(project, updatedProject)"
          :loading="isUpdateLoading"
          variant="tonal"
          color="secondary"
          block
          @click="updateProject"
        >
          <v-icon :class="{ 'mr-1': !isRail }">mdi-content-save</v-icon>
          <span v-if="!isRail">Save Changes</span>
        </v-btn>
      </div>
      <v-divider></v-divider>
      <v-list density="compact" nav>
        <v-list-item
          :prepend-icon="isRail ? 'mdi-chevron-left' : 'mdi-chevron-right'"
          title="Collapse Navigation"
          @click="isRail = !isRail"
        ></v-list-item>
      </v-list>
    </template>
  </v-navigation-drawer>
</template>

<script setup lang="ts">
import { VSkeletonLoader } from "vuetify/labs/VSkeletonLoader";
import { computed, onBeforeMount, ref } from "vue";
import { useRoute } from "vue-router";
import { apiClient } from "@/plugins/api";
import { ReadProject, UpdateProject } from "@/services";
import { isEqual as _isEqual } from "lodash-es";

import ViewProjectDeleteDialog from "@/components/ViewProjectDeleteDialog.vue";

const route = useRoute();

const breadcrumbs = computed(() => [
  {
    title: "Projects",
    to: { name: "ListProjects" },
    disabled: false,
  },
  {
    title: project.value?.title || route.params.projectId,
    to: {
      name: "ViewProject",
      params: { projectId: route.params.projectId },
    },
    disabled: true,
  },
]);

const isRail = ref(false);

const isLoading = ref(false);
const project = ref<ReadProject>();
const updatedProject = ref<UpdateProject>();
const projectStatus = [
  "Inception",
  "Call for Applications",
  "Running",
  "Published",
];

const fetchProject = async () => {
  isLoading.value = true;
  const startTime = new Date();
  try {
    const response = (project.value = await apiClient.projects.readProject(
      route.params.projectId.toString(),
    ));
    project.value = structuredClone(response);
    updatedProject.value = structuredClone(response);
  } catch (error) {
    console.error(error);
  } finally {
    const duration = new Date().getTime() - startTime.getTime();
    const timeout = duration >= 300 ? 0 : 300 - duration;
    setTimeout(() => {
      isLoading.value = false;
    }, timeout);
  }
};

const projectTitle = ref();
const isUpdateLoading = ref(false);

const focusProjectTitle = async () => {
  const nameElement = document.getElementById("projectTitle");
  nameElement?.focus();
};

const updateTitle = async (event: Event) => {
  (event.target as HTMLInputElement).blur();
  updatedProject.value!.title = (event.target as HTMLInputElement).innerText;
};

const updateProject = async () => {
  isUpdateLoading.value = true;
  const startTime = new Date();
  try {
    const response = await apiClient.projects.updateProject(
      route.params.projectId.toString(),
      updatedProject.value!,
    );
    project.value = structuredClone(response);
  } catch (error) {
    console.error(error);
  } finally {
    const duration = new Date().getTime() - startTime.getTime();
    const timeout = duration >= 300 ? 0 : 300 - duration;
    setTimeout(() => {
      isUpdateLoading.value = false;
    }, timeout);
  }
};

onBeforeMount(async () => {
  await fetchProject();
});
</script>
