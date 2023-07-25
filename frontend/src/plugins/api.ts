import { AppClient } from "@/services";

export const apiClient = new AppClient({
  BASE: import.meta.env.VITE_API_BASE_URL,
  WITH_CREDENTIALS: true,
});
