<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1>{{ project.title }}</h1>
      </v-col>
      <v-col cols="12" md="8" xl="9">
        <p class="overline mb-0">Description</p>
        <p>{{ project.description }}</p>
      </v-col>
      <v-col cols="12" md="4" xl="3">
        <p class="overline mb-0">Created at</p>
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <span v-bind="attrs" v-on="on">
              {{ dayjs(project.created_at).fromNow() }}
            </span>
          </template>
          <span>{{ dayjs(project.created_at).format("lll") }}</span>
        </v-tooltip>
        <p class="overline mb-0">Updated at</p>
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <span v-bind="attrs" v-on="on">
              {{ dayjs(project.updated_at).fromNow() }}
            </span>
          </template>
          <span>{{ dayjs(project.updated_at).format("lll") }}</span>
        </v-tooltip>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { supabase } from "../plugins/supabase";

export default {
  name: "ViewProject",
  data: () => ({
    project: {},
  }),
  methods: {
    async fetchProject() {
      try {
        const { data } = await supabase
          .from("projects")
          .select()
          .eq("id", this.$route.params.id)
          .single();
        this.project = data;
      } catch (error) {
        console.error(error);
      }
    },
  },
  async created() {
    await this.fetchProject();
  },
};
</script>
