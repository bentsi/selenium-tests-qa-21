import datetime

import pytest

from basetest import User
from browser import Browser


@pytest.fixture(scope="session")
def test_id():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


@pytest.fixture(scope="session")
def browser():
    browser_obj = Browser(base_url="https://cloud.scylladb.com")
    yield browser_obj
    browser_obj.quit()


@pytest.fixture(scope="session")
def test_user(test_id):
    return User(
        first_name="Testeriko",
        last_name="Qaisky",
        email=f"<your email>+{test_id}@gmail.com",  # use the test email
        company="Testing Professionals",
        country="Russia",
        phone="+79207657855",
    )
