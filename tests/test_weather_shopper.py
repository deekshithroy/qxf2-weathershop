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

    try:
        expected_pass = 0
        actual_pass = -1
        start_time = int(time.time())
        
        # Load config
        temp_threshold = conf.temp_threshold
        email = conf.email
        card_number = conf.card_number
        expiry = conf.expiry
        cvc = conf.cvc
        zip_code = conf.zip_code

        # Step 1: Load Home Page
        test_obj = PageFactory.get_page_object("weather home page", base_url=test_obj.base_url)

        # Step 2: Get temperature
        temperature, result_flag = test_obj.get_temperature()
        test_obj.log_result(result_flag,
            positive=f"Temperature: {temperature}°C",
            negative="Could not read temperature")

        # Step 3: Decide product type
        product_category = test_obj.decide_product_type(temperature, temp_threshold)
        result_flag = product_category is not None
        test_obj.log_result(result_flag,
            positive=f"Decided on product: {product_category[0] if product_category else 'None'}",
            negative="Could not decide product")
        
        product_type, button_locator = product_category

        # Step 4: Navigate to product page
        result_flag = test_obj.navigate_to_product_page(button_locator)
        test_obj.log_result(result_flag,
            positive=f"Navigated to {product_type} page",
            negative="Failed navigation")

        # Step 5: Product Page actions
        if result_flag:
            test_obj = PageFactory.get_page_object("product page", base_url=test_obj.base_url)
            items_added = test_obj.find_and_add_cheapest_and_most_expensive()
            result_flag &= items_added > 0
            test_obj.log_result(result_flag,
                positive=f"Added {items_added} items to cart",
                negative="Failed to add products")

        # Step 6: Navigate to cart
        result_flag = test_obj.navigate_to_cart()
        test_obj.log_result(result_flag,
            positive="Navigated to cart",
            negative="Failed to navigate to cart")

        # Step 7: Cart Page
        if result_flag:
            test_obj = PageFactory.get_page_object("cart page", base_url=test_obj.base_url)
            result_flag = test_obj.verify_items_in_cart()
            test_obj.log_result(result_flag,
                positive="Items verified in cart",
                negative="Cart verification failed")

            result_flag = test_obj.start_payment_process()
            test_obj.log_result(result_flag,
                positive="Payment process started",
                negative="Payment initiation failed")

        # Step 8: Payment Page
        if result_flag:
            test_obj = PageFactory.get_page_object("payment page", base_url=test_obj.base_url)

            result_flag = test_obj.switch_to_stripe_iframe()  # switch only once
            test_obj.log_result(result_flag,
                positive="Switched to Stripe iframe",
                negative="Failed to switch to Stripe iframe")

        if result_flag:
            result_flag = test_obj.process_payment(email, card_number, expiry, cvc, zip_code)
            test_obj.log_result(result_flag,
                positive="Stripe payment flow succeeded",
                negative="Stripe payment flow failed")

        # Final log and result
        test_obj.write(f'Script duration: {int(time.time() - start_time)} seconds\n')
        test_obj.write_test_summary()
        expected_pass = test_obj.result_counter
        actual_pass = test_obj.pass_counter

    except Exception as e:
        print(f"Exception during test: {__file__}")
        print(f"Python says: {str(e)}")

    assert expected_pass == actual_pass, f"Test failed: {__file__}"