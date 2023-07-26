<template>
  <v-container>
    <v-row class="justify-center">
      <v-col cols="12" md="10" lg="8">
        <v-breadcrumbs :items="breadcrumbs" class="px-0"></v-breadcrumbs>
        <div v-if="organization">
          <h1 class="mb-5">{{ organization?.name }}</h1>

          <div class="mb-8" id="details">
            <h2 class="mb-1">Details</h2>

            <h3 class="mb-1">Legal Form</h3>
            <p class="mb-2">
              Please provide the legal form as it appears on your
              government-issued identification.
            </p>
            <v-select
              v-model="organization.legal_form_name"
              :items="legalForms"
              label="Legal Form"
            ></v-select>

            <h3 class="mb-1">Sector</h3>
            <p class="mb-2">
              Please select the sector that best describes your industry or
              field of work.
            </p>
            <v-select
              v-model="organization.sector_names"
              :items="sectors"
              label="Sector"
              multiple
            ></v-select>
          </div>

          <div class="mb-8" id="contacts">
            <h2 class="mb-1">Contacts</h2>
            <p class="mb-1">
              An organization contact and a project contact both refer to
              individuals who can be contacted regarding a particular entity,
              but they differ in scope and responsibility.
            </p>
            <p class="mb-2">
              An organization contact represents the organization as a whole and
              is responsible for overall communication and management, while a
              project contact is associated with a specific project or
              initiative within the organization and is responsible for managing
              the details of the project and serving as the point of contact for
              stakeholders.
            </p>
            <div class="my-4">
              <contact-list :contacts="organization.contacts!"></contact-list>
            </div>
          </div>
        </div>
      </v-col>
    </v-row>
  </v-container>
  <v-navigation-drawer :rail="isRail" location="right" permanent>
    <v-list>
      <v-list-item :title="organization?.name" subtitle="Organization">
        <template v-slot:prepend>
          <v-avatar
            :size="isRail ? 24 : undefined"
            :rounded="isRail || 'lg'"
            color="secondary"
          >
            <strong class="text-white">
              {{ organization?.name.charAt(0).toUpperCase() }}
            </strong>
          </v-avatar>
        </template>
      </v-list-item>
    </v-list>
    <v-divider></v-divider>
    <v-list density="compact" nav>
      <!-- <v-list-item
        :to="{ hash: '#relationship-management' }"
        title="Relationship Management"
        prepend-icon="mdi-account-arrow-right"
        :active="false"
      ></v-list-item> -->
      <v-list-item
        :to="{ hash: '#details' }"
        title="Details"
        prepend-icon="mdi-text-box-search-outline"
        :active="false"
      ></v-list-item>
      <v-list-item
        :to="{ hash: '#contacts' }"
        title="Contacts"
        prepend-icon="mdi-account-arrow-left"
        :active="false"
      ></v-list-item>
      <!-- <v-list-item
        :to="{ hash: '#notes' }"
        title="Notes"
        prepend-icon="mdi-text-box-outline"
        :active="false"
      ></v-list-item> -->
    </v-list>
    <template v-slot:append>
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
import { computed, onBeforeMount, ref } from "vue";
import { useRoute } from "vue-router";
import { apiClient } from "@/plugins/api";
import { OrganizationCreate, OrganizationRead } from "@/services";
import ContactList from "@/components/ContactList.vue";

const route = useRoute();

const breadcrumbs = computed(() => [
  {
    title: "Organizations",
    to: { name: "ListOrganizations" },
    disabled: false,
  },
  {
    title: organization.value?.name || route.params.organizationId,
    to: {
      name: "ViewOrganization",
      params: { organizationId: route.params.organizationId },
    },
    disabled: true,
  },
]);

const isRail = ref(false);

const isLoading = ref(false);
const organization = ref<OrganizationRead>();
const legalForms = Object.values(OrganizationCreate.legal_form_name);
const sectors = ["Bildung", "Gesundheit", "Kultur", "Sport", "Umwelt"];

const fetchOrganization = async () => {
  isLoading.value = true;
  try {
    organization.value = await apiClient.organizations.getOrganization(
      route.params.organizationId.toString(),
    );
  } catch (error) {
    console.error(error);
  } finally {
    isLoading.value = false;
  }
};

onBeforeMount(async () => {
  await fetchOrganization();
});
</script>
