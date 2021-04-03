import datetime
import logging
import pytest
from pathlib import Path
from basetest import User
from browser import Browser


def setup_logging(test_id):
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    # basic logging
    # logging.basicConfig(filename=f'scylla-cloud.log', level=logging.INFO,
    #                     format="[%(asctime)s] - %(levelname)s - <%(module)s>: %(message)s ")
    root_logger = logging.getLogger()

    file_handler = logging.FileHandler(logs_dir / f'scylla-cloud_{test_id}.log')
    file_handler.setLevel(logging.DEBUG)

    log_format = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s - %(message)s')
    file_handler.setFormatter(log_format)
    root_logger.addHandler(file_handler)
    root_logger.setLevel(logging.DEBUG)
    # disable debug log messages
    selenium_logger = logging.getLogger("selenium")
    selenium_logger.setLevel(logging.INFO)

    urllib3 = logging.getLogger("urllib3")
    urllib3.setLevel(logging.INFO)


@pytest.fixture(scope="session")
def test_id():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


@pytest.fixture(scope="session")
def browser(test_id):
    setup_logging(test_id)
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
