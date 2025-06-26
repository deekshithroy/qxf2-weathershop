# --- weather_shopper_home_page.py ---
from core_helpers.web_app_helper import Web_App_Helper
from conf import base_url_conf as url_conf
import conf.locators_conf as conf
from selenium.webdriver.common.by import By
import re

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
            temp_text = self.get_text(By.ID, conf.TEMPERATURE_ID)
            if not isinstance(temp_text, str) or not temp_text:
                self.write("❌ Could not find temperature element or text.")
                return None
            temperature = int(re.sub(r"[^\d]", "", temp_text))
            self.write(f"🌡️ Current temperature: {temperature}°C")
            return temperature
        except Exception as e:
            self.write(f"❌ Could not read temperature: {e}")
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

            self.click_element(By.XPATH, button_xpath)
            return True
        except Exception as e:
            self.write(f"❌ Failed to click product button: {e}")
            return False
