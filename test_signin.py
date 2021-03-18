password = "EDfmJpVZ4@uFwSp!"

class TestSignIn:
    def test_title(self, browser):
        browser.goto_url("https://cloud.scylladb.com/user/signin")
        assert browser.title == "Scylla Cloud"

    def test_incorrect_credentials(self):
        pass