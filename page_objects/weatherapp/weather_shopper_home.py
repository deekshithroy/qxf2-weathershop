# --- weather_shopper_home_page.py ---
from core_helpers.web_app_helper import Web_App_Helper
import conf.locators_conf as conf
from selenium.webdriver.common.by import By

class WeatherShopperHomePage(Web_App_Helper):
    """Page object for Weather Shopper home page"""
    def start(self):
        "Use this method to go to specific URL -- if needed"
        url = 'weathershopper.pythonanywhere.com'
        self.open(url)
    
    def get_temperature(self):
        try:
            temp_text = self.get_text(By.ID, conf.TEMPERATURE_ID)
            temperature = int(temp_text.replace("\u00b0C", "").strip())
            self.write(f"🌡️ Current temperature: {temperature}°C")
            return temperature
        except Exception as e:
            self.write(f"❌ Could not read temperature: {e}")
            return None

    def click_product_button(self, product_type):
        try:
            button_xpath = conf.BUY_SUNSCREENS_BTN if product_type == "sunscreen" else conf.BUY_MOISTURIZERS_BTN
            self.click_element(By.XPATH, button_xpath)
            return True
        except Exception as e:
            self.write(f"❌ Failed to click product button: {e}")
            return False
