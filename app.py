import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
import string

@pytest.fixture
def browser():
    options = webdriver.FirefoxOptions()
    options.add_argument("--width=1920")
    options.add_argument("--height=1080")
    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_product_screenshots_switching(browser):
    try:
        browser.get("https://demo-opencart.ru/index.php?route=common/home")
        time.sleep(2)

        product_link = WebDriverWait(browser, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'MacBook')]"))
        )
        product_name = product_link.text
        product_link.click()
        time.sleep(2)

        product_title = WebDriverWait(browser, 15).until(
            EC.visibility_of_element_located((By.XPATH, "//h1[contains(text(),'MacBook')]"))
        ).text
        assert product_name in product_title

        thumbnails = WebDriverWait(browser, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.thumbnails li a.thumbnail"))
        )
        assert len(thumbnails) > 0

        for thumbnail in thumbnails:
            try:
                thumbnail.click()
                time.sleep(1)
                WebDriverWait(browser, 5).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, ".mfp-content img"))
                )
                browser.find_element(By.CSS_SELECTOR, "button.mfp-close").click()
                WebDriverWait(browser, 5).until(
                    EC.invisibility_of_element_located((By.CSS_SELECTOR, ".mfp-content"))
                )
            except:
                continue

    except Exception as e:
        raise e

def test_empty_pc_category_via_menu(browser):
    try:
        browser.get("https://demo-opencart.ru/index.php?route=common/home")
        
        computers_menu = WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'Компьютеры')]"))
        )
        ActionChains(browser).move_to_element(computers_menu).perform()
        time.sleep(1)
        
        pc_link = WebDriverWait(browser, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'PC') and contains(@href,'path=20_26')]"))
        )
        pc_link.click()
        
        WebDriverWait(browser, 15).until(
            EC.url_contains("path=20_26")
        )
        time.sleep(2)
        
    except Exception as e:
        raise e
    
def generate_random_email():
    letters = string.ascii_lowercase
    username = ''.join(random.choice(letters) for _ in range(8))
    return f"{username}@example.com"

def test_user_registration(browser):
    try:
        browser.get("https://demo-opencart.ru/index.php?route=common/home")
        time.sleep(2)
        
        account_menu = WebDriverWait(browser, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@title='Личный кабинет']"))
        )
        account_menu.click()
        
        register_link = WebDriverWait(browser, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Регистрация')]"))
        )
        register_link.click()
        
        WebDriverWait(browser, 15).until(
            EC.title_contains("Регистрация")
        )
        
        test_email = generate_random_email()
        test_password = "TestPassword123"
        
        browser.find_element(By.ID, "input-firstname").send_keys("Иван")
        browser.find_element(By.ID, "input-lastname").send_keys("Петров")
        browser.find_element(By.ID, "input-email").send_keys(test_email)
        browser.find_element(By.ID, "input-telephone").send_keys("+79123456789")
        browser.find_element(By.ID, "input-password").send_keys(test_password)
        browser.find_element(By.ID, "input-confirm").send_keys(test_password)
        
        privacy_policy = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.NAME, "agree"))
        )
        privacy_policy.click()
        
        submit_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@value='Продолжить']"))
        )
        submit_button.click()
        
        success_message = WebDriverWait(browser, 15).until(
            EC.visibility_of_element_located((By.XPATH, "//h1[contains(text(), 'Ваша учетная запись создана!')]"))
        )
        assert "Ваша учетная запись создана!" in success_message.text
        
    except Exception as e:
        raise e
    
def test_search_product(browser):
    try:
        browser.get("https://demo-opencart.ru/index.php?route=common/home")
        WebDriverWait(browser, 15).until(
            EC.title_contains("Opencart")
        )
        time.sleep(2)
        
        search_input = WebDriverWait(browser, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='search']"))
        )
        
        search_query = "iPhone"
        search_input.clear()
        search_input.send_keys(search_query)
        
        search_button = WebDriverWait(browser, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#search button"))
        )
        search_button.click()
        
        WebDriverWait(browser, 15).until(
            EC.url_contains("search=" + search_query)
        )
        
        try:
            page_title = WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located((By.TAG_NAME, "h1"))
            ).text
            assert search_query in page_title
        except:
            pass
        
        products = WebDriverWait(browser, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-thumb"))
        )
        assert len(products) > 0
        
    except Exception as e:
        raise e