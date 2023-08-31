import requests

CMS_URL = "https://cms.correlaid.org/graphql"
API_URL = "http://localhost:8000"
API_TEST_USERNAME = "testuser@example.com"
API_TEST_PASSWORD = "testpassword123"  # pragma: allowlist secret

ORGANIZATION_QUERY = """
query Orgs {
    Organizations(filter: {Projects: {Projects_id: {status : {_eq: "published"}}}}) {
        id
        date_created
        date_updated
        legal_form
        sector
        translations {
            languages_code {code}
            name
            description
            website
        }
    }
}
"""

LEGAL_FORM_MAPPING = {
    "e_v": "e.V. - Eingetragener Verein",
    "gug": "gUG - Gemeinnützige Unternehmergesellschaft",
    "stiftung": "Stiftung",
    #  other
    #  no_legal_form
    #  None is also present
}
SECTOR_MAPPING = {
    "environment": "Umwelt",
    # social_services
    # law_advocacy_politics
    # development_housing
    "arts_culture_sports": "Kultur",
    "education_research": "Bildung",
    # professional_associations_unions
}


def create_organization(organization, session):
    org_data = {
        "name": organization["translations"][0]["name"],
        # maybe also store project["translations"][0]["summary"],
        "legal_form": LEGAL_FORM_MAPPING[organization["legal_form"]],
        "sectors": [SECTOR_MAPPING[organization["sector"]]],
    }
    response = session.post(f"{API_URL}/organizations/", json=org_data)
    if response.status_code == 201:
        print(f"Created project {organization['translations'][0]['name']}")
    else:
        print(f"Error creating project {organization['translations'][0]['name']}")
        print(response.json())


def login(session):
    login_data = {
        "username": API_TEST_USERNAME,
        "password": API_TEST_PASSWORD,
    }
    session.post(f"{API_URL}/auth/login", data=login_data)


def insert_public_orgs_in_local_backend():
    response = requests.post(CMS_URL, json={"query": ORGANIZATION_QUERY})
    organizations = response.json()["data"]["Organizations"]

    legal_forms = {org["legal_form"] for org in organizations}
    print(legal_forms)

    session = requests.Session()

    login(session)

    for org in [
        o
        for o in organizations
        if o["legal_form"] in LEGAL_FORM_MAPPING and o["sector"] in SECTOR_MAPPING
    ]:
        create_organization(org, session)


if __name__ == "__main__":
    insert_public_orgs_in_local_backend()
