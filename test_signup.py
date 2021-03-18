from pages.signup import SignUpPage


class TestSignUp:

    def test_signup(self, browser, test_user):
        page = SignUpPage(browser=browser)
        browser.goto_url(url=page.url)
        page.signup(user=test_user)
        browser.wait_till_current_url_changes(url=browser.base_url + "/user/complete", timeout=15)
