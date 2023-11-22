import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as ec
from utils import WebDriverUtils

import time 
from datetime import datetime, timedelta
from faker import Faker

class RegistrationTest(unittest.TestCase):
    
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
            )
        self.driver.maximize_window()
        self.base_url = "https://practicesoftwaretesting.com"
        self.driver.get(self.base_url)
        self.wait = WebDriverWait(self.driver, 10)

    def generate_random_date_of_birth(self, fake):
        random_age = fake.random_int(min=18, max=65)
        
        birth_date = datetime.now() - timedelta(days=random_age * 365)
        
        formatted_birth_date = birth_date.strftime('%d.%m.%Y')
        
        return formatted_birth_date

    def login_page_is_displayed(self):
        element = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, "//div[@class='col-lg-6 auth-form']//h3"))
        )
        return element.is_displayed() and element.text == "Login"


    def test_user_registration(self):
        fake = Faker()
        WebDriverUtils(self.driver)\
            .click_by_css_selector(css_selector='a[data-test="nav-sign-in"]')\
            .click(xpath="//div[@class='col-lg-6 auth-form']//form//div[@class='input-group mb-3'][4]//p//a[1]")\
            .fill(xpath='//*[@id="first_name"]', value=fake.first_name())\
            .fill(xpath='//*[@id="last_name"]', value=fake.last_name())\
            .fill(xpath='//*[@id="dob"]', value=self.generate_random_date_of_birth(fake))\
            .fill(xpath='//*[@id="address"]', value=fake.address())\
            .fill(xpath='//*[@id="postcode"]', value=fake.postcode())\
            .fill(xpath='//*[@id="city"]',value=fake.city())\
            .fill(xpath='//*[@id="state"]', value=fake.state())\
            .select_option(xpath='//*[@id="country"]', index=42)\
            .fill(xpath='//*[@id="phone"]', value=''.join(char for char in fake.phone_number() if char.isdigit()))\
            .fill(xpath='//*[@id="email"]', value=fake.email())\
            .fill(xpath='//*[@id="password"]', value=fake.password())\
            .click(xpath='//div[@class="col-lg-8 auth-form"]//form//button[@class="btnSubmit mb-3"]')

        assert self.login_page_is_displayed(), "User is not on the login page after submission."

    def tearDown(self):
        time.sleep(10)
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
