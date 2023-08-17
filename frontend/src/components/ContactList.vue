<template>
  <contact-list-create-dialog
    @add-contact="emit('addContact', $event)"
  ></contact-list-create-dialog>
  <v-list>
    <v-list-item
      v-for="contact in contacts"
      :key="contact.name"
      :title="contact.name"
      lines="three"
      class="px-0"
    >
      <template #prepend>
        <v-avatar rounded="lg" color="secondary">
          <strong>
            {{ contact.name.charAt(0).toUpperCase() }}
          </strong>
        </v-avatar>
      </template>
      <template #subtitle>
        {{ contact.email }}
        <br />
        {{ contact.phone }}
      </template>
      <template #append>
        <v-btn
          variant="text"
          color="error"
          size="small"
          @click="emit('deleteContact', contact)"
          >Delete</v-btn
        >
      </template>
    </v-list-item>
  </v-list>
</template>

<script setup lang="ts">
import { OrganizationContactRead } from "@/services";
import ContactListCreateDialog from "./ContactListCreateDialog.vue";

defineProps<{
  // eslint-disable-next-line no-unused-vars
  contacts: OrganizationContactRead[];
}>();

const emit = defineEmits<{
  // eslint-disable-next-line no-unused-vars
  (e: "addContact", contact: OrganizationContactRead): void;
  // eslint-disable-next-line no-unused-vars
  (e: "deleteContact", contact: OrganizationContactRead): void;
}>();
</script>
