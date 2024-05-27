from selenium import webdriver
from selenium.webdriver.common.by import By


class BasicTestClass():

    def setup_method(self, method):
        op = webdriver.FirefoxOptions()
        op.add_argument('-headless')
        self.driver = webdriver.Firefox(options=op)
        self.driver.get("http://0.0.0.0:8080/")
        self.vars = {}

    def login(self, user, password):
        self.driver.implicitly_wait(0.5)
        self.driver.set_window_size(50000, 30000)
        self.driver.find_element(By.ID, "id_user_name").send_keys(user)
        self.driver.find_element(By.ID, "id_password").send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()

    def logout(self):
        dropdown = self.driver.find_element(
            by=By.ID, value="navbarScrollingDropdown")
        dropdown.click()
        dropdown_menu = self.driver.find_element(
            by=By.ID, value="dropdown-login")
        logout = dropdown_menu.find_elements(
            by=By.CLASS_NAME, value="dropdown-item")[1]
        logout.click()