<template>
  <v-list>
    <v-list-item
      v-for="contact in contacts"
      :key="contact.name"
      :title="contact.name"
      lines="three"
      class="px-0"
    >
      <template v-slot:prepend>
        <v-avatar rounded="lg" color="secondary">
          <strong>
            {{ contact.name.charAt(0).toUpperCase() }}
          </strong>
        </v-avatar>
      </template>
      <template v-slot:subtitle>
        {{ contact.email }}
        <br />
        {{ contact.phone }}
      </template>
      <template v-slot:append>
        <v-btn
          variant="text"
          color="error"
          size="small"
          @click="emit('deleteContact', contact)"
          >Delete</v-btn
        >
      </template>
    </v-list-item>
    <contact-list-create-dialog
      @add-contact="emit('addContact', $event)"
    ></contact-list-create-dialog>
  </v-list>
</template>

<script setup lang="ts">
import { OrganizationContact } from "@/services";
import ContactListCreateDialog from "./ContactListCreateDialog.vue";

const props = defineProps<{
  contacts: OrganizationContact[];
}>();

const emit = defineEmits<{
  (e: "addContact", contact: OrganizationContact): void;
  (e: "deleteContact", contact: OrganizationContact): void;
}>();
</script>
