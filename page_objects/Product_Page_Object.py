# page_objects/product_page.py
from core_helpers.web_app_helper import Web_App_Helper
from utils.Wrapit import Wrapit
import conf.locators_conf as locators
import re


class Product_Page_Object(Web_App_Helper):
    "Page object for the Product Page"

    product_container = locators.product_container
    product_price = locators.product_price
    product_name = locators.product_name
    cart_btn = locators.cart_btn

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def extract_products_from_page(self):
        "Extract all products from the page"
        product_containers = self.get_elements(self.product_container)
        self.write(f"Found {len(product_containers)} products", level='debug')

        products = []
        for container in product_containers:
        
            name = container.find_element(*self.product_name).text.strip()
            price_text = container.find_element(*self.product_price).text.strip()
            price = int(re.search(r"[\d,]+", price_text).group().replace(",", ""))
            add_btn = container.find_element("tag name", "button")
            products.append({'name': name, 'price': price, 'element': add_btn})
            
            continue
                
        return products

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def find_min_and_max(self, products):
        "Find cheapest and most expensive products"
        if not products:
            self.conditional_write(False,
                negative="No products found to compare",
                level='debug')
            return None, None
            
        cheapest = min(products, key=lambda x: x['price'])
        most_expensive = max(products, key=lambda x: x['price'])

        self.conditional_write(True,
            positive=f"Cheapest: {cheapest['name']} - ₹{cheapest['price']}",
            negative="",
            level='debug')

        self.conditional_write(True,
            positive=f"Most Expensive: {most_expensive['name']} - ₹{most_expensive['price']}",
            negative="",
            level='debug')

        return cheapest, most_expensive

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def add_selected_products(self, products_to_add):
        "Add selected products to cart"
        items_added = 0
        for item in products_to_add:
            try:
                item['element'].click()
                items_added += 1
                self.write(f"Added: {item['name']}", level='debug')
            except Exception as e:
                self.write(f"Failed to add {item['name']}: {e}", level='debug')
                
        return items_added

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def find_and_add_cheapest_and_most_expensive(self):
        "Find and add cheapest and most expensive products to cart"
        products = self.extract_products_from_page()
        
        if not products:
            self.conditional_write(False,
                negative="No products found on page",
                level='debug')
            return 0

        cheapest, most_expensive = self.find_min_and_max(products)
        
        if not cheapest or not most_expensive:
            return 0

        items_added = self.add_selected_products([cheapest, most_expensive])
        
        result_flag = items_added > 0
        self.conditional_write(result_flag,
            positive=f"Successfully added {items_added} items to cart",
            negative="Failed to add products to cart",
            level='debug')
            
        return items_added

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def navigate_to_cart(self):
        "Navigate to cart page"
        result_flag = self.click_element(self.cart_btn)
        if result_flag:
            self.switch_page("cart page")
            
        self.conditional_write(result_flag,
            positive="Navigated to cart",
            negative="Failed to navigate to cart",
            level='debug')
        return result_flag