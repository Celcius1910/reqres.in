import pytest
import httpx
import os
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("BASE_URL", "https://reqres.in/api")


@pytest.fixture(scope="session")
def api_client():
    return httpx.Client(base_url=BASE_URL)
