/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { OrganizationContactRead } from "./OrganizationContactRead";

export type OrganizationRead = {
  id: string;
  name: string;
  legal_form_name: OrganizationRead.legal_form_name;
  sector_names: Array<"Bildung" | "Gesundheit" | "Kultur" | "Sport" | "Umwelt">;
  contacts?: Array<OrganizationContactRead>;
};

export namespace OrganizationRead {
  export enum legal_form_name {
    E_V_EINGETRAGENER_VEREIN = "e.V. - Eingetragener Verein",
    G_GMB_H_GEMEINN_TZIGE_GESELLSCHAFT_MIT_BESCHR_NKTER_HAFTUNG = "gGmbH - Gemeinnützige Gesellschaft mit beschränkter Haftung",
    GMB_H_GESELLSCHAFT_MIT_BESCHR_NKTER_HAFTUNG = "GmbH - Gesellschaft mit beschränkter Haftung",
    G_UG_GEMEINN_TZIGE_UNTERNEHMERGESELLSCHAFT = "gUG - Gemeinnützige Unternehmergesellschaft",
    UG_UNTERNEHMERGESELLSCHAFT = "UG - Unternehmergesellschaft",
    STIFTUNG = "Stiftung",
  }
}
