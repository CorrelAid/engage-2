import axios from "axios";

import { AppClient } from "@/services";
import { useAuthStore } from "@/store/auth";
import { useRouter } from "vue-router";

// axios interceptor that logs out user if API returns 401
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response.status === 401) {
      const router = useRouter();
      const authStore = useAuthStore();
      // delete user details if user is not authorized
      authStore.user = null;
      // redirect to login page
      router.push({ name: "Login" });
    }
    return Promise.reject(error);
  },
);

export const apiClient = new AppClient({
  BASE: import.meta.env.VITE_API_BASE_URL,
  WITH_CREDENTIALS: true,
});
