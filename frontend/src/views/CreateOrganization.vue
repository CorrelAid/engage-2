<template>
  <v-container>
    <v-row class="justify-center">
      <v-col cols="12" md="10" lg="8">
        <v-breadcrumbs :items="breadcrumbs" class="px-0"></v-breadcrumbs>
        <h1 class="mb-5">Create Organization</h1>
        <v-form v-model="isFormValid">
          <v-text-field
            v-model="name"
            label="Name"
            :rules="[nameRule]"
          ></v-text-field>
          <v-btn
            :disabled="!isFormValid"
            :loading="isLoading"
            type="submit"
            color="secondary"
            @click.prevent="createOrganization"
          >
            Create Organization
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

const router = useRouter();

const breadcrumbs = [
  { title: "Organizations", to: { name: "ListOrganizations" } },
  {
    title: "Create Organization",
    to: { name: "CreateOrganization" },
    disabled: true,
  },
];

const isLoading = ref(false);
const isFormValid = ref(false);

const name = ref("");
const nameRule = (v: string) => !!v || "Name is required";

const createOrganization = async () => {
  isLoading.value = true;
  try {
    await apiClient.organizations.createOrganization({
      name: name.value,
    });
    router.push({ name: "ListOrganizations" });
  } finally {
    isLoading.value = false;
  }
};
</script>
