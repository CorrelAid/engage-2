import { createClient } from "@supabase/supabase-js";
const supabaseUrl = "https://lyntwkexaazesicgpvnt.supabase.co";
const supabaseAnonKey =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYW5vbiIsImlhdCI6MTYzMzI2NTg5MywiZXhwIjoxOTQ4ODQxODkzfQ.Ff9dA7c4uD0GI9HvGLL_UeN8ATSNJQMLK0bjNsMY0OM";
export const supabase = createClient(supabaseUrl, supabaseAnonKey);
