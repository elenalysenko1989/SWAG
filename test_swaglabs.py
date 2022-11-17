from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import pytest
from time import sleep
from get_excel_data import login_form_parameters
import logging

##################################################################################
logging.basicConfig(filename='/Users/elenalysenko/Desktop/QA/PyTest/demo_swag/logs/info.log',
                    encoding='utf-8',
                    level=logging.INFO,
                    force=True,
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
def launch_swaglabs():
    logging.info('Launching the Swaglabs page')
    global driver
    driver = webdriver.Chrome()
    driver.get('https://www.saucedemo.com/')
    logging.info('Maximazing the window')
    driver.maximize_window()

def valid_login_swaglabs():
    logging.info('Logging in')
    driver.find_element(By.ID, 'user-name').send_keys('standard_user')
    driver.find_element(By.ID, 'password').send_keys('secret_sauce')
    driver.find_element(By.CSS_SELECTOR, '#login-button').click()

def capture_evidence():
    image_name = fr"/Users/elenalysenko/Desktop/QA/PyTest/demo_swag/evidence/image-{datetime.today().strftime('%m%d%y-%H%M%S')}.png"
    driver.save_screenshot(image_name)

def text_is_dysplaed(text):
    logging.info(f'Checking if [{text}] exists on the page')
    return text.lower() in driver.page_source.lower()


######################### TEST CASES ##################################################
def test_launch_login_page():
    launch_swaglabs()
    assert driver.title == 'Swag Labs'
    capture_evidence()
    driver.quit()

# login_form_parameters = [
#     ('locked_out_user', 'secret_sauce', 'Sorry, this user has been locked out.')
#     ('test', 'test', 'Username and password do not match any user in this service')
# ]
@pytest.mark.parametrize("username, password, checkpoint", login_form_parameters)
def test_login_with_invalid_cred(username, password, checkpoint):
    launch_swaglabs()
    if username != None: driver.find_element(By.ID, 'user-name').send_keys(username)
    if password != None: driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.CSS_SELECTOR, '#login-button').click()
    assert text_is_dysplaed(checkpoint)
    sleep(5)
    capture_evidence()
    driver.quit()
    
######################### SETUP AND TEARDOWN #########################################
@pytest.fixture()
def setup(request):
    launch_swaglabs()
    valid_login_swaglabs()

    def teardown():
        capture_evidence()   
        driver.quit()
    request.addfinalizer(teardown)
########################################################################################

def test_login_with_valid_cred(setup):
    assert text_is_dysplaed('products')


def test_view_product_details(setup):
    product_names = driver.find_elements(By.CLASS_NAME, 'inventory_item_name')
    product_names[0].click()
    assert text_is_dysplaed('back to products')
