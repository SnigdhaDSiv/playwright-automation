from playwright.sync_api import Page, Locator
from src.page_objects.base_page import BasePage


class TransactionPage(BasePage):

    def __init__(self, page: Page, urls):
        super().__init__(page, urls)
        self.current_page = page
        self.urls = urls
        self._selectors = self._Selectors()

  
    def goto_transaction_page(self,value:str = "transaction_creation.html"):
        print(f" ******baseurl => {self.urls} {self.urls['WEB_BASE_URL']}")
        baseurl =  self.urls["WEB_BASE_URL"]+'transaction_creation.html'
        #self.current_page.goto("http://localhost:8000/user_registration.html")
        self.current_page.goto(baseurl)

    def set_user_id(self, value: str):
        self.current_page.fill(self._selectors.USERID, value)

    def set_recipient_id(self, value: str):
        self.current_page.fill(self._selectors.RECIPIENTID, value)
    
    def set_amount(self, value: str):
         self.current_page.fill(self._selectors.AMOUNT, value)

    def set_transfer_type(self, value: str):
        self.current_page.select_option(self._selectors.TRANSFER_TYPE, value)

    def click_create_transfer(self):
        self.current_page.click(self._selectors.TRANSACTION_CREATE_BUTTON)

    def transaction_reg_to_application(self, userid: str, recipientid: str,amount: str, transfertype: str):
        self.set_user_id(userid)
        self.set_recipient_id(recipientid)
        self.set_amount(amount)
        self.set_transfer_type(transfertype)
        self.click_create_transfer()
        #return UsersPage(self.current_page,self.urls)

    def get_message_locator(self) -> Locator:
        return self.current_page.locator(self._selectors.MESSAGE)
    
    def get_toast_message(self, fieldname):
        name_msg=""
        if fieldname == "name":
            name_msg = self.current_page.eval_on_selector(self._selectors.USERID, "el => el.validationMessage")
        elif fieldname == "email":
            name_msg = self.current_page.eval_on_selector("input[name=email]", "el => el.validationMessage")
        elif fieldname == "accounttype":
            name_msg = self.current_page.eval_on_selector(self._selectors.TRANSFER_TYPE, "el => el.validationMessage")
        
        return name_msg

    def get_trans_registration_button_locator(self) -> Locator:
        return self.current_page.locator(self._selectors.TRANSACTION_CREATE_BUTTON)

    class _Selectors:
        USERID = "#userId"
        RECIPIENTID = "#recipientId"
        AMOUNT = "#amount"
        TRANSFER_TYPE = "#type"
        TRANSACTION_CREATE_BUTTON = "#create_transaction"
        MESSAGE = "#message"



