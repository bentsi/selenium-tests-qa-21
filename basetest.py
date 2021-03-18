import random
import string
from functools import cached_property


class User:
    def __init__(self, first_name, last_name, email, company, country, phone):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.company = company
        self.country = country
        self.phone = phone
        self._password = None

    @staticmethod
    def _generate_password(num_letters, num_special_chars, num_digits, shuffle=True):
        special_chars = random.sample(string.punctuation, num_special_chars)
        letters = random.sample(string.ascii_letters, num_letters)
        numbers = random.sample(string.digits, num_digits)
        password = letters + special_chars + numbers
        if shuffle:
            random.shuffle(password)
        return "".join(password)

    @cached_property
    def password(self):
        """ should contain:
            - 8 characters minimum
            - One special character
            - One letter
            - One number
        """
        self._password = self._generate_password(num_letters=5, num_special_chars=2, num_digits=1)
        return self._password