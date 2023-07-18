/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from "../core/CancelablePromise";
import type { BaseHttpRequest } from "../core/BaseHttpRequest";

export class CsrfService {
  constructor(public readonly httpRequest: BaseHttpRequest) {}

  /**
   * Get Csrf
   * @returns void
   * @throws ApiError
   */
  public getCsrfCsrfGet(): CancelablePromise<void> {
    return this.httpRequest.request({
      method: "GET",
      url: "/csrf",
    });
  }
}
