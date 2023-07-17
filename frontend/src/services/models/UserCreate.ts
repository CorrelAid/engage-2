/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type UserCreate = {
    email: string;
    password: string;
    is_active?: (boolean | null);
    is_superuser?: (boolean | null);
    is_verified?: (boolean | null);
    roles?: Array<string>;
    name: string;
};
