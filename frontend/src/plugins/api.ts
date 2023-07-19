import { AppClient } from "@/services";
import axios from "axios";

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "x-csrftoken";

export const apiClient = new AppClient({
  BASE: "http://localhost:8000",
  WITH_CREDENTIALS: true,
});
