<template>
  <v-container>
    <h1>Projects</h1>
    <v-row>
      <v-col
        cols="12"
        md="6"
        xl="4"
        v-for="project in projects"
        :key="project.id"
      >
        <v-card>
          <v-card-title>{{ project.title }}</v-card-title>
          <v-card-actions>
            <v-btn :to="{ name: 'Project', params: { id: project.id } }">
              Learn more
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { supabase } from "../plugins/supabase";

export default {
  name: "ViewHome",
  data: () => ({
    projects: [],
  }),
  methods: {
    async fetchProjects() {
      try {
        const { data } = await supabase.from("projects").select();
        this.projects = data;
      } catch (error) {
        console.error(error);
      }
    },
  },
  async created() {
    await this.fetchProjects();
  },
};
</script>
