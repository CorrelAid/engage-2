/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { OrganizationCreate } from "../models/OrganizationCreate";
import type { OrganizationRead } from "../models/OrganizationRead";
import type { OrganizationUpdate } from "../models/OrganizationUpdate";

import type { CancelablePromise } from "../core/CancelablePromise";
import type { BaseHttpRequest } from "../core/BaseHttpRequest";

export class OrganizationsService {
  constructor(public readonly httpRequest: BaseHttpRequest) {}

  /**
   * List Organizations
   * @returns OrganizationRead Successful Response
   * @throws ApiError
   */
  public listOrganizations(): CancelablePromise<Array<OrganizationRead>> {
    return this.httpRequest.request({
      method: "GET",
      url: "/organizations",
    });
  }

  /**
   * Create Organization
   * @param requestBody
   * @returns OrganizationRead Successful Response
   * @throws ApiError
   */
  public createOrganization(
    requestBody: OrganizationCreate,
  ): CancelablePromise<OrganizationRead> {
    return this.httpRequest.request({
      method: "POST",
      url: "/organizations",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Get Organization
   * @param organizationId
   * @returns OrganizationRead Successful Response
   * @throws ApiError
   */
  public getOrganization(
    organizationId: string,
  ): CancelablePromise<OrganizationRead> {
    return this.httpRequest.request({
      method: "GET",
      url: "/organizations/{organization_id}",
      path: {
        organization_id: organizationId,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Update Organization
   * @param organizationId
   * @param requestBody
   * @returns OrganizationRead Successful Response
   * @throws ApiError
   */
  public updateOrganization(
    organizationId: string,
    requestBody: OrganizationUpdate,
  ): CancelablePromise<OrganizationRead> {
    return this.httpRequest.request({
      method: "PATCH",
      url: "/organizations/{organization_id}",
      path: {
        organization_id: organizationId,
      },
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Delete Organization
   * @param organizationId
   * @returns void
   * @throws ApiError
   */
  public deleteOrganization(organizationId: string): CancelablePromise<void> {
    return this.httpRequest.request({
      method: "DELETE",
      url: "/organizations/{organization_id}",
      path: {
        organization_id: organizationId,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Archive Organization
   * @param organizationId
   * @returns OrganizationRead Successful Response
   * @throws ApiError
   */
  public archiveOrganization(
    organizationId: string,
  ): CancelablePromise<OrganizationRead> {
    return this.httpRequest.request({
      method: "PATCH",
      url: "/organizations/{organization_id}/archive",
      path: {
        organization_id: organizationId,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }
}
