# page_objects/weather_home_page.py
import re
from core_helpers.web_app_helper import Web_App_Helper
from utils.Wrapit import Wrapit
import conf.locators_conf as locators


class Weather_Home_Object(Web_App_Helper):
    "Page object for the Weather Shopper Home Page"

    temperature_field = locators.temperature_field
    buy_sunscreens_btn = locators.buy_sunscreens_btn
    buy_moisturizers_btn = locators.buy_moisturizers_btn

    @Wrapit._exceptionHandler
    def get_temperature(self):
        temp_text = self.get_text(self.temperature_field)
        if isinstance(temp_text, bytes):
            temp_text = temp_text.decode("utf-8")
        match = re.search(r"(\d+)", temp_text or "")  # Fixed regex
        temperature = int(match.group(1)) if match else None
        self.write(f"Current temperature: {temperature}°C" if temperature else "Temperature not found")
        return temperature

    @Wrapit._exceptionHandler
    def decide_product_type(self, temperature, temp_threshold):
        if temperature is None:
            self.write("Temperature is None - cannot decide product type")
            return None
        if temperature > temp_threshold:
            self.write(f"{temperature}°C > {temp_threshold}°C → Sunscreens")
            return ("sunscreen", self.buy_sunscreens_btn)
        else:
            self.write(f"{temperature}°C ≤ {temp_threshold}°C → Moisturizers")
            return ("moisturizer", self.buy_moisturizers_btn)

    @Wrapit._exceptionHandler
    def navigate_to_product_page(self, button_locator):
        result_flag = self.click_element(button_locator)
        self.conditional_write(result_flag,
            positive="Successfully navigated to product page",
            negative="Failed to navigate to product page")
        return result_flag