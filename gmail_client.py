import email
import logging
from datetime import datetime, timedelta
from imaplib import IMAP4_SSL, IMAP4

from dateutil.tz import tz

LOGGER = logging.getLogger(__name__)


class GmailClient:
    SERVER = "imap.gmail.com"
    PORT = 993

    def __init__(self, email_addr, password):
        LOGGER.info("Setting up Gmail client...")
        self.email_address = email_addr
        self.password = password
        self.client = None  # IMAP4_SSL
        self.connect()

    def connect(self):
        LOGGER.info("Connecting to Gmail server...")
        self.client = IMAP4_SSL(host=self.SERVER)
        self.client.login(self.email_address, self.password)
        self.client.select('inbox')

    @staticmethod
    def _check_response(resp: str):
        LOGGER.debug("IMAP response: %s", resp)
        assert resp == "OK", "IMAP client error: command unknown or arguments invalid"

    def get_message_ids(self, search_criteria):
        LOGGER.info("Getting message ids...")
        self.client.noop()  # https://tools.ietf.org/html/rfc3501#section-6.1.2
        res, data = self.client.search(None, search_criteria)
        self._check_response(res)
        msg_ids = data[0].decode().split()
        LOGGER.debug("Got message ids: %s", msg_ids)
        return msg_ids

    def fetch_emails(self, message_ids, current_utc_time, date_format):
        email_messages = []
        for i in message_ids:
            res, data = self.client.fetch(i, '(RFC822)')
            self._check_response(res)
            for response_part in data:
                if not isinstance(response_part, tuple):
                    continue
                msg = email.message_from_string(tuple(response_part)[1].decode())
                LOGGER.info("Found the following msg '{}':"
                            "\nFROM: '{}'\nTO: '{}'\nSubject: '{}'\nDATE: '{}'"
                            "".format(i, msg["from"], msg["to"], msg["subject"], msg["date"]))
                # Convert email date to local UTC time
                msg_date = datetime.strptime(msg["date"], date_format).astimezone(tz=tz.tzlocal()).replace(
                    tzinfo=None)
                if (msg_date - current_utc_time).total_seconds() >= 0:
                    email_messages.append(msg)
        return email_messages

    def get_messages(self, to_email, from_email=None,  # pylint: disable=too-many-arguments
                     search_in_all_folders=True, is_new_emails=True, find_before=20):
        current_utc_time = datetime.now() - timedelta(seconds=find_before)
        date_format = "%a, %d %b %Y %H:%M:%S %z"
        search_criteria = ""

        if search_in_all_folders:
            search_criteria += " ALL"
        if from_email:
            search_criteria += ' FROM "{}"'.format(from_email)
        if to_email:
            search_criteria += ' TO "{}"'.format(to_email)
        if is_new_emails:
            search_criteria += " UNSEEN"
        # Remove white-space
        search_criteria = search_criteria.strip()

        def get_emails_list() -> list:
            LOGGER.info("Retrieving emails...")
            email_messages = self.fetch_emails(message_ids=self.get_message_ids(search_criteria),
                                               current_utc_time=current_utc_time, date_format=date_format)
            assert email_messages, "Not found at least one email message that matches to following filters '{}' and" \
                                   " since '{}'".format(search_criteria, current_utc_time)
            return email_messages

        return get_emails_list()

    def logout(self):
        LOGGER.info("Closing the GMAIL connection")
        # noinspection PyBroadException
        try:
            self.client.logout()
        except IMAP4.abort:
            LOGGER.warning("The GMAIL connection was closed")


if __name__ == '__main__':
    gmail_client = GmailClient(email_addr="testerikod@gmail.com", password="86a5701d-47f2-4b43-be55-0e6b11967a34")
    LOGGER.info("Getting messages...")
    messages = gmail_client.get_messages(to_email="testerikod@gmail.com", find_before=2000)
    LOGGER.info("Done.")
