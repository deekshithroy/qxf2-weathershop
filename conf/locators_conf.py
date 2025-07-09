from selenium.webdriver.common.by import By

#Locators are ordered alphabetically


#Locators for the weather shopper home page object(weather_home_object.py)
temperature_field = (By.ID, "temperature")
buy_sunscreens_btn = (By.XPATH, "//button[text()='Buy sunscreens']")
buy_moisturizers_btn = (By.XPATH, "//button[text()='Buy moisturizers']")
#----

#Locators for the product page object(product_page_object.py)
product_container = (By.XPATH, "//p[contains(text(),'Price')]/..")
product_price = (By.XPATH, "./p[contains(text(),'Price')]")
product_name = (By.XPATH, "./p[1]")
cart_btn = (By.XPATH, "//button[contains(text(),'Cart')]")
#----

#Locators for the cart page object(cart_page_object.py)
stripe_btn = (By.CSS_SELECTOR, "button.stripe-button-el")
#----

#Locators for the payment object(payment_object.py)
stripe_iframe = (By.CSS_SELECTOR, "iframe[name='stripe_checkout_app']")
email_field = (By.ID, "email")
card_number_field = (By.ID, "card_number")
expiry_field = (By.ID, "cc-exp")
cvc_field = (By.ID, "cc-csc")
zip_code_field = (By.ID, "billing-zip")
stripe_pay_btn = (By.XPATH, "//span[contains(text(),'Pay INR')]")
success_msg = (By.XPATH, "//*[contains(text(),'success')]")