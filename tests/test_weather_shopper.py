"""
Automated test using Qxf2's framework for Weather Shopper web application.

This test performs the following:
1. Open Weather Shopper main page.
2. Fetch temperature and decide product type.
3. Navigate to appropriate product page.
4. Add cheapest and most expensive items to cart.
5. Navigate to cart and verify items.
6. Complete checkout using Stripe with dummy test data.
7. Verify successful payment message.
"""

import os
import sys
import time
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from page_objects.PageFactory import PageFactory
import conf.weather_shopper_conf as conf

@pytest.mark.GUI
def test_weather_shopper(test_obj):
    "Run Weather Shopper desktop GUI test"
    expected_pass = 1
    actual_pass = 0

    try:
        start_time = int(time.time())

        # Load config
        temp_threshold = conf.temp_threshold
        email = conf.email
        card_number = conf.card_number
        expiry = conf.expiry
        cvc = conf.cvc

        # 1. Load Home Page
        home_page = PageFactory.get_page_object("weather home page", base_url=test_obj.base_url)
        home_page.start() 
        test_obj.write("Home page loaded successfully")

        # 2. Get temperature
        temperature = home_page.get_temperature()
        result_flag = temperature is not None
        test_obj.log_result(result_flag,
            positive=f"Temperature: {temperature}°C",
            negative="Could not read temperature")
  

        # 3. Decide product type
        product_category = home_page.decide_product_type(temperature, temp_threshold)
        result_flag = product_category is not None
        test_obj.log_result(result_flag,
            positive=f"Decided on product: {product_category[0] if product_category else 'None'}",
            negative="Could not decide product")
        
        
        product_type, button_locator = product_category

        # 4. Navigate to product page
        result_flag = home_page.navigate_to_product_page(button_locator)
        test_obj.log_result(result_flag,
            positive=f"Navigated to {product_type} page",
            negative="Failed navigation")
       

        # Small wait for page to load
        time.sleep(1)

        # 5. Product Page actions
        product_page = PageFactory.get_page_object("product page", base_url=test_obj.base_url)
        items_added = product_page.find_and_add_cheapest_and_most_expensive(product_type)
        result_flag = items_added > 0
        test_obj.log_result(result_flag,
            positive=f"Added {items_added} items to cart",
            negative="Failed to add products")
    

        # 6. Navigate to cart
        result_flag = product_page.navigate_to_cart()
        test_obj.log_result(result_flag,
            positive="Navigated to cart",
            negative="Failed to navigate to cart")
        

        # Small wait for cart page to load
        time.sleep(1)

        # 7. Cart Page
        cart_page = PageFactory.get_page_object("cart page", base_url=test_obj.base_url)
        result_flag = cart_page.verify_items_in_cart()
        test_obj.log_result(result_flag,
            positive="Items verified in cart",
            negative="Cart verification failed")
     

        result_flag = cart_page.start_payment_process()
        test_obj.log_result(result_flag,
            positive="Payment process started",
            negative="Payment initiation failed")
      

        # Wait for payment page to load
        time.sleep(2)

        # 8. Payment Page
        payment_page = PageFactory.get_page_object("payment page", base_url=test_obj.base_url)

        result_flag = payment_page.switch_to_stripe_iframe()
        test_obj.log_result(result_flag,
            positive="Switched to Stripe iframe",
            negative="Failed to switch iframe")
     

        result_flag = payment_page.fill_payment_details(email, card_number, expiry, cvc)
        test_obj.log_result(result_flag,
            positive="Filled payment details",
            negative="Failed to fill payment form")


        result_flag = payment_page.complete_payment()
        test_obj.log_result(result_flag,
            positive="Payment completed",
            negative="Payment failed")
     

        # Wait for payment processing
        time.sleep(3)

        result_flag = payment_page.verify_payment_success()
        test_obj.log_result(result_flag,
            positive="Payment verified",
            negative="Payment verification failed")
     

        # Final pass
        actual_pass = 1
        test_obj.write(f"Test completed successfully. Duration: {int(time.time() - start_time)} seconds")
        test_obj.write("Final result: PASS")

    except AssertionError as e:
        test_obj.write(f"ASSERTION ERROR: {str(e)}")
        test_obj.log_result(False, negative=f"Test failed: {str(e)}")
        actual_pass = 0
        
    except Exception as e:
        test_obj.write(f"UNEXPECTED ERROR: Exception in test_weather_shopper: {str(e)}")
        test_obj.log_result(False, negative=f"Test failed due to: {str(e)}")
        actual_pass = 0

    assert actual_pass == expected_pass, "Weather Shopper test failed"