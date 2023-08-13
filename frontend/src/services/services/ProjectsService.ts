/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CreateProject } from "../models/CreateProject";
import type { ReadProject } from "../models/ReadProject";
import type { UpdateProject } from "../models/UpdateProject";

import type { CancelablePromise } from "../core/CancelablePromise";
import type { BaseHttpRequest } from "../core/BaseHttpRequest";

export class ProjectsService {
  constructor(public readonly httpRequest: BaseHttpRequest) {}

  /**
   * List Projects
   * @returns ReadProject List all projects
   * @throws ApiError
   */
  public listProjects(): CancelablePromise<Array<ReadProject>> {
    return this.httpRequest.request({
      method: "GET",
      url: "/projects/",
    });
  }

  /**
   * Create Project
   * @param requestBody
   * @returns ReadProject Create a new project
   * @throws ApiError
   */
  public createProject(
    requestBody: CreateProject,
  ): CancelablePromise<ReadProject> {
    return this.httpRequest.request({
      method: "POST",
      url: "/projects/",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Read Project
   * @param projectId
   * @returns ReadProject Get a single project
   * @throws ApiError
   */
  public readProject(projectId: string): CancelablePromise<ReadProject> {
    return this.httpRequest.request({
      method: "GET",
      url: "/projects/{project_id}",
      path: {
        project_id: projectId,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Delete Project
   * @param projectId
   * @returns void
   * @throws ApiError
   */
  public deleteProject(projectId: string): CancelablePromise<void> {
    return this.httpRequest.request({
      method: "DELETE",
      url: "/projects/{project_id}",
      path: {
        project_id: projectId,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Update Project
   * @param projectId
   * @param requestBody
   * @returns ReadProject Update a single project
   * @throws ApiError
   */
  public updateProject(
    projectId: string,
    requestBody: UpdateProject,
  ): CancelablePromise<ReadProject> {
    return this.httpRequest.request({
      method: "PATCH",
      url: "/projects/{project_id}",
      path: {
        project_id: projectId,
      },
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }
}
