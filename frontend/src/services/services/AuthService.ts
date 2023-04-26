/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_auth_token_db_login_auth_login_post } from '../models/Body_auth_token_db_login_auth_login_post';
import type { Body_reset_forgot_password_auth_forgot_password_post } from '../models/Body_reset_forgot_password_auth_forgot_password_post';
import type { Body_reset_reset_password_auth_reset_password_post } from '../models/Body_reset_reset_password_auth_reset_password_post';
import type { Body_verify_request_token_auth_request_verify_token_post } from '../models/Body_verify_request_token_auth_request_verify_token_post';
import type { Body_verify_verify_auth_verify_post } from '../models/Body_verify_verify_auth_verify_post';
import type { UserCreate } from '../models/UserCreate';
import type { UserRead } from '../models/UserRead';

import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';

export class AuthService {

    constructor(public readonly httpRequest: BaseHttpRequest) {}

    /**
     * Auth:Token-Db.Login
     * @param formData
     * @returns any Successful Response
     * @throws ApiError
     */
    public authTokenDbLoginAuthLoginPost(
        formData: Body_auth_token_db_login_auth_login_post,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/auth/login',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
            errors: {
                400: `Bad Request`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Auth:Token-Db.Logout
     * @returns any Successful Response
     * @throws ApiError
     */
    public authTokenDbLogoutAuthLogoutPost(): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/auth/logout',
            errors: {
                401: `Missing token or inactive user.`,
            },
        });
    }

    /**
     * Register:Register
     * @param requestBody
     * @returns UserRead Successful Response
     * @throws ApiError
     */
    public registerRegisterAuthRegisterPost(
        requestBody: UserCreate,
    ): CancelablePromise<UserRead> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/auth/register',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Bad Request`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Reset:Forgot Password
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public resetForgotPasswordAuthForgotPasswordPost(
        requestBody: Body_reset_forgot_password_auth_forgot_password_post,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/auth/forgot-password',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Reset:Reset Password
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public resetResetPasswordAuthResetPasswordPost(
        requestBody: Body_reset_reset_password_auth_reset_password_post,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/auth/reset-password',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Bad Request`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Verify:Request-Token
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public verifyRequestTokenAuthRequestVerifyTokenPost(
        requestBody: Body_verify_request_token_auth_request_verify_token_post,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/auth/request-verify-token',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Verify:Verify
     * @param requestBody
     * @returns UserRead Successful Response
     * @throws ApiError
     */
    public verifyVerifyAuthVerifyPost(
        requestBody: Body_verify_verify_auth_verify_post,
    ): CancelablePromise<UserRead> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/auth/verify',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Bad Request`,
                422: `Validation Error`,
            },
        });
    }

}
