<template>
  <v-app-bar app color="primary" dark>
    <div class="d-flex align-center">
      <v-img
        alt="Vuetify Logo"
        class="shrink mr-2"
        contain
        src="https://cdn.vuetifyjs.com/images/logos/vuetify-logo-dark.png"
        transition="scale-transition"
        width="40"
      />

      <v-img
        alt="Vuetify Name"
        class="shrink mt-1 hidden-sm-and-down"
        contain
        min-width="100"
        src="https://cdn.vuetifyjs.com/images/logos/vuetify-name-dark.png"
        width="100"
      />
    </div>

    <v-spacer></v-spacer>
    <v-btn v-if="isAuthenticated" @click="logout"> Logout </v-btn>
    <v-btn v-else :to="{ name: 'Login' }"> Login </v-btn>
  </v-app-bar>
</template>

<script>
import { mapGetters } from "vuex";
import { supabase } from "../../plugins/supabase";

export default {
  name: "Navigation",
  computed: {
    ...mapGetters("auth", ["isAuthenticated"]),
  },
  methods: {
    async logout() {
      await supabase.auth.signOut();
      this.$store.dispatch("auth/setUser", null);
      this.$store.dispatch("auth/setToken", null);
    },
  },
};
</script>
