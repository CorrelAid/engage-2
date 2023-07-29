<template>
  <v-dialog v-model="isDialogVisible" width="500px">
    <template v-slot:activator="{ props }">
      <v-btn v-bind="props" variant="tonal" color="error">
        Delete Organization
      </v-btn>
    </template>

    <v-card>
      <v-card-title class="d-flex align-center" style="min-height: 52px">
        <div>Delete Organization</div>
      </v-card-title>
      <v-divider></v-divider>
      <v-card-text>
        <p class="mb-2">
          Please type out
          <code class="text-error font-weight-bold">DELETE</code> in the textbox
          below to confirm that you want to delete the organization '{{
            organization.name
          }}'. Please note that this action cannot be undone.
        </p>
        <v-form
          v-model="isFormValid"
          ref="form"
          id="delete-organization-form"
          @submit.prevent="deleteOrganization"
        >
          <v-text-field
            v-model="confirmation"
            :rules="[
              (v) =>
                (!!v && v.toUpperCase() === 'DELETE') ||
                'Type DELETE to confirm.',
            ]"
          ></v-text-field>
        </v-form>
      </v-card-text>
      <v-divider></v-divider>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn variant="text" @click="cancel"> Cancel </v-btn>
        <v-btn
          :disabled="!isFormValid"
          type="submit"
          form="delete-organization-form"
          variant="elevated"
          color="error"
        >
          Delete Organization
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { apiClient } from "@/plugins/api";
import router from "@/router";
import { OrganizationRead } from "@/services";
import { ref } from "vue";

const props = defineProps<{
  organization: OrganizationRead;
}>();

const isDialogVisible = ref(false);
const isFormValid = ref(false);

const form = ref();
const confirmation = ref("");

const cancel = () => {
  form.value.reset();
  isDialogVisible.value = false;
};

const deleteOrganization = async () => {
  await apiClient.organizations.deleteOrganization(props.organization.id);
  router.push({ name: "ListOrganizations" });
};
</script>
