import logging
from basetest import User
from pages.base.elements import InputElement, CheckBoxElement, ButtonElement, ComboBox
from pages.signup.locators import first_name_locator, last_name_locator, email_locator, password_locator, \
    company_locator, phone_locator, country_locator, agreement_checkbox_locator, signup_button_locator


LOGGER = logging.getLogger(__name__)


class SignUpPage:

    def __init__(self, browser):
        self.path = "/user/signup"
        self.url = browser.base_url + self.path
        self.first_name = InputElement(driver=browser.driver, locator=first_name_locator)
        self.last_name = InputElement(driver=browser.driver, locator=last_name_locator)
        self.email = InputElement(driver=browser.driver, locator=email_locator)
        self.password = InputElement(driver=browser.driver, locator=password_locator)
        self.company = InputElement(driver=browser.driver, locator=company_locator)
        self.country = ComboBox(driver=browser.driver, locator=country_locator,
                                list_of_items=("Angola", "Israel", "Russia"))
        self.phone = InputElement(driver=browser.driver, locator=phone_locator)
        self.agreement_check_box = CheckBoxElement(driver=browser.driver, locator=agreement_checkbox_locator)
        self.signup_button = ButtonElement(driver=browser.driver, locator=signup_button_locator)

    def signup(self, user: User):
        LOGGER.info("Signing up..")
        self.first_name.enter_text(user.first_name)
        self.last_name.enter_text(user.last_name)
        self.email.enter_text(user.email)
        self.password.enter_text(user.password)
        self.company.enter_text(user.company)
        self.country.input_item(user.country)
        self.phone.enter_text(user.phone)
        self.agreement_check_box.check()
        self.signup_button.click()
        LOGGER.info("Signup complete.")


