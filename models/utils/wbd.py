import os
from selenium.webdriver.edge.service import Service
from selenium import webdriver


class WebDriverManager(object):

    _driver = None

    def __init__(self):
        print(os.getcwd())
        self.exec_path = f"{os.getcwd()}/models/utils/msedgedriver"

    def get_driver(self):

        if self._driver is None:
            # exec_path = os.getcwd() + "/msedgedriver"
            svc = Service(executable_path=self.exec_path)
            options = webdriver.EdgeOptions()
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920, 1080")
            self._driver = webdriver.Edge(
                service=svc,
                options=options
            )

        return self._driver

    def close_driver(self):

        if self._driver:
            self._driver.quit()
            self._driver = None


class Singleton:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if hasattr(self, 'initialized'):
            return

        self.value = WebDriverManager().get_driver()
        self.initialized = True

    def get_value(self):
        return self.value
