// Composables
import { createRouter, createWebHistory } from "vue-router";
import { useAuthentication } from "@/composables/useAuthentication";

const routes = [
  {
    name: "LandingPage",
    path: "/",
    component: () => import("@/views/Home.vue"),
  },
  {
    name: "Login",
    path: "/login",
    component: () => import("@/views/Login.vue"),
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

router.beforeEach((to, from, next) => {
  const authentication = useAuthentication();

  if (!authentication.isAuthenticated() && to.name !== "Login") {
    return next({ name: "Login" });
  }

  return next();
});

export default router;
