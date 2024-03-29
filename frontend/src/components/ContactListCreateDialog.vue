<template>
  <v-dialog v-model="isDialogVisible" width="500px">
    <template #activator="{ props }">
      <v-btn v-bind="props" variant="tonal" size="small" color="secondary">
        <v-icon class="mr-1">mdi-plus</v-icon>
        Add Contact
      </v-btn>
    </template>

    <v-card>
      <v-card-title class="d-flex align-center" style="min-height: 52px">
        <div>Create New Contact</div>
      </v-card-title>
      <v-divider></v-divider>
      <v-card-text>
        <v-form
          id="add-contact-form"
          ref="form"
          v-model="isFormValid"
          @submit.prevent="addContact"
        >
          <v-text-field
            v-model="name"
            :rules="[isValueValid]"
            label="Name"
          ></v-text-field>
          <v-select
            v-model="role"
            :items="roles"
            :rules="[isValueValid]"
            label="Role"
          ></v-select>
          <v-text-field
            v-model="email"
            :rules="[isValueValid, isEmailValid]"
            label="Email"
          ></v-text-field>
          <v-text-field
            v-model="phone"
            :rules="[isValueValid]"
            label="Phone"
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
          form="add-contact-form"
          variant="elevated"
          color="secondary"
        >
          Add Contact
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { OrganizationContactRead } from "@/services";
import { ref } from "vue";

const emit = defineEmits<{
  // eslint-disable-next-line no-unused-vars
  (e: "addContact", contact: OrganizationContactRead): void;
}>();

const isDialogVisible = ref(false);
const isFormValid = ref(false);

const form = ref();

const name = ref("");
const role = ref();
const roles = ["Organization Contact", "Project Contact"];
const email = ref("");
const phone = ref("");
const isValueValid = (value: string) =>
  (!!value && value.length > 0) || "Please provide a value.";
const isEmailValid = (value: string) =>
  /.+@.+\..+/.test(value) || "Please provide a valid email.";

const cancel = () => {
  form.value.reset();
  isDialogVisible.value = false;
};

const addContact = () => {
  emit("addContact", {
    name: name.value,
    role: role.value,
    email: email.value,
    phone: phone.value,
  });
  form.value.reset();
  isDialogVisible.value = false;
};
</script>
