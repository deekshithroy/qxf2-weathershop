# page_objects/payment_page.py
from core_helpers.web_app_helper import Web_App_Helper
from page_objects.payment_page_object import Payment_Page_Object  # Fixed import

class Payment_Page(Payment_Page_Object, Web_App_Helper):  # Fixed class name
    """Page for handling Stripe payment flow"""
    def start(self):
        pass  # reached after clicking payment button