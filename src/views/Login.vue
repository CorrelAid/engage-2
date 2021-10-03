<template>
  <v-container class="fill-height align-center justify-center">
    <v-card width="400px">
      <v-card-text>
        <v-text-field
          v-model="email"
          label="Email"
          name="email"
          outlined
        ></v-text-field>
        <v-text-field
          v-model="password"
          label="Password"
          name="password"
          outlined
        ></v-text-field>
      </v-card-text>
      <v-card-actions class="justify-center">
        <v-btn @click="login">Login</v-btn>
        <router-link :to="{ name: 'SignUp' }">
          No account yet? Sign up!
        </router-link>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
import { supabase } from "../plugins/supabase";

export default {
  name: "ViewLogin",
  data: () => ({
    email: "",
    password: "",
  }),
  methods: {
    async login() {
      try {
        const { user, session } = await supabase.auth.signIn({
          email: this.email,
          password: this.password,
        });
        this.$store.dispatch("auth/setUser", user);
        this.$store.dispatch("auth/setToken", session);
        this.$router.push({ name: "Dashboard" });
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>
