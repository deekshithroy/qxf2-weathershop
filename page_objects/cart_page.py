# page_objects/cart_page.py
from core_helpers.web_app_helper import Web_App_Helper
from page_objects.cart_page_object import Cart_Page_Object

class Cart_Page(Cart_Page_Object, Web_App_Helper):
    """Page for viewing and verifying cart"""
    def start(self):
        pass  # navigated from product page