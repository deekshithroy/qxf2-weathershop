# --- weather_shopper_cart_page.py ---
from selenium.webdriver.common.by import By
import conf.locators_conf as conf
import time

class WeatherShopperCartPage():
    """Page object for Weather Shopper cart and checkout"""

    def checkout(self):
        try:
            self.click_element(By.XPATH, conf.CART_BTN)
            time.sleep(conf.PAGE_LOAD_WAIT)

            # Check if checkout is possible
            stripe_buttons = self.find_elements(By.CSS_SELECTOR, conf.STRIPE_BTN)
            if not stripe_buttons:
                self.write("❌ No items in cart")
                return False

            stripe_buttons[0].click()
            time.sleep(conf.PAGE_LOAD_WAIT)

            iframe = self.find_element(By.CSS_SELECTOR, conf.STRIPE_IFRAME)
            self.driver.switch_to.frame(iframe)

            self.set_text(By.ID, "email", conf.EMAIL)
            self.driver.execute_script(f"document.querySelector('input#card_number').value='{conf.CARD_NUMBER}'")
            self.driver.execute_script(f"document.querySelector('input#cc-exp').value='{conf.EXPIRY}'")
            self.driver.execute_script(f"document.querySelector('input#cc-csc').value='{conf.CVC}'")

            self.driver.find_element(By.XPATH, conf.STRIPE_PAY_BTN).click()
            self.driver.switch_to.default_content()

            success_text = self.get_text(By.XPATH, conf.SUCCESS_MSG)
            self.write(f"🎉 Payment successful: {success_text.strip()}")
            return True

        except Exception as e:
            self.write(f"❌ Checkout failed: {e}")
            return False
