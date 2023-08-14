import requests

CMS_URL = "https://cms.correlaid.org/graphql"
API_URL = "http://localhost:8000"
API_TEST_USERNAME = "testuser@example.com"
API_TEST_PASSWORD = "testpassword123"  # pragma: allowlist secret

PROJECT_QUERY = """
query ProjectOverview($language: String = "de-DE") {
    Projects(filter: { status: { _in: ["published"] } }) {
        status
        project_id
        is_internal
        translations(filter: { languages_code: { code: { _eq: $language } } }) {
            title
            description
            summary
        }
    }
}
"""


def create_project(project, session):
    project_data = {
        "title": project["translations"][0]["title"],
        "summary": project["translations"][0]["summary"],
        "status": project["status"],
    }
    response = session.post(f"{API_URL}/projects/", json=project_data)
    if response.status_code == 201:
        print(f"Created project {project['translations'][0]['title']}")
    else:
        print(f"Error creating project {project['translations'][0]['title']}")
        print(response.json())


def login(session):
    login_data = {
        "username": API_TEST_USERNAME,
        "password": API_TEST_PASSWORD,
    }
    session.post(f"{API_URL}/auth/login", data=login_data)


def insert_public_projects_in_local_backend():
    response = requests.post(CMS_URL, json={"query": PROJECT_QUERY})
    projects = response.json()["data"]["Projects"]

    session = requests.Session()

    login(session)

    for project in projects:
        create_project(project, session)


if __name__ == "__main__":
    insert_public_projects_in_local_backend()
