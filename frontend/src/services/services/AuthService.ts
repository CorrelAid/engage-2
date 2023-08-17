/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_auth } from "../models/Body_auth";
import type { pydantic__main__Body_reset__1 } from "../models/pydantic__main__Body_reset__1";
import type { pydantic__main__Body_reset__2 } from "../models/pydantic__main__Body_reset__2";
import type { pydantic__main__Body_verify__1 } from "../models/pydantic__main__Body_verify__1";
import type { pydantic__main__Body_verify__2 } from "../models/pydantic__main__Body_verify__2";
import type { UserCreate } from "../models/UserCreate";
import type { UserRead } from "../models/UserRead";
import type { UserUpdate } from "../models/UserUpdate";

import type { CancelablePromise } from "../core/CancelablePromise";
import type { BaseHttpRequest } from "../core/BaseHttpRequest";

export class AuthService {
  constructor(public readonly httpRequest: BaseHttpRequest) {}

  /**
   * Auth:Token-Db.Login
   * @param formData
   * @returns any Successful Response
   * @throws ApiError
   */
  public authTokenDbLogin(formData: Body_auth): CancelablePromise<any> {
    return this.httpRequest.request({
      method: "POST",
      url: "/auth/login",
      formData: formData,
      mediaType: "application/x-www-form-urlencoded",
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
  public authTokenDbLogout(): CancelablePromise<any> {
    return this.httpRequest.request({
      method: "POST",
      url: "/auth/logout",
      errors: {
        401: `Missing token or inactive user.`,
      },
    });
  }

  /**
   * Reset:Forgot Password
   * @param requestBody
   * @returns any Successful Response
   * @throws ApiError
   */
  public resetForgotPassword(
    requestBody: pydantic__main__Body_reset__1,
  ): CancelablePromise<any> {
    return this.httpRequest.request({
      method: "POST",
      url: "/auth/forgot-password",
      body: requestBody,
      mediaType: "application/json",
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
  public resetResetPassword(
    requestBody: pydantic__main__Body_reset__2,
  ): CancelablePromise<any> {
    return this.httpRequest.request({
      method: "POST",
      url: "/auth/reset-password",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        400: `Bad Request`,
        422: `Validation Error`,
      },
    });
  }

  /**
   * Register:Register
   * @param requestBody
   * @returns UserRead Successful Response
   * @throws ApiError
   */
  public registerRegister(
    requestBody: UserCreate,
  ): CancelablePromise<UserRead> {
    return this.httpRequest.request({
      method: "POST",
      url: "/auth/register",
      body: requestBody,
      mediaType: "application/json",
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
  public verifyRequestToken(
    requestBody: pydantic__main__Body_verify__1,
  ): CancelablePromise<any> {
    return this.httpRequest.request({
      method: "POST",
      url: "/auth/request-verify-token",
      body: requestBody,
      mediaType: "application/json",
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
  public verifyVerify(
    requestBody: pydantic__main__Body_verify__2,
  ): CancelablePromise<UserRead> {
    return this.httpRequest.request({
      method: "POST",
      url: "/auth/verify",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        400: `Bad Request`,
        422: `Validation Error`,
      },
    });
  }

  /**
   * Users:Current User
   * @returns UserRead Successful Response
   * @throws ApiError
   */
  public usersCurrentUser(): CancelablePromise<UserRead> {
    return this.httpRequest.request({
      method: "GET",
      url: "/auth/me",
      errors: {
        401: `Missing token or inactive user.`,
      },
    });
  }

  /**
   * Users:Patch Current User
   * @param requestBody
   * @returns UserRead Successful Response
   * @throws ApiError
   */
  public usersPatchCurrentUser(
    requestBody: UserUpdate,
  ): CancelablePromise<UserRead> {
    return this.httpRequest.request({
      method: "PATCH",
      url: "/auth/me",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        400: `Bad Request`,
        401: `Missing token or inactive user.`,
        422: `Validation Error`,
      },
    });
  }

  /**
   * Users:User
   * @param id
   * @returns UserRead Successful Response
   * @throws ApiError
   */
  public usersUser(id: string): CancelablePromise<UserRead> {
    return this.httpRequest.request({
      method: "GET",
      url: "/auth/{id}",
      path: {
        id: id,
      },
      errors: {
        401: `Missing token or inactive user.`,
        403: `Not a superuser.`,
        404: `The user does not exist.`,
        422: `Validation Error`,
      },
    });
  }

  /**
   * Users:Patch User
   * @param id
   * @param requestBody
   * @returns UserRead Successful Response
   * @throws ApiError
   */
  public usersPatchUser(
    id: string,
    requestBody: UserUpdate,
  ): CancelablePromise<UserRead> {
    return this.httpRequest.request({
      method: "PATCH",
      url: "/auth/{id}",
      path: {
        id: id,
      },
      body: requestBody,
      mediaType: "application/json",
      errors: {
        400: `Bad Request`,
        401: `Missing token or inactive user.`,
        403: `Not a superuser.`,
        404: `The user does not exist.`,
        422: `Validation Error`,
      },
    });
  }

  /**
   * Users:Delete User
   * @param id
   * @returns void
   * @throws ApiError
   */
  public usersDeleteUser(id: string): CancelablePromise<void> {
    return this.httpRequest.request({
      method: "DELETE",
      url: "/auth/{id}",
      path: {
        id: id,
      },
      errors: {
        401: `Missing token or inactive user.`,
        403: `Not a superuser.`,
        404: `The user does not exist.`,
        422: `Validation Error`,
      },
    });
  }
}
