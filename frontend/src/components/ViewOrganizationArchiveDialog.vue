<template>
  <v-dialog v-model="isDialogVisible" width="500px">
    <template v-slot:activator="{ props }">
      <v-btn v-bind="props" variant="tonal" color="warning">
        {{ organization.archived_at ? "Restore" : "Archive" }} Organization
      </v-btn>
    </template>

    <v-card>
      <v-card-title class="d-flex align-center" style="min-height: 52px">
        <div>
          {{ organization.archived_at ? "Restore" : "Archive" }} Organization
        </div>
      </v-card-title>
      <v-divider></v-divider>
      <v-card-text>
        <p v-if="organization.archived_at" class="mb-2">
          Are you sure you want to restore '{{ organization.name }}'? You can
          archive organizations at any time.
        </p>
        <p v-else class="mb-2">
          Are you sure you want to archive '{{ organization.name }}'? You can
          reactivate organizations at any time.
        </p>
      </v-card-text>
      <v-divider></v-divider>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn variant="text" @click="isDialogVisible = false"> Cancel </v-btn>
        <v-btn
          variant="elevated"
          color="warning"
          @click="toggleArchiveOrganization"
        >
          {{ organization.archived_at ? "Restore" : "Archive" }} Organization
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { apiClient } from "@/plugins/api";
import { OrganizationRead } from "@/services";
import { ref } from "vue";

const props = defineProps<{
  organization: OrganizationRead;
}>();

const emit = defineEmits<{
  (e: "toggledArchive", organization: OrganizationRead): void;
}>();

const isDialogVisible = ref(false);

const toggleArchiveOrganization = async () => {
  const response = await apiClient.organizations.archiveOrganization(
    props.organization.id,
  );
  emit("toggledArchive", response);
  isDialogVisible.value = false;
};
</script>
