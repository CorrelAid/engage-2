<template>
  <v-container>
    <v-row class="justify-center">
      <v-col cols="12" md="10" lg="8">
        <v-breadcrumbs :items="breadcrumbs" class="px-0"></v-breadcrumbs>
        <h1 class="mb-5">Create Project</h1>
        <v-form v-model="isFormValid" @submit.prevent="createProject">
          <h2>General Information</h2>
          <v-text-field
            v-model="title"
            label="Title"
            :rules="[required]"
          ></v-text-field>

          <div id="details" class="mb-8">
            <h2 class="mb-1">Details</h2>

            <h3 class="mb-1">Status</h3>
            <p class="mb-2">Please select the current status of the Project.</p>
            <v-select
              v-model="status"
              :items="projectStatus"
              label="Project Status"
              :rules="[required]"
            ></v-select>

            <h2 class="mb-1">Summary</h2>
            <v-textarea
              box
              label="Summary"
              auto-grow
              v-model="summary"
            ></v-textarea>
          </div>
          <v-btn
            :disabled="!isFormValid"
            :loading="isLoading"
            type="submit"
            color="secondary"
          >
            Create Project
          </v-btn>
        </v-form>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { apiClient } from "@/plugins/api";
import { ref } from "vue";
import { useRouter } from "vue-router";
import { ApiError } from "@/services";

const router = useRouter();

const breadcrumbs = [
  { title: "Projects", to: { name: "ListProjects" } },
  {
    title: "Create Project",
    to: { name: "CreateProject" },
    disabled: true,
  },
];

const isLoading = ref(false);
const isFormValid = ref(false);
const error = ref<string | boolean>(false);

const required = (v: string) => !!v || "Field is required";
const title = ref("");
const projectStatus = ["published"] as const;

type pStatus = (typeof projectStatus)[number];

const status = ref<pStatus>();
const summary = ref();

const createProject = async () => {
  isLoading.value = true;
  try {
    await apiClient.projects.createProject({
      title: title.value,
      status: status.value!,
      summary: summary.value,
    });
    router.push({ name: "ListProjects" });
  } catch (e: unknown) {
    if (e instanceof ApiError) {
      error.value = e.message;
    } else {
      error.value = "An unknown error occurred.";
    }
  } finally {
    isLoading.value = false;
  }
};
</script>
