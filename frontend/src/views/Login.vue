<template>
  <v-container class="fill-height">
    <v-row class="justify-center align-center">
      <v-col cols="10" md="6" lg="4">
        <v-card>
          <v-card-text>
            <v-text-field
              v-model="email"
              type="email"
              label="Email"
            ></v-text-field>
            <v-text-field
              v-model="password"
              label="Password"
              :type="isPasswordVisible ? 'text' : 'password'"
              :append-inner-icon="isPasswordVisible ? 'mdi-eye-off' : 'mdi-eye'"
              @click:append-inner="isPasswordVisible = !isPasswordVisible"
            ></v-text-field>
            <div class="d-flex justify-center">
              <v-btn color="secondary">Login</v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { apiClient } from "@/plugins/api";

const isPasswordVisible = ref(false);
const email = ref("");
const password = ref("");

apiClient.auth.authTokenDbLoginAuthLoginPost({
  username: email.value,
  password: password.value,
});
</script>
