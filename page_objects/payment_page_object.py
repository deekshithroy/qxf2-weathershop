# page_objects/payment_page.py
from core_helpers.web_app_helper import Web_App_Helper
from utils.Wrapit import Wrapit
import conf.locators_conf as locators


class Payment_Page_Object(Web_App_Helper):  # Fixed class name
    "Page object for the Payment Page with Stripe integration"

    stripe_iframe = locators.stripe_iframe
    email_field = locators.email_field
    card_number_field = locators.card_number_field
    expiry_field = locators.expiry_field
    cvc_field = locators.cvc_field
    stripe_pay_btn = locators.stripe_pay_btn
    success_msg = locators.success_msg

    def start(self):
        pass

    @Wrapit._exceptionHandler
    def switch_to_stripe_iframe(self):
        iframe_element = self.get_element(self.stripe_iframe)
        self.driver.switch_to.frame(iframe_element)
        self.conditional_write(True, positive="Switched to Stripe iframe", negative="Failed to switch to Stripe iframe")
        return True

    @Wrapit._exceptionHandler
    def fill_payment_details(self, email, card_number, expiry, cvc):
        self.set_text(self.email_field, email)
        self.driver.execute_script(f'document.querySelector("input#card_number").value = "{card_number}";')
        self.driver.execute_script(f'document.querySelector("input#cc-exp").value = "{expiry}";')
        self.driver.execute_script(f'document.querySelector("input#cc-csc").value = "{cvc}";')
        self.conditional_write(True, positive="Payment details filled", negative="Failed to fill payment details")
        return True

    @Wrapit._exceptionHandler
    def complete_payment(self):
        result_flag = self.click_element(self.stripe_pay_btn)
        if result_flag:
            self.driver.switch_to.default_content()
        self.conditional_write(result_flag, positive="Payment completed", negative="Payment failed")
        return result_flag

    @Wrapit._exceptionHandler
    def verify_payment_success(self):
        success_text = self.get_text(self.success_msg)
        result_flag = success_text is not None
        self.conditional_write(result_flag,
            positive="Payment successful",
            negative="Payment verification failed")
        return result_flag