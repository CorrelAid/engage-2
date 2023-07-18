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
    name: "Dashboard",
    path: "/dashboard",
    component: () => import("@/views/Dashboard.vue"),
    meta: { requiresAuth: true },
  },
  {
    name: "Organizations",
    path: "/organizations",
    component: () => import("@/views/Organizations.vue"),
    meta: { requiresAuth: true },
  },
  {
    name: "Organization",
    path: "/organizations/:organizationId",
    component: () => import("@/views/Organization.vue"),
    meta: { requiresAuth: true },
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

router.beforeEach(async (to, from, next) => {
  if (!to.meta.requiresAuth) {
    return next();
  }
  const authentication = useAuthentication();

  await authentication.getMe();
  if (!authentication.isAuthenticated()) {
    return next({ name: "Login" });
  }

  return next();
});

export default router;
