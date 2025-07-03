# page_objects/weather_home_page.py
from core_helpers.web_app_helper import Web_App_Helper
from page_objects.weather_home_object import Weather_Home_Object

class weather_home_page(Weather_Home_Object, Web_App_Helper):
    """Home page for Weather Shopper with temperature and decision logic"""

    def start(self):
        self.open("/")