# --- weather_shopper_product_page.py ---
from selenium.webdriver.common.by import By
import conf.locators_conf as conf
from conf.locators_conf import ELEMENT_INTERACTION_WAIT
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
            product_containers = self.find_elements((By.XPATH, conf.PRODUCT_CONTAINER))
            self.write(f"🛒 Found {len(product_containers)} products")

            products = []
            for container in product_containers:
                try:
                    name_element = container.find_element(By.XPATH, conf.PRODUCT_NAME)
                    product_name = name_element.text.strip()

                    price_element = container.find_element(By.XPATH, conf.PRODUCT_PRICE)
                    price_text = price_element.text.strip()
                    price_match = re.search(r'[\d,]+', price_text)
                    
                    if not price_match:
                        self.write(f"⚠️ No price found in: {price_text}")
                        continue

                    price = int(price_match.group().replace(',', ''))

                    add_button = container.find_element(By.TAG_NAME, "button")
                    products.append((product_name, price, add_button))
                except Exception as inner_e:
                    self.write(f"⚠️ Couldn't process one product: {inner_e}")
                    continue

            if not products:
                self.write("❌ No valid products collected!")
                return False

            # Identify cheapest and most expensive
            cheapest_product = min(products, key=lambda x: x[1])
            most_expensive_product = max(products, key=lambda x: x[1])

            self.write(f"💰 Cheapest: {cheapest_product[0]} - ₹{cheapest_product[1]}")
            self.write(f"💎 Most expensive: {most_expensive_product[0]} - ₹{most_expensive_product[1]}")

            items_added = 0

            # Add cheapest product
            cheapest_product[2].click()
            items_added += 1
            self.write(f"✅ Added: {cheapest_product[0]}")
            time.sleep(ELEMENT_INTERACTION_WAIT)

            # Add most expensive product if different
            if cheapest_product[0] != most_expensive_product[0]:
                most_expensive_product[2].click()
                items_added += 1
                self.write(f"✅ Added: {most_expensive_product[0]}")
                time.sleep(ELEMENT_INTERACTION_WAIT)
            else:
                self.write("ℹ️ Cheapest and most expensive are the same product")

            return items_added > 0

        except Exception as e:
            self.write(f"❌ Failed to select products: {e}")
            return False

