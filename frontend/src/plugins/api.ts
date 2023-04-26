import { AppClient } from "@/services";

export const apiClient = new AppClient({
  BASE: "http://localhost:8000",
});
