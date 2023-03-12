<template>
  <v-container>
    <v-row class="justify-center">
      <v-col cols="12" md="10" lg="8">
        <v-breadcrumbs :items="breadcrumbs" class="px-0"></v-breadcrumbs>
        <div v-if="organization">
          <h1 class="mb-5">{{ organization?.name }}</h1>
          <div class="mb-8" id="relationship-management">
            <h2 class="mb-1">Relationship Management</h2>

            <h3 class="mb-1">Relationship Team</h3>
            <p class="mb-2">
              Please provide the names or titles of the members of your
              relationship team for this account or service.
            </p>
            <v-select
              v-model="organization.relationship_team"
              :items="relationshipTeams"
              item-title="name"
              return-object
            ></v-select>

            <h3 class="mb-1">Relationship Manager</h3>
            <p class="mb-2">
              Please provide the name of your relationship manager or point of
              contact for thisp account or service.
            </p>
            <v-select
              v-model="organization.relationship_contact"
              :items="relationshipContacts"
              item-title="name"
              return-object
            ></v-select>
          </div>

          <div class="mb-8" id="details">
            <h2 class="mb-1">Details</h2>

            <h3 class="mb-1">Legal Form</h3>
            <p class="mb-2">
              Please provide the legal form as it appears on your
              government-issued identification.
            </p>
            <v-select
              v-model="organization.legal_form"
              :items="legalForms"
              label="Legal Form"
            ></v-select>

            <h3 class="mb-1">Sector</h3>
            <p class="mb-2">
              Please select the sector that best describes your industry or
              field of work.
            </p>
            <v-select
              v-model="organization.sector"
              :items="sectors"
              label="Sector"
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
            <v-list>
              <v-list-item
                v-for="contact in organization.contacts"
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
                  {{ contact.type }}
                  <br />
                  {{ contact.email }}
                  <br />
                  {{ contact.phone }}
                </template>
              </v-list-item>
            </v-list>
            <v-btn variant="tonal" size="small" color="secondary">
              <v-icon class="mr-1">mdi-plus</v-icon>
              Add Contact
            </v-btn>
          </div>

          <div id="notes">
            <h2 class="mb-1">Notes</h2>
            <p class="mb-2">
              You can use the <strong>Notes</strong> field to record additional
              information. It is used to capture details that may not fit into
              other fields and is important for keeping a record of interactions
              and progress.
            </p>
            <v-textarea v-model="organization.notes"></v-textarea>
          </div>
        </div>
      </v-col>
    </v-row>
  </v-container>
  <v-navigation-drawer :rail="isRail" location="right" permanent>
    <v-list>
      <v-list-item :title="organization?.name" subtitle="Organization">
      </v-list-item>
    </v-list>
    <v-divider></v-divider>
    <v-list density="compact" nav>
      <v-list-item
        :to="{ hash: '#relationship-management' }"
        title="Relationship Management"
        prepend-icon="mdi-account-arrow-right"
        :active="false"
      ></v-list-item>
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
      <v-list-item
        :to="{ hash: '#notes' }"
        title="Notes"
        prepend-icon="mdi-text-box-outline"
        :active="false"
      ></v-list-item>
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

const route = useRoute();

const breadcrumbs = computed(() => [
  { title: "Organizations", to: { name: "Organizations" }, disabled: false },
  {
    title: organization.value?.name || route.params.organizationId,
    to: {
      name: "Organization",
      params: { organizationId: route.params.organizationId },
    },
    disabled: true,
  },
]);

const isRail = ref(false);

interface OrganizationContact {
  name: string;
  email: string;
  phone: string;
  type: "Organization Contact" | "Project Contact";
}

interface Organization {
  id: string;
  name: string;
  legal_form: string;
  sector: string;
  relationship_team: {
    id: string;
    name: string;
  };
  relationship_contact: {
    id: string;
    name: string;
  };
  contacts: OrganizationContact[];
  notes: string;
}

const legalForms = [
  "e.V. - Eingetragener Verein",
  "gGmbH - Gemeinnützige Gesellschaft mit beschränkter Haftung",
  "gUG - gemeinnützige Unternehmergesellschaft (haftungsbeschränkt)",
  "Stiftung",
];

const sectors = [
  "LGBTQ+ organizations",
  "Women's and gender equality organizations",
  "Environmental and conservation organizations",
  "Community development and advocacy groups",
  "Healthcare and social services organizations",
  "Education and youth development organizations",
  "Arts and culture organizations",
  "International and humanitarian aid organizations",
  "Religious and faith-based organizations",
  "Animal welfare organizations",
  "Housing and homelessness organizations",
  "Civil rights and social justice organizations",
  "Disabilities and special needs organizations",
  "Sports and recreation organizations",
];

const relationshipTeams = [
  {
    id: "460b02df-64aa-4fc5-b773-f936b83266bd",
    name: "CorrelAid Germany",
  },
  {
    id: "da942b5f-de2a-4d20-8a32-9921ab9923cf",
    name: "Local Chapter Konstanz",
  },
  {
    id: "9cac22bc-229b-4036-805f-f4fb7234b40f",
    name: "Local Chapter Bremen",
  },
];
const relationshipContacts = [
  {
    id: "0618cfa8-d1ca-4af7-a189-da3bf1ba169e",
    name: "Frie",
  },
  {
    id: "9ae39299-0c10-43cd-aead-6ec69a332a52",
    name: "Isabelle",
  },
  {
    id: "18c8fae0-4062-4e86-bcc0-858d4c16b41f",
    name: "Phillip",
  },
];

const isLoading = ref(false);
const organization = ref<Organization>();

const fetchOrganization = async () => {
  organization.value = {
    id: "2345a5a1-5e4a-445e-b3e8-9179c978476a",
    name: "Deutscher Caritasverband e.V.",
    legal_form: "e.V. - Eingetragener Verein",
    sector: "Community development and advocacy groups",
    relationship_team: {
      id: "460b02df-64aa-4fc5-b773-f936b83266bd",
      name: "CorrelAid Germany",
    },
    relationship_contact: {
      id: "0618cfa8-d1ca-4af7-a189-da3bf1ba169e",
      name: "Frie",
    },
    contacts: [
      {
        name: "Susie Harper",
        email: "ruw@tujep.tg",
        phone: "+49 176 2032 0211",
        type: "Organization Contact",
      },
      {
        name: "Johnny Briggs",
        email: "ekofut@papgula.pa",
        phone: "+49 176 2032 1111",
        type: "Project Contact",
      },
    ],
    notes:
      "Die Caritas ist mehr als eine Organisation. Sie ist eine Grundhaltung gegenüber Menschen, besonders gegenüber Menschen in Not. Wie er sieht die Caritas ihre Aufgabe darin, den Menschen ohne Ansehen von Herkunft, Status oder Religion mit Liebe und Achtung zu begegnen.",
  };
};

onBeforeMount(async () => {
  await fetchOrganization();
});
</script>
