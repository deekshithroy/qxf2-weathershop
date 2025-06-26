# --- weather_shopper_product_page.py ---
from selenium.webdriver.common.by import By
import conf.locators_conf as conf
import re
import time
from core_helpers.web_app_helper import Web_App_Helper
from conf import base_url_conf as url_conf

class WeatherShopperProductPage(Web_App_Helper):
    """Page object for Weather Shopper product selection page"""
    def __init__(self, base_url=None):
        if base_url is None:
            base_url = url_conf.ui_base_url
        super().__init__(base_url)

    def select_cheapest_and_expensive(self):
        try:
            product_elements = self.find_elements(By.XPATH, conf.PRODUCT_CONTAINER)
            products = []
            for element in product_elements:
                try:
                    name = element.find_element(By.XPATH, conf.PRODUCT_NAME).text.strip()
                    price_text = element.find_element(By.XPATH, conf.PRODUCT_PRICE).text.strip()
                    match = re.search(r'[\d,]+', price_text)
                    if not match:
                        continue
                    price = int(match.group().replace(',', ''))
                    button = element.find_element(By.TAG_NAME, "button")
                    products.append((name, price, button))
                except:
                    continue

            if not products:
                self.write("❌ No valid products found")
                return False

            cheapest = min(products, key=lambda x: x[1])
            most_expensive = max(products, key=lambda x: x[1])

            cheapest[2].click()
            time.sleep(conf.ELEMENT_INTERACTION_WAIT)
            self.write(f"✅ Added cheapest product: {cheapest[0]}")

            if cheapest[0] != most_expensive[0]:
                most_expensive[2].click()
                self.write(f"✅ Added most expensive product: {most_expensive[0]}")
                time.sleep(conf.ELEMENT_INTERACTION_WAIT)

            return True
        except Exception as e:
            self.write(f"❌ Failed to select products: {e}")
            return False
