import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/store/auth";

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

/* eslint-disable no-unused-vars */
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
/* eslint-enable no-unused-vars */

router.beforeEach(async (to, from, next) => {
  if (!to.meta.requiresAuth) {
    return next();
  }
  const authStore = useAuthStore();

  await authStore.refresh();
  if (!authStore.isAuthenticated) {
    return next({ name: "Login" });
  }

  return next();
});

export default router;
