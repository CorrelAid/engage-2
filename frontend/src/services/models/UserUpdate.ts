/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type UserUpdate = {
  password?: string | null;
  email?: string | null;
  is_active?: boolean | null;
  is_superuser?: boolean | null;
  is_verified?: boolean | null;
  roles?: Array<string>;
  name: string;
};
