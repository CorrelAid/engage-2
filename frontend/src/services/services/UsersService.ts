/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { UserRead } from "../models/UserRead";
import type { UserUpdate } from "../models/UserUpdate";

import type { CancelablePromise } from "../core/CancelablePromise";
import type { BaseHttpRequest } from "../core/BaseHttpRequest";

export class UsersService {
  constructor(public readonly httpRequest: BaseHttpRequest) {}

  /**
   * Users:Current User
   * @returns UserRead Successful Response
   * @throws ApiError
   */
  public usersCurrentUserUsersMeGet(): CancelablePromise<UserRead> {
    return this.httpRequest.request({
      method: "GET",
      url: "/users/me",
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
  public usersPatchCurrentUserUsersMePatch(
    requestBody: UserUpdate,
  ): CancelablePromise<UserRead> {
    return this.httpRequest.request({
      method: "PATCH",
      url: "/users/me",
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
  public usersUserUsersIdGet(id: any): CancelablePromise<UserRead> {
    return this.httpRequest.request({
      method: "GET",
      url: "/users/{id}",
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
   * Users:Delete User
   * @param id
   * @returns void
   * @throws ApiError
   */
  public usersDeleteUserUsersIdDelete(id: any): CancelablePromise<void> {
    return this.httpRequest.request({
      method: "DELETE",
      url: "/users/{id}",
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
  public usersPatchUserUsersIdPatch(
    id: any,
    requestBody: UserUpdate,
  ): CancelablePromise<UserRead> {
    return this.httpRequest.request({
      method: "PATCH",
      url: "/users/{id}",
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
}
