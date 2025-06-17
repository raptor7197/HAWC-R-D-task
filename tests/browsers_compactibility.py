import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from page_objects.login_page import LoginPage

class TestCrossBrowser:
    
    @pytest.mark.parametrize("browser", ["chrome", "firefox", "edge"])
    def test_login_page_cross_browser(self, browser):
        
        if browser == "chrome":
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service)
        elif browser == "firefox":
            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service)
        elif browser == "edge":
            service = EdgeService(EdgeChromiumDriverManager().install())
            driver = webdriver.Edge(service=service)
        
        try:
            driver.get("https://internshala.com/login/user")
            page = LoginPage(driver)
            assert page.is_element_present(page.EMAIL_INPUT)
            assert page.is_element_present(page.PASSWORD_INPUT)
            assert page.is_element_present(page.LOGIN_BUTTON)
            
            page.click_student_tab()
            page.click_employer_tab()
            
            page.enter_email("test@example.com")
            page.enter_password("testpassword")
            
        finally:
            driver.quit()