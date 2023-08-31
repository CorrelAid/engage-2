import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/store/auth";

const routes = [
  {
    path: "/",
    redirect: { name: "Dashboard" },
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
    name: "ListOrganizations",
    path: "/organizations",
    component: () => import("@/views/ListOrganizations.vue"),
    meta: { requiresAuth: true },
  },
  {
    name: "CreateOrganization",
    path: "/organizations/create",
    component: () => import("@/views/CreateOrganization.vue"),
    meta: { requiresAuth: true },
  },
  {
    name: "ViewOrganization",
    path: "/organizations/:organizationId",
    component: () => import("@/views/ViewOrganization.vue"),
    meta: { requiresAuth: true },
  },
  {
    name: "ListProjects",
    path: "/projects",
    component: () => import("@/views/ListProjects.vue"),
    meta: { requiresAuth: true },
  },
  {
    name: "CreateProject",
    path: "/projects/create",
    component: () => import("@/views/CreateProject.vue"),
    meta: { requiresAuth: true },
  },
  {
    name: "ViewProject",
    path: "/projects/:projectId",
    component: () => import("@/views/ViewProject.vue"),
    meta: { requiresAuth: true },
  },
];

/* eslint-disable no-unused-vars */
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
  scrollBehavior(to) {
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
