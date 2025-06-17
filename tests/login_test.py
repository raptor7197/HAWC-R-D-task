from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    STUDENT_TAB = (By.XPATH, "//a[text()='Student']")
    EMPLOYER_TAB = (By.XPATH, "//a[text()='Employer / T&P']")
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Login']")
    GOOGLE_LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), 'Login with Google')]")
    FORGOT_PASSWORD_LINK = (By.XPATH, "//a[text()='Forgot password?']")
    STUDENT_REGISTER_LINK = (By.XPATH, "//a[text()='Student']")
    COMPANY_REGISTER_LINK = (By.XPATH, "//a[text()='Company']")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message")
    
    def click_student_tab(self):
        try:
            element = self.wait.until(EC.element_to_be_clickable(self.STUDENT_TAB))
            element.click()
        except TimeoutException:
            raise Exception("Student tab not found or not clickable")
    
    def click_employer_tab(self):
        try:
            element = self.wait.until(EC.element_to_be_clickable(self.EMPLOYER_TAB))
            element.click()
        except TimeoutException:
            raise Exception("Employer tab not found or not clickable")
    
    def enter_email(self, email):
        try:
            element = self.wait.until(EC.presence_of_element_located(self.EMAIL_INPUT))
            element.clear()
            element.send_keys(email)
        except TimeoutException:
            raise Exception("Email field not found")
    
    def enter_password(self, password):
        try:
            element = self.wait.until(EC.presence_of_element_located(self.PASSWORD_INPUT))
            element.clear()
            element.send_keys(password)
        except TimeoutException:
            raise Exception("Password field not found")
    
    def click_login_button(self):
        try:
            element = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
            element.click()
        except TimeoutException:
            raise Exception("Login button not found or not clickable")
    
    def click_google_login(self):
        try:
            element = self.wait.until(EC.element_to_be_clickable(self.GOOGLE_LOGIN_BUTTON))
            element.click()
        except TimeoutException:
            raise Exception("Google login button not found")
    
    def click_forgot_password(self):
        try:
            element = self.wait.until(EC.element_to_be_clickable(self.FORGOT_PASSWORD_LINK))
            element.click()
        except TimeoutException:
            raise Exception("Forgot password link not found")
    
    def get_error_message(self):
        try:
            element = self.wait.until(EC.presence_of_element_located(self.ERROR_MESSAGE))
            return element.text
        except TimeoutException:
            return None
    
    def is_element_present(self, locator):
        try:
            self.driver.find_element(*locator)
            return True
        except:
            return False
    
    def get_current_url(self):
        return self.driver.current_url
    
    def get_page_title(self):
        return self.driver.title