import logging
import re
from pages.signup import SignUpPage
from gmail_client import GmailClient


LOGGER = logging.getLogger(__name__)


class TestSignUp:

    def test_signup(self, browser, test_user):
        page = SignUpPage(browser=browser)
        browser.goto_url(url=page.url)
        page.signup(user=test_user)
        browser.wait_till_current_url_changes(url=browser.base_url + "/user/complete", timeout=15)
        gmail_client = GmailClient(email_addr="testerikod@gmail.com", password="password")
        messages = gmail_client.get_messages(to_email=test_user.email, find_before=60)
        assert len(messages) == 1, f"More than one message fot {test_user.email} in the Inbox!"
        email_message_str = str(messages[0])
        match_obj = re.search('<a href="(.+)">', email_message_str)
        assert match_obj is not None, f"Link not found in {email_message_str}"
        verification_link = match_obj.group(1)
        browser.goto_url(url=verification_link, wait_till_changes=False)
        browser.wait_till_current_url_changes(url="https://cloud.scylladb.com/user/signin")
