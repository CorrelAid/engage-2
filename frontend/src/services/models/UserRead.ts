/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type UserRead = {
    id: string;
    email: string;
    is_active?: boolean;
    is_superuser?: boolean;
    is_verified?: boolean;
    roles?: Array<string>;
    name: string;
};
