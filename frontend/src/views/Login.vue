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
            <v-expand-transition>
              <div v-if="error" class="mb-4">
                <v-alert density="compact" type="error">
                  {{ error }}
                </v-alert>
              </div>
            </v-expand-transition>
            <div class="d-flex justify-center">
              <v-btn :loading="isLoading" color="secondary" @click="login">
                Login
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import router from "@/router";
import { useAuthStore } from "@/store/auth";
import { ref } from "vue";

const authStore = useAuthStore();

const isLoading = ref(false);
const error = ref<string | boolean>(false);

const isPasswordVisible = ref(false);
const email = ref("");
const password = ref("");

const login = async () => {
  isLoading.value = true;
  error.value = false;
  try {
    await authStore.login(email.value, password.value);
    router.push({ name: "Dashboard" });
  } catch (e) {
    error.value = "Invalid email or password.";
  } finally {
    isLoading.value = false;
  }
};
</script>
