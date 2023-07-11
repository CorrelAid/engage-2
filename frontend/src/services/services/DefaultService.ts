/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from "../core/CancelablePromise";
import type { BaseHttpRequest } from "../core/BaseHttpRequest";

export class DefaultService {
  constructor(public readonly httpRequest: BaseHttpRequest) {}

  /**
   * Authenticated Route
   * @returns any Successful Response
   * @throws ApiError
   */
  public authenticatedRouteAuthenticatedRouteGet(): CancelablePromise<any> {
    return this.httpRequest.request({
      method: "GET",
      url: "/authenticated-route",
    });
  }
}
