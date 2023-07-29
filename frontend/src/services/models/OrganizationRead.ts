/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { OrganizationContactRead } from "./OrganizationContactRead";

export type OrganizationRead = {
  id: string;
  name: string;
  legal_form: OrganizationRead.legal_form;
  sectors: Array<"Bildung" | "Gesundheit" | "Kultur" | "Sport" | "Umwelt">;
  contacts?: Array<OrganizationContactRead>;
  created_at: string;
  created_by: string;
  updated_at: string;
  updated_by: string;
  archived_at: string | null;
  archived_by: string | null;
};

export namespace OrganizationRead {
  export enum legal_form {
    E_V_EINGETRAGENER_VEREIN = "e.V. - Eingetragener Verein",
    G_GMB_H_GEMEINN_TZIGE_GESELLSCHAFT_MIT_BESCHR_NKTER_HAFTUNG = "gGmbH - Gemeinnützige Gesellschaft mit beschränkter Haftung",
    GMB_H_GESELLSCHAFT_MIT_BESCHR_NKTER_HAFTUNG = "GmbH - Gesellschaft mit beschränkter Haftung",
    G_UG_GEMEINN_TZIGE_UNTERNEHMERGESELLSCHAFT = "gUG - Gemeinnützige Unternehmergesellschaft",
    UG_UNTERNEHMERGESELLSCHAFT = "UG - Unternehmergesellschaft",
    STIFTUNG = "Stiftung",
  }
}
