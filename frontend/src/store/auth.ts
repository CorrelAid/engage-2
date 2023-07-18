// Utilities
import { apiClient } from "@/plugins/api";
import { UserRead } from "@/services";
import { defineStore } from "pinia";
import { computed, ref } from "vue";

export const useAuthStore = defineStore("app", () => {
  const user = ref<UserRead | null>(null);

  const isAuthenticated = computed<boolean>(() => !!user.value);

  const login = async (email: string, password: string): Promise<void> => {
    await apiClient.auth.authTokenDbLoginAuthLoginPost({
      username: email,
      password: password,
    });
    await fetchUser();
  };

  const logout = async (): Promise<void> => {
    await apiClient.auth.authTokenDbLogoutAuthLogoutPost();
    user.value = null;
  };

  const fetchUser = async (): Promise<void> => {
    try {
      const response = await apiClient.auth.usersCurrentUserAuthMeGet();
      user.value = response;
    } catch (error) {
      user.value = null;
    }
  };

  return {
    user,
    isAuthenticated,
    login,
    logout,
    getMe: fetchUser,
  };
});
