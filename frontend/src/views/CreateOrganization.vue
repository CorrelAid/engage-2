<template>
  <v-container>
    <v-row class="justify-center">
      <v-col cols="12" md="10" lg="8">
        <v-breadcrumbs :items="breadcrumbs" class="px-0"></v-breadcrumbs>
        <h1 class="mb-5">Create Organization</h1>
        <v-form v-model="isFormValid" @submit.prevent="createOrganization">
          <v-text-field
            v-model="name"
            label="Name"
            :rules="[nameRule]"
          ></v-text-field>
          <v-select
            v-model="legalForm"
            :items="legalForms"
            label="Legal Form"
          ></v-select>
          <v-select
            v-model="sector"
            :items="sectors"
            label="Sectors"
            multiple
          ></v-select>
          <contact-list
            :contacts="contacts"
            @add-contact="contacts.push($event)"
            @delete-contact="contacts.splice(contacts.indexOf($event), 1)"
          ></contact-list>
          <v-btn
            :disabled="!isFormValid"
            :loading="isLoading"
            type="submit"
            color="secondary"
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
import { OrganizationCreate, OrganizationContact } from "@/services";
import ContactList from "@/components/ContactList.vue";

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
const legalForms = Object.values(OrganizationCreate.legal_form_name);
const legalForm = ref<OrganizationCreate.legal_form_name>();
const sectors = ["Bildung", "Gesundheit", "Kultur", "Sport", "Umwelt"];
const sector = ref<
  Array<"Bildung" | "Gesundheit" | "Kultur" | "Sport" | "Umwelt">
>([]);
const contacts = ref<OrganizationContact[]>([]);

const createOrganization = async () => {
  isLoading.value = true;
  try {
    await apiClient.organizations.createOrganization({
      name: name.value,
      legal_form_name: legalForm.value!,
      sectors: sector.value,
      contacts: contacts.value,
    });
    router.push({ name: "ListOrganizations" });
  } finally {
    isLoading.value = false;
  }
};
</script>
