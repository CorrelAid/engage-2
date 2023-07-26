<template>
  <v-container>
    <v-row class="justify-center">
      <v-col cols="12" md="10" lg="8">
        <v-breadcrumbs :items="breadcrumbs" class="px-0"></v-breadcrumbs>
        <h1 class="mb-5">Create Organization</h1>
        <v-form v-model="isFormValid" @submit.prevent="createOrganization">
          <h2>General Information</h2>
          <v-text-field
            v-model="name"
            label="Name"
            :rules="[required]"
          ></v-text-field>

          <h2>Details</h2>
          <h3>Legal Form</h3>
          <p>
            Please provide the legal form as it appears on your
            government-issued identification.
          </p>
          <v-select
            v-model="legalForm"
            :items="legalForms"
            label="Legal Form"
            :rules="[required]"
          ></v-select>
          <h3>Sector</h3>
          <p>
            Please select the sector that best describes the industry or field
            of work.
          </p>
          <v-select
            v-model="sector"
            :items="sectors"
            label="Sectors"
            multiple
          ></v-select>

          <h3>Contacts</h3>
          <p>
            An organization contact and a project contact both refer to
            individuals who can be contacted regarding a particular entity, but
            they differ in scope and responsibility.
          </p>
          <p>
            An organization contact represents the organization as a whole and
            is responsible for overall communication and management, while a
            project contact is associated with a specific project or initiative
            within the organization and is responsible for managing the details
            of the project and serving as the point of contact for stakeholders.
          </p>
          <div class="mt-4 mb-4">
            <contact-list
              :contacts="contacts"
              @add-contact="contacts.push($event)"
              @delete-contact="contacts.splice(contacts.indexOf($event), 1)"
            ></contact-list>
          </div>

          <v-expand-transition>
            <v-alert v-if="error" type="error" icon="$warning" class="mb-4">
              <b>
                {{ error }}
              </b>
            </v-alert>
          </v-expand-transition>
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
import { OrganizationCreate, OrganizationContact, ApiError } from "@/services";
import ContactList from "@/components/ContactList.vue";
import { AxiosError } from "axios";

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
const error = ref<string | boolean>(false);

const required = (v: string) => !!v || "Field is required";
const name = ref("");
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
