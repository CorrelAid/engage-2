// Composables
import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    name: "LandingPage",
    path: "/",
    component: () => import("@/views/Home.vue"),
  },
  {
    name: "Organizations",
    path: "/organizations",
    component: () => import("@/views/Organizations.vue"),
  },
  {
    name: "Organization",
    path: "/organizations/:organizationId",
    component: () => import("@/views/Organization.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (to.hash) {
      return {
        el: to.hash,
        behavior: "smooth",
      };
    }
  },
});

export default router;
