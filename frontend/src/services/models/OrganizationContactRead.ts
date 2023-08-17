/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type OrganizationContactRead = {
  name: string;
  role: OrganizationContactRead.role;
  email: string;
  phone: string;
};

export namespace OrganizationContactRead {
  export enum role {
    ORGANIZATION_CONTACT = "Organization Contact",
    PROJECT_CONTACT = "Project Contact",
  }
}
