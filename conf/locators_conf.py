#Common locator file for all locators
#Locators are ordered alphabetically

############################################
#Selectors we can use
#ID
#NAME
#css selector
#CLASS_NAME
#LINK_TEXT
#PARTIAL_LINK_TEXT
#XPATH
###########################################

BASE_URL = "https://weathershopper.pythonanywhere.com/"
# Temperature threshold
TEMP_THRESHOLD = 30

# Wait times
IMPLICIT_WAIT = 10
PAGE_LOAD_WAIT = 3
ELEMENT_INTERACTION_WAIT = 1
CLEANUP_WAIT = 2

# Navigation buttons
BUY_SUNSCREENS_BTN = "//button[text()='Buy sunscreens']"
BUY_MOISTURIZERS_BTN = "//button[text()='Buy moisturizers']"
CART_BTN = "//button[contains(text(),'Cart')]"

# Product elements
PRODUCT_CONTAINER = "//p[contains(text(),'Price')]/.."
PRODUCT_PRICE = "./p[contains(text(),'Price')]"
PRODUCT_NAME = "./p[1]"

# Checkout elements
STRIPE_BTN = "button.stripe-button-el"
STRIPE_IFRAME = "iframe[name='stripe_checkout_app']"
STRIPE_PAY_BTN = "//span[contains(text(),'Pay INR')]"
SUCCESS_MSG = "//*[contains(text(),'success')]"

# Temperature element
TEMPERATURE_ID = "temperature"

# Stripe dummy data
EMAIL = "dheekshi@gmail.com"
CARD_NUMBER = "4242 4242 4242 4242"
EXPIRY = "12/25"
CVC = "123"
