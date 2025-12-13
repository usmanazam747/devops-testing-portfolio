import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os

@pytest.fixture
def driver():
    """Setup Chrome WebDriver"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    
    # For remote Selenium Grid
    selenium_url = os.getenv('SELENIUM_URL', 'http://localhost:4444/wd/hub')
    
    try:
        driver = webdriver.Remote(
            command_executor=selenium_url,
            options=chrome_options
        )
    except:
        # Fallback to local Chrome
        driver = webdriver.Chrome(options=chrome_options)
    
    driver.implicitly_wait(10)
    yield driver
    
    # Take screenshot on failure
    if hasattr(driver, 'save_screenshot'):
        screenshot_dir = 'screenshots'
        os.makedirs(screenshot_dir, exist_ok=True)
        driver.save_screenshot(f'{screenshot_dir}/test_{int(time.time())}.png')
    
    driver.quit()

class TestUserRegistrationE2E:
    """End-to-end tests for user registration flow"""
    
    def test_user_can_register(self, driver):
        """Test complete user registration flow"""
        base_url = os.getenv('BASE_URL', 'http://localhost:3000')
        driver.get(f'{base_url}/register')
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        
        # Fill registration form
        driver.find_element(By.ID, "username").send_keys("e2euser")
        driver.find_element(By.ID, "email").send_keys("e2e@example.com")
        driver.find_element(By.ID, "password").send_keys("E2EPass123!")
        driver.find_element(By.ID, "first_name").send_keys("E2E")
        driver.find_element(By.ID, "last_name").send_keys("User")
        
        # Submit form
        driver.find_element(By.ID, "register-button").click()
        
        # Wait for success message
        success_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "success-message"))
        )
        
        assert "successfully registered" in success_message.text.lower()
    
    def test_registration_validation_errors(self, driver):
        """Test form validation on registration page"""
        base_url = os.getenv('BASE_URL', 'http://localhost:3000')
        driver.get(f'{base_url}/register')
        
        # Try to submit empty form
        driver.find_element(By.ID, "register-button").click()
        
        # Check for validation errors
        errors = driver.find_elements(By.CLASS_NAME, "error-message")
        assert len(errors) > 0

class TestUserLoginE2E:
    """End-to-end tests for user login flow"""
    
    def test_user_can_login(self, driver):
        """Test complete login flow"""
        base_url = os.getenv('BASE_URL', 'http://localhost:3000')
        
        # First register a user
        driver.get(f'{base_url}/register')
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        
        driver.find_element(By.ID, "username").send_keys("loginuser")
        driver.find_element(By.ID, "email").send_keys("login@example.com")
        driver.find_element(By.ID, "password").send_keys("LoginPass123!")
        driver.find_element(By.ID, "register-button").click()
        
        time.sleep(2)
        
        # Now login
        driver.get(f'{base_url}/login')
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        
        driver.find_element(By.ID, "username").send_keys("loginuser")
        driver.find_element(By.ID, "password").send_keys("LoginPass123!")
        driver.find_element(By.ID, "login-button").click()
        
        # Wait for dashboard or profile page
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "user-dashboard"))
        )
        
        # Verify user is logged in
        assert "dashboard" in driver.current_url.lower()
    
    def test_login_with_invalid_credentials(self, driver):
        """Test login with wrong credentials"""
        base_url = os.getenv('BASE_URL', 'http://localhost:3000')
        driver.get(f'{base_url}/login')
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        
        driver.find_element(By.ID, "username").send_keys("wronguser")
        driver.find_element(By.ID, "password").send_keys("WrongPass123!")
        driver.find_element(By.ID, "login-button").click()
        
        # Check for error message
        error = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "error-message"))
        )
        
        assert "invalid" in error.text.lower() or "credentials" in error.text.lower()

class TestProductBrowsingE2E:
    """End-to-end tests for product browsing"""
    
    def test_user_can_browse_products(self, driver):
        """Test browsing product catalog"""
        base_url = os.getenv('BASE_URL', 'http://localhost:3000')
        driver.get(f'{base_url}/products')
        
        # Wait for products to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "product-card"))
        )
        
        # Check that products are displayed
        products = driver.find_elements(By.CLASS_NAME, "product-card")
        assert len(products) > 0
    
    def test_user_can_view_product_details(self, driver):
        """Test viewing product details"""
        base_url = os.getenv('BASE_URL', 'http://localhost:3000')
        driver.get(f'{base_url}/products')
        
        # Wait for products and click first one
        product = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "product-card"))
        )
        product.click()
        
        # Verify we're on product detail page
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "product-detail"))
        )
        
        assert "/product/" in driver.current_url

class TestCheckoutFlowE2E:
    """End-to-end tests for complete checkout flow"""
    
    def test_complete_purchase_flow(self, driver):
        """Test complete user journey from browse to checkout"""
        base_url = os.getenv('BASE_URL', 'http://localhost:3000')
        
        # 1. Login
        driver.get(f'{base_url}/login')
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        driver.find_element(By.ID, "username").send_keys("testbuyer")
        driver.find_element(By.ID, "password").send_keys("BuyerPass123!")
        driver.find_element(By.ID, "login-button").click()
        
        time.sleep(2)
        
        # 2. Browse products
        driver.get(f'{base_url}/products')
        product = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "product-card"))
        )
        product.click()
        
        # 3. Add to cart
        add_to_cart_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "add-to-cart"))
        )
        add_to_cart_btn.click()
        
        # 4. Go to cart
        driver.find_element(By.ID, "cart-icon").click()
        
        # 5. Checkout
        checkout_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "checkout-button"))
        )
        checkout_btn.click()
        
        # 6. Verify order confirmation
        confirmation = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "order-confirmation"))
        )
        
        assert "thank you" in confirmation.text.lower() or "order placed" in confirmation.text.lower()

# Pytest configuration
if __name__ == '__main__':
    pytest.main(['-v', '--html=selenium-report.html', '--self-contained-html'])
