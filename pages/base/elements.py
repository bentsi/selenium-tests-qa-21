import logging

from selenium.webdriver.common.keys import Keys


LOGGER = logging.getLogger()


class BaseElement:
    def __init__(self, driver, locator):
        self._driver = driver
        self.locator = locator  # (By.ID, "some-id")


class InputElement(BaseElement):

    def enter_text(self, text):
        LOGGER.debug(f"InputElement: entering text '{text}'")
        element = self._driver.find_element(*self.locator)
        element.click()
        element.send_keys(text)

    def get_text(self):
        element = self._driver.find_element(*self.locator)
        return element.get_attribute("value")


class CheckBoxElement(BaseElement):
    def __init__(self, driver, locator):
        super().__init__(driver=driver, locator=locator)
        self._checked = False

    def check(self):
        if self._checked:
            return True
        element = self._driver.find_element(*self.locator)
        element.click()
        self._checked = True

    def uncheck(self):
        if not self._checked:
            return True
        element = self._driver.find_element(*self.locator)
        element.click()
        self._checked = True

    @property
    def checked(self):
        """return whether the checkbox is checked or not"""
        # !!! this should be replaced by another logic that will get the real stat
        # from the DOM
        return self._checked


class ComboBox(BaseElement):
    def __init__(self, driver, locator, list_of_items):
        """TODO: get list of items from web app"""
        super().__init__(driver=driver, locator=locator)
        self.list_of_items = list_of_items

    def input_item(self, text):
        assert text in self.list_of_items
        element = self._driver.find_element(*self.locator)
        element.click()
        element.send_keys(text)
        element.send_keys(Keys.RETURN)

    def select_item(self):
        pass


class ButtonElement(BaseElement):
    def click(self):
        element = self._driver.find_element(*self.locator)
        element.click()