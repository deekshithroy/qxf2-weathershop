# page_objects/weather_home_page.py
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
    @Wrapit._screenshot
    def get_temperature(self):  
        temp_text = self.get_text(self.temperature_field)
        result_flag = False
        temperature = None
        
        if isinstance(temp_text, bytes):
            temp_text = temp_text.decode("utf-8")

        match = re.search(r"(\d+)", temp_text or "")
        if match:
            temperature = int(match.group(1))
            result_flag = True
            
        self.conditional_write(result_flag, 
            positive=f"Temperature found: {temperature}°C",
            negative=f"Could not extract temperature from text: '{temp_text}'",
            level='debug')

        return temperature, result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def decide_product_type(self, temperature, temp_threshold):
        result_flag = True
        is_sunscreen = temperature > temp_threshold
        
        if is_sunscreen:
            self.conditional_write(result_flag,
                positive=f"{temperature}°C > {temp_threshold}°C → Sunscreens",
                negative="",
                level='debug')
            return ("sunscreen", self.buy_sunscreens_btn)
        else:
            self.conditional_write(result_flag,
                positive=f"{temperature}°C ≤ {temp_threshold}°C → Moisturizers",
                negative="",
                level='debug')
            return ("moisturizer", self.buy_moisturizers_btn)

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def navigate_to_product_page(self, button_locator):
        result_flag = self.click_element(button_locator)
        if result_flag:
            self.switch_page("product page")
            
        self.conditional_write(result_flag,
            positive="Successfully navigated to product page",
            negative="Failed to navigate to product page",
            level='debug')
        return result_flag