from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from .record_generator import RecordGenerator


class BasicTestClass():

    def setup_method(self, method):
        op = webdriver.FirefoxOptions()
        op.add_argument('--headless')
        op.add_argument("--no-sandbox")
        try:
            self.driver = webdriver.Firefox(
                options=op)
        except Exception as e:
            print(f"Error setting up WebDriver: {e}")
            raise
        self.driver = webdriver.Firefox(options=op)
        self.driver.get("http://localhost:8080/")
        self.wait = WebDriverWait(self.driver, 2)
        self.vars = {}
        self.sat3_sample_code = ""

    def teardown_method(self, method):
        self.delete_test_record()
        self.logout()
        self.driver.close()
        self.driver.quit()

    def delete_test_record(self):
        # self.driver.save_screenshot("before_not_displaysesed.png")
        self.driver.implicitly_wait(0.2)
        self.wait.until(
            lambda _: self.driver.find_element(
                By.ID,
                "all-samples-nav").is_displayed()
        )
        # self.driver.save_screenshot("not_displaysesed.png")
        self.driver.find_element(By.ID, "all-samples-nav").click()
        self.driver.find_element(By.ID,
                                 f"Delete {self.sat3_sample_code}").click()

    def login(self, user, password):
        self.driver.implicitly_wait(0.2)
        self.driver.set_window_size(50000, 30000)
        self.driver.find_element(By.ID, "id_user_name").send_keys(user)
        self.driver.find_element(By.ID, "id_password").send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
        self.driver.find_element(By.ID, "sample-tracking-nav").click()

    def logout(self):
        dropdown = self.driver.find_element(
            by=By.ID, value="navbarScrollingDropdown")
        dropdown.click()
        dropdown_menu = self.driver.find_element(
            by=By.ID, value="dropdown-login")
        logout = dropdown_menu.find_elements(
            by=By.CLASS_NAME, value="dropdown-item")[1]
        logout.click()

    def submit_record(self):
        self.wait.until(
            lambda _: self.driver.find_element(By.ID,
                                               "modalButton").is_displayed())
        self.driver.find_element(By.ID, "modalButton").click()
        self.wait.until(
            lambda _: self.driver.find_element(
                By.CSS_SELECTOR,
                ".modal-footer > .btn-primary").is_displayed())
        self.driver.find_element(
            By.CSS_SELECTOR, ".modal-footer > .btn-primary").click()

    def check_submission(self):
        # self.driver.save_screenshot("screenie.png")
        message_container = self.driver.find_element(By.CLASS_NAME, "messages")
        message = message_container.find_element(By.TAG_NAME, "li")
        assert (message.text == "Submission successful!")

        for m in message_container.find_elements(By.TAG_NAME, "li"):
            print(m.text)

    def create_minimal_test_record(self):
        """
        Minimal record in the sense of having all recruiter fields filled out.
        Not only the required ones.
        """
        # self.driver.save_screenshot("screenie.png")
        recruiting_site = self.driver.find_element(
            By.ID, "id_recruiting_site")
        select_recruiting_site = Select(recruiting_site)
        select_recruiting_site.select_by_visible_text(
            RecordGenerator.random_site_choice())

        patient_identifier = RecordGenerator.random_patient_identifier()
        self.driver.find_element(
            By.ID, "id_patient_identifier").send_keys(patient_identifier)

        sex = self.driver.find_element(By.ID, "id_sex")
        sex_select = Select(sex)
        sex_select.select_by_value(RecordGenerator.random_sex_choice())

        self.driver.find_element(By.ID, "id_died").send_keys(
            RecordGenerator.random_date())
        self.driver.find_element(By.ID, "id_died").send_keys(Keys.ENTER)

        # SATURN3 Sample Code #
        # Entity
        sat3_code_entity = RecordGenerator.random_sample_code_entity_choice()
        saturn3_sample_code_0 = self.driver.find_element(
            By.ID, "id_saturn3_sample_code_0")
        select_saturn3_sample_code_0 = Select(saturn3_sample_code_0)
        select_saturn3_sample_code_0.select_by_value(sat3_code_entity)

        # saturn3_sample_code_1 is filled out automatically

        # samling time point
        sat3_code_sampling_time_point = \
            RecordGenerator.random_sample_code_number()
        self.driver.find_element(
            By.ID, "id_saturn3_sample_code_2").send_keys(
                sat3_code_sampling_time_point)

        # tissue type
        sat3_code_tissue_type = \
            RecordGenerator.random_sample_code_tissue_type()
        saturn3_sample_code_3 = self.driver.find_element(
            By.ID, "id_saturn3_sample_code_3")
        select_saturn3_sample_code_3 = Select(saturn3_sample_code_3)
        select_saturn3_sample_code_3.select_by_value(sat3_code_tissue_type)

        # tissue type - order number
        sat3_code_tissue_type_order_number = \
            RecordGenerator.random_sample_code_number()
        self.driver.find_element(
            By.ID, "id_saturn3_sample_code_4").send_keys(
                sat3_code_tissue_type_order_number)

        # storage format
        sat3_code_storage_format = RecordGenerator.random_storage_format()
        saturn3_sample_code_5 = self.driver.find_element(
            By.ID, "id_saturn3_sample_code_5")
        select_saturn3_sample_code_5 = Select(saturn3_sample_code_5)
        select_saturn3_sample_code_5.select_by_value(sat3_code_storage_format)

        # analyte type
        sat3_code_analyte_type = \
            RecordGenerator.random_sample_code_analyte_type()
        saturn3_sample_code_6 = self.driver.find_element(
            By.ID, "id_saturn3_sample_code_6")
        select_saturn3_sample_code_6 = Select(saturn3_sample_code_6)
        select_saturn3_sample_code_6.select_by_value(sat3_code_analyte_type)

        # analyte type - order number
        sat3_code_analyte_type_order_number = \
            RecordGenerator.random_sample_code_number()
        self.driver.find_element(
            By.ID, "id_saturn3_sample_code_7").send_keys(
                sat3_code_analyte_type_order_number)

        self.sat3_sample_code = \
            sat3_code_entity + \
            "-" + patient_identifier + \
            "-" + sat3_code_sampling_time_point + \
            "-" + sat3_code_tissue_type + sat3_code_tissue_type_order_number +\
            "-" + sat3_code_storage_format + \
            "-" + sat3_code_analyte_type + sat3_code_analyte_type_order_number

        # End of SATURN3 Sample Code section

        self.driver.find_element(
            By.ID,
            "id_note").send_keys(RecordGenerator.random_string_of_length(20))

        self.driver.find_element(
            By.ID, "id_sampling_date").send_keys(RecordGenerator.random_date())
        self.driver.find_element(
            By.ID, "id_sampling_date").send_keys(Keys.ENTER)

        tissue_type = self.driver.find_element(By.ID, "id_tissue_type")
        select_tissue_type = Select(tissue_type)
        select_tissue_type.select_by_value(
            RecordGenerator.random_tissue_type())

        type_of_intervention = self.driver.find_element(
            By.ID, "id_type_of_intervention")
        select_type_of_intervention = Select(type_of_intervention)
        select_type_of_intervention.select_by_value(
            RecordGenerator.random_intervention_type())

        localisation = self.driver.find_element(By.ID, "id_localisation")
        select_localisation = Select(localisation)
        select_localisation.select_by_value(
            RecordGenerator.random_localisation())

        corresponding_organoid = self.driver.find_element(
            By.ID, "id_corresponding_organoid")
        select_corresponding_organoid = Select(corresponding_organoid)
        select_corresponding_organoid.select_by_visible_text(
            RecordGenerator.random_corresponding_organoid_choice())

        grading = self.driver.find_element(By.ID, "id_grading")
        select_grading = Select(grading)
        select_grading.select_by_value(RecordGenerator.random_grading())
