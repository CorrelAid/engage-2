/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { OrganizationContactRead } from "./OrganizationContactRead";

export type OrganizationUpdate = {
  name?: string | null;
  legal_form?:
    | "e.V. - Eingetragener Verein"
    | "gGmbH - Gemeinnützige Gesellschaft mit beschränkter Haftung"
    | "GmbH - Gesellschaft mit beschränkter Haftung"
    | "gUG - Gemeinnützige Unternehmergesellschaft"
    | "UG - Unternehmergesellschaft"
    | "Stiftung"
    | null;
  sectors?: Array<
    "Bildung" | "Gesundheit" | "Kultur" | "Sport" | "Umwelt"
  > | null;
  contacts?: Array<OrganizationContactRead> | null;
};
