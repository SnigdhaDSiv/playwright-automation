
#!/usr/bin/env python
from src.utils.Logger import get_logger

logger = get_logger(__name__)

class CustomAssert:

    @staticmethod
    def contains(container, item, message=None):
        if item not in container:
            raise AssertionError(message or f"Expected '{container}' to contain '{item}'")
    
    @staticmethod
    def api_status(response, expected_code, message=None):
        if response != expected_code:
            raise AssertionError(f"Expected status {expected_code}, got {response}")
        
    @staticmethod
    def comapare_data(response, expected_code, message=None):
        print("comapare_data")
        #DataAccessCompare() implemented and used in test_user_api

