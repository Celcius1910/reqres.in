import jsonschema
import pytest
import allure
from jsonschema import validate
from faker import Faker

faker = Faker()

BASE_URL = "https://reqres.in/api"

USER_SCHEMA = {
    "type": "object",
    "properties": {
        "data": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "email": {"type": "string"},
                "first_name": {"type": "string"},
                "last_name": {"type": "string"},
            },
            "required": ["id", "email", "first_name", "last_name"]
        }
    },
    "required": ["data"]
}

LIST_USER_SCHEMA = {
    "type": "object",
    "properties": {
        "page": {"type": "integer"},
        "per_page": {"type": "integer"},
        "total": {"type": "integer"},
        "total_pages": {"type": "integer"},
        "data": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "email": {"type": "string"},
                    "first_name": {"type": "string"},
                    "last_name": {"type": "string"},
                    "avatar": {"type": "string"}
                },
                "required": ["id", "email", "first_name", "last_name", "avatar"]
            }
        }
    },
    "required": ["page", "per_page", "total", "total_pages", "data"]
}

RESOURCE_SCHEMA = {
    "type": "object",
    "properties": {
        "data": {
            "type": "object",
            "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "year": {"type": "integer"},
                    "color": {"type": "string"},
                    "pantone_value": {"type": "string"}
                },
            "required": ["id", "name", "year", "color", "pantone_value"]
        }
    },
    "required": ["data"]
}

LIST_RESOURCE_SCHEMA = {
    "type": "object",
    "properties": {
        "page": {"type": "integer"},
        "per_page": {"type": "integer"},
        "total": {"type": "integer"},
        "total_pages": {"type": "integer"},
        "data": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "year": {"type": "integer"},
                    "color": {"type": "string"},
                    "pantone_value": {"type": "string"}
                },
                "required": ["id", "name", "year", "color", "pantone_value"]
            }
        }
    },
    "required": ["page", "per_page", "total", "total_pages", "data"]
}

@allure.feature("User API")
@allure.story("Get Users List")
def test_get_users(api_client):
    with allure.step("Send GET request to /users?page=2"):
        response = api_client.get(f"{BASE_URL}/users?page=2")

    with allure.step("Validate response status code"):
        assert response.status_code == 200

    with allure.step("Validate response contains 'data' field"):
        assert "data" in response.json()
        
    with allure.step("Validate response matches LIST_USER_SCHEMA"):
        validate(instance=response.json(), schema=LIST_USER_SCHEMA)


@allure.feature("User API")
@allure.story("Get Single User")
def test_single_user(api_client):
    with allure.step("Send GET request to /users/2"):
        response = api_client.get(f"{BASE_URL}/users/2")

    with allure.step("Validate response status code"):
        assert response.status_code == 200

    with allure.step("Validate response matches USER_SCHEMA"):
        validate(instance=response.json(), schema=USER_SCHEMA)

@allure.feature("User API")
@allure.story("Create User")
def test_create_user(api_client):
    name = faker.name()
    job = faker.job()
    payload = {"name": f"{name}", "job": f"{job}"}
    with allure.step("Send POST request to /users"):
        response = api_client.post(f"{BASE_URL}/users", json=payload)

    with allure.step("Validate response status code"):
        assert response.status_code == 201

    with allure.step("Validate response contains correct user name"):
        assert response.json()["name"] == name
    
    with allure.step("Validate response contains correct job"):
        assert response.json()["job"] == job

@allure.feature("User API")
@allure.story("Delete User")
def test_delete_user(api_client):
    with allure.step("Send DELETE request to /users/2"):
        response = api_client.delete(f"{BASE_URL}/users/2")

    with allure.step("Validate response status code"):
        assert response.status_code == 204

@allure.feature("Resource API")
@allure.story("Get Resource List")
def test_get_resource(api_client):
    with allure.step("Send GET request to /unknown"):
        response = api_client.get(f"{BASE_URL}/unknown")

    with allure.step("Validate response status code"):
        assert response.status_code == 200

    with allure.step("Validate response contains 'data' field"):
        assert "data" in response.json()
        
    with allure.step("Validate response matches LIST_RESOURCE_SCHEMA"):
        validate(instance=response.json(), schema=LIST_RESOURCE_SCHEMA)

@allure.feature("Resource API")
@allure.story("Get Single Resource")
def test_single_resource(api_client):
    with allure.step("Send GET request to /unknown/5"):
        response = api_client.get(f"{BASE_URL}/unknown/5")

    with allure.step("Validate response status code"):
        assert response.status_code == 200

    with allure.step("Validate response matches RESOURCE_SCHEMA"):
        validate(instance=response.json(), schema=RESOURCE_SCHEMA)