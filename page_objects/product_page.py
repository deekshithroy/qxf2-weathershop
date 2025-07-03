# page_objects/product_page.py
from core_helpers.web_app_helper import Web_App_Helper
from page_objects.Product_Page_Object import Product_Page_Object

class Product_Page(Product_Page_Object, Web_App_Helper):
    """Page for sunscreen/moisturizer products"""
    def start(self):
        pass  # navigated from home page