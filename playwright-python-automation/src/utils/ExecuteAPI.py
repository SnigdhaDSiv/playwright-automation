
import json
from playwright.sync_api import sync_playwright
from resources.endpoints import endpoints

from src.utils.Logger import get_logger

logger = get_logger(__name__)


class ExecuteAPI:

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.playwright = sync_playwright().start()
        self.request_context = self.playwright.request.new_context(base_url=base_url)

    def close(self):
        """Close Playwright and the request context."""
        self.request_context.dispose()
        self.playwright.stop()

    def execute_api(self, url, apiname, token_json, payload, headers):

        '''with sync_playwright() as p:
            request_context = p.request.new_context(base_url=url)'''

        action = endpoints.get(apiname).get("action")
        endpoint = url+endpoints.get(apiname).get("endpoint")

        if headers is None:
            headers = {}
        if data is not None:
            # If JSON, set Content-Type and convert
            headers.setdefault("Content-Type", "application/json")
            data = json.dumps(data)
            logger.log(self.token)
            logger.log("Starting application..." + url)
            querystring = {'access_token': '{}'.format(self.token)}
            logger.log(querystring)
            logger.log(payload)

        # Make the request dynamically based on method

        method = action.upper()
        if method == "GET":
            response = self.request_context.get(endpoint, headers=headers)
        elif method == "POST":
            response = self.request_context.post(endpoint, headers=headers, data=data)
        elif method == "PUT":
            response = self.request_context.put(endpoint, headers=headers, data=data)
        elif method == "DELETE":
            response = self.request_context.delete(endpoint, headers=headers)
        else:
            raise ValueError(f"Unsupported  method: {method}")

        logger.log("Status:", response.status)
        logger.log("Response:", response.json())

        return response.status, response.json()
    
    def assert_status(self,response, expected, testinfo):
        message = f" Expected {expected}, got response for {testinfo}"
        assert response == expected, message
    
        
