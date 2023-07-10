/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type UserUpdate = {
    password?: string;
    email?: string;
    is_active?: boolean;
    is_superuser?: boolean;
    is_verified?: boolean;
    roles?: Array<string>;
    local_chapter?: string;
    first_name: string;
    surname: string;
    gender?: string;
};
