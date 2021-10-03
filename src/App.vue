<template>
  <v-app>
    <navigation></navigation>
    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
import Navigation from "./components/application/Navigation.vue";
import { supabase } from "./plugins/supabase";

export default {
  components: { Navigation },
  name: "App",
  computed: {},
  async created() {
    try {
      const { data, user, error } = await supabase.auth.refreshSession();
      if (error) throw error;
      console.log(data);
      this.$store.dispatch("auth/setUser", user);
      this.$store.dispatch("auth/setToken", data);
    } catch (error) {
      console.error(error);
    }
  },
};
</script>
