# page_objects/payment_page_object.py

from core_helpers.web_app_helper import Web_App_Helper
from utils.Wrapit import Wrapit
import conf.locators_conf as locators
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Payment_Page_Object(Web_App_Helper):
    "Page object for the Payment Page with Stripe integration"

    stripe_iframe = locators.stripe_iframe
    email_field = locators.email_field
    card_number_field = locators.card_number_field
    expiry_field = locators.expiry_field
    cvc_field = locators.cvc_field
    stripe_pay_btn = locators.stripe_pay_btn
    success_msg = locators.success_msg
    zip_code_field = locators.zip_code_field

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def switch_to_stripe_iframe(self):
        "Switch to Stripe iframe for payment form"
        iframe_element = self.get_element(self.stripe_iframe)
        if iframe_element:
            self.driver.switch_to.frame(iframe_element)
            result_flag = True
        else:
            result_flag = False

        self.conditional_write(result_flag,
            positive="Switched to Stripe iframe",
            negative="Failed to switch to Stripe iframe",
            level='debug')
        return result_flag
        
    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def fill_payment_details(self, email, card_number, expiry, cvc, zip_code):
        "Fill payment details in Stripe form using normal set_text"

        result_flag = self.set_text(self.email_field, email)
       
        for digit in card_number:
            result_flag &= self.set_text(self.card_number_field, digit, clear_flag=False)
    
        # Wait for card number to be processed
        for digit in expiry:
            result_flag &= self.set_text(self.expiry_field, digit, clear_flag=False)
      
        result_flag &= self.set_text(self.cvc_field, cvc)
        
        result_flag &= self.set_text(self.zip_code_field, zip_code)
        
        self.conditional_write(result_flag,
        positive="Successfully filled payment details",
        negative="Failed to fill payment details",
        level='debug')

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def complete_payment(self):
        "Complete payment by clicking pay button"
        result_flag = self.click_element(self.stripe_pay_btn)
        if result_flag:
            self.driver.switch_to.default_content()

        self.conditional_write(result_flag,
            positive="Payment completed",
            negative="Payment failed",
            level='debug')
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def verify_payment_success(self):
        "Verify payment success message"
        success_text = self.get_text(self.success_msg)
        result_flag = success_text is not None and len(success_text) > 0

        self.conditional_write(result_flag,
            positive="Payment successful",
            negative="Payment verification failed",
            level='debug')
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def process_payment(self, email, card_number, expiry, cvc, zip_code):
        "Complete Stripe payment steps - assumes already inside iframe"

        result_flag = self.fill_payment_details(email, card_number, expiry, cvc, zip_code)
        self.conditional_write(result_flag,
            positive="Filled payment details",
            negative="Failed to fill payment details")

        if result_flag:
            result_flag = self.complete_payment()
            self.conditional_write(result_flag,
                positive="Payment completed",
                negative="Payment failed")

        if result_flag:
            result_flag = self.verify_payment_success()
            self.conditional_write(result_flag,
                positive="Payment verified",
                negative="Payment verification failed")

        return result_flag