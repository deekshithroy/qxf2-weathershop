# --- test_weather_shop.py ---
"""
Test case for Weather Shopper using Qxf2-style framework
"""
import os, sys, time
import pytest
from page_objects.PageFactory import PageFactory
import conf.locators_conf as conf

@pytest.mark.GUI
def test_weather_shop(test_obj):
    "Run end-to-end Weather Shopper test"
    try:
        expected_pass = 0
        actual_pass = -1

        start_time = int(time.time())

        # 1. Get home page and read temperature
        home_page = PageFactory.get_page_object("weathershopper home page")
        home_page.start()
        temperature = home_page.get_temperature()
        test_obj.log_result(temperature is not None, "Temperature fetched", "Failed to fetch temperature")
        if temperature is None:
            expected_pass = test_obj.result_counter
            actual_pass = test_obj.pass_counter
            assert expected_pass == actual_pass
            return

        # 2. Navigate to products page
        product_type = "sunscreen" if temperature > conf.TEMP_THRESHOLD else "moisturizer"
        result_flag = home_page.click_product_button(product_type)
        test_obj.log_result(result_flag, f"Navigated to {product_type} page", f"Failed to navigate to {product_type} page")

        # 3. Select products
        product_page = PageFactory.get_page_object("weathershopper products page")
        result_flag = product_page.select_cheapest_and_expensive()
        test_obj.log_result(result_flag, "Selected products", "Failed to select products")

        # 4. Go to cart and checkout
        cart_page = PageFactory.get_page_object("weathershopper cart page")
        result_flag = cart_page.checkout()
        test_obj.log_result(result_flag, "Checkout completed", "Checkout failed", level="critical")

        # Final test status
        expected_pass = test_obj.result_counter
        actual_pass = test_obj.pass_counter

    except Exception as e:
        print(f"Test failed due to exception: {e}")

    assert expected_pass == actual_pass
