# page_objects/cart_page.py
from core_helpers.web_app_helper import Web_App_Helper
from utils.Wrapit import Wrapit
import conf.locators_conf as locators


class Cart_Page_Object(Web_App_Helper):
    "Page object for the Cart Page"

    stripe_btn = locators.stripe_btn

    def start(self):
        pass

    @Wrapit._exceptionHandler
    def verify_items_in_cart(self):
        try:
            checkout_elements = self.get_elements(self.stripe_btn)
            result_flag = len(checkout_elements) > 0
            self.conditional_write(result_flag,
                positive="Items verified in cart",
                negative="No items in cart")
            return result_flag
        except Exception as e:
            self.conditional_write(False, negative=f"Could not verify cart contents: {e}")
            return False

    @Wrapit._exceptionHandler
    def start_payment_process(self):
        result_flag = self.click_element(self.stripe_btn)
        self.conditional_write(result_flag,
            positive="Payment process started",
            negative="Failed to start payment")
        return result_flag
