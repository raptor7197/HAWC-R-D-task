import pytest
from page_objects.login_page import LoginPage
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestLoginFunctionality:
    
    def test_page_load(self, login_page):
        page = LoginPage(login_page)
        assert "internshala.com" in page.get_current_url().lower()
        assert page.is_element_present(page.EMAIL_INPUT)
        assert page.is_element_present(page.PASSWORD_INPUT)
        assert page.is_element_present(page.LOGIN_BUTTON)
    
    def test_ui_elements_visibility(self, login_page):
        page = LoginPage(login_page)
        
        assert page.is_element_present(page.STUDENT_TAB)
        assert page.is_element_present(page.EMPLOYER_TAB)
        assert page.is_element_present(page.EMAIL_INPUT)
        assert page.is_element_present(page.PASSWORD_INPUT)
        assert page.is_element_present(page.LOGIN_BUTTON)
        assert page.is_element_present(page.GOOGLE_LOGIN_BUTTON)
        assert page.is_element_present(page.FORGOT_PASSWORD_LINK)
    
    def test_tab_switching(self, login_page):
        page = LoginPage(login_page)
        
        page.click_student_tab()
        time.sleep(1)
        
        page.click_employer_tab()
        time.sleep(1)
        
        assert page.is_element_present(page.EMAIL_INPUT)
        assert page.is_element_present(page.PASSWORD_INPUT)
    
    @pytest.mark.parametrize("email,password,expected_result", [
        ("", "password123", "validation_error"),  
        ("test@example.com", "", "validation_error"),  
        ("", "", "validation_error"),  
        ("invalid-email", "password123", "validation_error"),  
        ("test@example.com", "wrongpassword", "login_error"),  
    ])
    def test_login_validation(self, login_page, email, password, expected_result):
        page = LoginPage(login_page)
        
        page.click_student_tab()
        page.enter_email(email)
        page.enter_password(password)
        page.click_login_button()
        
        time.sleep(2)  
        
        if expected_result == "validation_error":
            assert "login" in page.get_current_url().lower()
        elif expected_result == "login_error":
            error_msg = page.get_error_message()
            assert error_msg is not None or "login" in page.get_current_url().lower()
    
    def test_forgot_password_link(self, login_page):
        page = LoginPage(login_page)
        
        current_url = page.get_current_url()
        page.click_forgot_password()
        time.sleep(2)
        
        new_url = page.get_current_url()
        assert new_url != current_url
    
    def test_google_login_button(self, login_page):
        page = LoginPage(login_page)
        
        try:
            page.click_google_login()
            assert True
        except Exception as e:
            pytest.fail(f"Google login button not clickable: {str(e)}")
    
    def test_sql_injection_prevention(self, login_page):
        page = LoginPage(login_page)
        
        sql_injection_payload = "' OR '1'='1"
        page.click_student_tab()
        page.enter_email(sql_injection_payload)
        page.enter_password("password")
        page.click_login_button()
        
        time.sleep(2)
        assert "login" in page.get_current_url().lower()
    
    def test_xss_prevention(self, login_page):
        page = LoginPage(login_page)
        
        xss_payload = "<script>alert('XSS')</script>"
        page.click_student_tab()
        page.enter_email(xss_payload)
        page.enter_password("password")
        page.click_login_button()
        
        time.sleep(2)
        assert "login" in page.get_current_url().lower()

class TestResponsiveDesign:
    
    @pytest.mark.parametrize("width,height", [
        (1920, 1080),  
        (1366, 768),   
        (768, 1024),   
        (375, 667),    
    ])
    def test_responsive_design(self, driver, width, height):
        driver.set_window_size(width, height)
        driver.get("https://internshala.com/login/user")
        
        page = LoginPage(driver)
        
        assert page.is_element_present(page.EMAIL_INPUT)
        assert page.is_element_present(page.PASSWORD_INPUT)
        assert page.is_element_present(page.LOGIN_BUTTON)
        
        email_element = driver.find_element(*page.EMAIL_INPUT)
        password_element = driver.find_element(*page.PASSWORD_INPUT)
        login_element = driver.find_element(*page.LOGIN_BUTTON)
        
        assert email_element.is_displayed()
        assert password_element.is_displayed()
        assert login_element.is_displayed()

class TestPerformance:
    
    def test_page_load_time(self, driver):
        import time
        
        start_time = time.time()
        driver.get("https://internshala.com/login/user")
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        
        load_time = time.time() - start_time
        
        assert load_time < 5, f"Page load time {load_time:.2f}s is more than 5 seconds"