// Utilities
import { apiClient } from "@/plugins/api";
import { UserRead } from "@/services";
import { defineStore } from "pinia";
import { computed, ref } from "vue";

export const useAuthStore = defineStore("app", () => {
  const user = ref<UserRead | null>(null);

  const isAuthenticated = computed<boolean>(() => !!user.value);

  const login = async (email: string, password: string): Promise<void> => {
    await apiClient.auth.authTokenDbLogin({
      username: email,
      password: password,
    });
    user.value = await fetchUser();
  };

  const refresh = async (): Promise<void> => {
    user.value = await fetchUser();
  };

  const logout = async (): Promise<void> => {
    await apiClient.auth.authTokenDbLogout();
    user.value = null;
  };

  const fetchUser = async (): Promise<UserRead | null> => {
    try {
      const response = await apiClient.auth.usersCurrentUser();
      return response;
    } catch (error) {
      return null;
    }
  };

  return {
    user,
    isAuthenticated,
    login,
    logout,
    refresh,
  };
});
