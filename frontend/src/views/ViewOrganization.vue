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

        <div v-if="updatedOrganization && !isLoading">
          <div class="d-flex align-center justify-space-between mb-5">
            <h1
              id="organizationName"
              ref="organizationName"
              class="d-flex flex-grow-1"
              contenteditable="true"
              @keydown.enter="updateName"
              @blur="updateName"
            >
              {{ updatedOrganization.name }}
            </h1>
            <v-icon class="ml-2" @click="focusOrganizationName">
              mdi-pencil
            </v-icon>
          </div>

          <div class="mb-8" id="details">
            <h2 class="mb-1">Details</h2>

            <h3 class="mb-1">Legal Form</h3>
            <p class="mb-2">
              Please provide the legal form as it appears on your
              government-issued identification.
            </p>
            <v-select
              v-model="updatedOrganization.legal_form"
              :items="legalForms"
              label="Legal Form"
            ></v-select>

            <h3 class="mb-1">Sector</h3>
            <p class="mb-2">
              Please select the sector that best describes your industry or
              field of work.
            </p>
            <v-select
              v-model="updatedOrganization.sectors"
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
              <contact-list
                :contacts="updatedOrganization.contacts!"
                @add-contact="updatedOrganization.contacts!.push($event)"
                @delete-contact="
                  updatedOrganization.contacts!.splice(
                    updatedOrganization.contacts!.indexOf($event),
                    1,
                  )
                "
              ></contact-list>
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
      <div class="pa-2">
        <v-btn
          :disabled="_isEqual(organization, updatedOrganization)"
          :loading="isUpdateLoading"
          variant="tonal"
          color="secondary"
          block
          @click="updateOrganization"
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
import {
  OrganizationCreate,
  OrganizationRead,
  OrganizationUpdate,
} from "@/services";
import ContactList from "@/components/ContactList.vue";
import { isEqual as _isEqual } from "lodash-es";

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
const updatedOrganization = ref<OrganizationUpdate>();
const legalForms = Object.values(OrganizationCreate.legal_form);
const sectors = ["Bildung", "Gesundheit", "Kultur", "Sport", "Umwelt"];

const fetchOrganization = async () => {
  isLoading.value = true;
  const startTime = new Date();
  try {
    const response = (organization.value =
      await apiClient.organizations.getOrganization(
        route.params.organizationId.toString(),
      ));
    organization.value = structuredClone(response);
    updatedOrganization.value = structuredClone(response);
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

const organizationName = ref();
const isUpdateLoading = ref(false);

const focusOrganizationName = async () => {
  const nameElement = document.getElementById("organizationName");
  nameElement?.focus();
};

const updateName = async (event: Event) => {
  (event.target as HTMLInputElement).blur();
  updatedOrganization.value!.name = (
    event.target as HTMLInputElement
  ).innerText;
};

const updateOrganization = async () => {
  isUpdateLoading.value = true;
  const startTime = new Date();
  try {
    const response = await apiClient.organizations.updateOrganization(
      route.params.organizationId.toString(),
      updatedOrganization.value!,
    );
    organization.value = structuredClone(response);
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
  await fetchOrganization();
});
</script>
