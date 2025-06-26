# --- weather_shopper_home_page.py ---
import re
from core_helpers.web_app_helper import Web_App_Helper
from conf import base_url_conf as url_conf
import conf.locators_conf as conf
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WeatherShopperHomePage(Web_App_Helper):
    """Page object for Weather Shopper home page"""
    def __init__(self, base_url=None):
        if base_url is None:
            base_url = url_conf.ui_base_url
        super().__init__(base_url)

    def start(self):
        "Navigate to the homepage using the correct URL"
        self.driver.get(self.base_url)

    def get_temperature(self):
        try:
            # Wait until the temperature element's text is not empty
            WebDriverWait(self.driver, 10).until(
                lambda d: d.find_element(By.ID, conf.TEMPERATURE_ID).text.strip() != ""
            )
            temp_text = self.driver.find_element(By.ID, conf.TEMPERATURE_ID).text
            if not temp_text:
                self.write("❌ Could not find temperature element or text.")
                return None
            temperature = int(re.sub(r"[^\d]", "", temp_text))
            self.write(f"🌡️ Current temperature: {temperature}°C")
            return temperature
        except Exception as e:
            self.write(f"❌ Could not read temperature: {e}")
            self.write(self.driver.page_source)  # For debugging
            return None

    def click_product_button(self, product_type):
        try:
            if product_type.lower() == "sunscreen":
                button_xpath = conf.BUY_SUNSCREENS_BTN
            elif product_type.lower() == "moisturizer":
                button_xpath = conf.BUY_MOISTURIZERS_BTN
            else:
                self.write(f"❌ Invalid product type: {product_type}")
                return False

            self.click_element((By.XPATH, button_xpath))
            # Wait for the product page to load by checking for the product container
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, conf.PRODUCT_CONTAINER))
            )
            return True
        except Exception as e:
            self.write(f"❌ Failed to click product button: {e}")
            return False
