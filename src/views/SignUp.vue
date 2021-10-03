<template>
  <v-container class="fill-height align-center justify-center">
    <v-card width="400px">
      <v-card-title>Sign Up</v-card-title>
      <v-card-text>
        <v-text-field v-model="email" label="Email" outlined></v-text-field>
        <v-text-field
          v-model="password"
          label="Password"
          outlined
        ></v-text-field>
      </v-card-text>
      <v-card-actions>
        <v-btn @click="signUp">Login</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
import { supabase } from "../plugins/supabase";

export default {
  name: "ViewSignUp",
  data: () => ({
    email: "",
    password: "",
  }),
  methods: {
    async signUp() {
      await supabase.auth.signUp({
        email: this.email,
        password: this.password,
      });
      this.$router.push({ name: "Login" });
    },
  },
};
</script>
