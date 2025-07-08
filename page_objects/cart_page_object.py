# page_objects/cart_page_object.py
from core_helpers.web_app_helper import Web_App_Helper
from utils.Wrapit import Wrapit
import conf.locators_conf as locators


class Cart_Page_Object(Web_App_Helper):
    "Page object for the Cart Page"

    stripe_btn = locators.stripe_btn


    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def verify_items_in_cart(self):
        "Verify items are present in cart"
        try:
            checkout_elements = self.get_elements(self.stripe_btn)
            result_flag = len(checkout_elements) > 0
            self.conditional_write(result_flag,
                positive="Items verified in cart",
                negative="No items in cart",
                level='debug')
            return result_flag
        except Exception as e:
            self.conditional_write(False, 
                negative=f"Could not verify cart contents: {e}",
                level='debug')
            return False

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def start_payment_process(self):
        "Start the payment process by clicking Stripe button"
        result_flag = self.click_element(self.stripe_btn)
        self.conditional_write(result_flag,
            positive="Payment process started",
            negative="Failed to start payment",
            level='debug')
        return result_flag