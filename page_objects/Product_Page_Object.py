# page_objects/product_page.py
from core_helpers.web_app_helper import Web_App_Helper
from utils.Wrapit import Wrapit
import conf.locators_conf as locators
import re


class Product_Page_Object(Web_App_Helper):  # Fixed class name
    "Page object for the Product Page"

    product_container = locators.product_container
    product_price = locators.product_price
    product_name = locators.product_name
    cart_btn = locators.cart_btn

    def start(self):
        pass  # navigated from home

    @Wrapit._exceptionHandler
    def find_and_add_cheapest_and_most_expensive(self, product_type):
        product_containers = self.get_elements(self.product_container)
        self.write(f"Found {len(product_containers)} products")
        products = []
        for container in product_containers:
            try:
                name = container.find_element(*self.product_name).text.strip()
                price_text = container.find_element(*self.product_price).text.strip()
                price = int(re.search(r"[\d,]+", price_text).group().replace(",", ""))
                add_btn = container.find_element("tag name", "button")
                products.append({'name': name, 'price': price, 'element': add_btn})
            except Exception:
                self.write("Skipped a product due to parsing error")

        if not products:
            self.write("No valid products found")
            return 0

        cheapest = min(products, key=lambda x: x['price'])
        most_expensive = max(products, key=lambda x: x['price'])
        self.write(f"Cheapest: {cheapest['name']} - ₹{cheapest['price']}")
        self.write(f"Most Expensive: {most_expensive['name']} - ₹{most_expensive['price']}")

        items_added = 0
        for item in [cheapest, most_expensive]:
            try:
                item['element'].click()
                items_added += 1
                self.write(f"Added: {item['name']}")
            except Exception:
                self.write(f"Failed to add: {item['name']}")

        return items_added

    @Wrapit._exceptionHandler
    def navigate_to_cart(self):
        result_flag = self.click_element(self.cart_btn)
        self.conditional_write(result_flag,
            positive="Navigated to cart",
            negative="Failed to navigate to cart")
        return result_flag