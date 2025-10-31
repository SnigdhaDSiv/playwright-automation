from playwright.sync_api import Page, Locator
from src.page_objects.base_page import BasePage


class UsersPage(BasePage):

    def __init__(self, page: Page, urls):
        super().__init__(page, urls)
        self.current_page = page
        self.urls = urls
        self._selectors = self._Selectors()

    def goto_users_page(self,value:str = "user_registration.html"):
        print(f" ******baseurl => {self.urls} {self.urls['WEB_BASE_URL']}")
        baseurl =  self.urls["WEB_BASE_URL"]+'user_registration.html'
        #self.current_page.goto("http://localhost:8000/user_registration.html")
        self.current_page.goto(baseurl)

    def set_username(self, value: str):
        self.current_page.fill(self._selectors.USERNAME, value)

    def set_email(self, value: str):
        self.current_page.fill(self._selectors.EMAIL, value)
    
    def set_accounttype(self, value: str):
        self.current_page.select_option(self._selectors.ACCOUNT_TYPE, value)

    def click_user_registration(self):
        self.current_page.click(self._selectors.USER_REG_BUTTON)

    def user_reg_to_application(self, username: str, email: str, accounttype: str):
        self.set_username(username)
        self.set_email(email)
        self.set_accounttype(accounttype)
        self.click_user_registration()
        #return UsersPage(self.current_page,self.urls)

    def get_message_locator(self) -> Locator:
        return self.current_page.locator(self._selectors.MESSAGE)
    
    def get_toast_message(self, fieldname):
        name_msg=""
        if fieldname == "name":
            name_msg = self.current_page.eval_on_selector(self._selectors.USERNAME, "el => el.validationMessage")
        elif fieldname == "email":
            name_msg = self.current_page.eval_on_selector("input[name=email]", "el => el.validationMessage")
        elif fieldname == "accounttype":
            name_msg = self.current_page.eval_on_selector(self._selectors.ACCOUNT_TYPE, "el => el.validationMessage")
        
        return name_msg

    def get_user_registration_button_locator(self) -> Locator:
        return self.current_page.locator(self._selectors.USER_REG_BUTTON)

    class _Selectors:
        USERNAME = "#name"
        EMAIL = "#email"
        ACCOUNT_TYPE = "#accountType"
        USER_REG_BUTTON = "#userRegistration"
        MESSAGE = "#message"



