/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

/**
 * Base User model.
 */
export type UserRead = {
    id?: any;
    email: string;
    is_active?: boolean;
    is_superuser?: boolean;
    is_verified?: boolean;
    roles?: Array<string>;
    local_chapter?: string;
    first_name: string;
    surname: string;
    gender?: string;
};
