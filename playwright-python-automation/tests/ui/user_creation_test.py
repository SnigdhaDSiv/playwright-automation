
import pytest
from playwright.sync_api import Page, expect
from src.page_objects.users_page import UsersPage
from src.utils.Logger import get_logger
from resources.testdata import data_users
from resources.testdata import data_users_negative

logger = get_logger(__name__)

@pytest.mark.ui
class TestUserCreation:

    @pytest.fixture(autouse=True, scope='function')
    def setup(self, page: Page, urls):
        self.user_creation = UsersPage(page, urls)
        print(data_users)
    
    @pytest.mark.parametrize("users",data_users)
    def test_user_creation(self, users):
        """	user creation postive use cases """
        self.user_creation.goto_users_page()
        logger.info(f"users['username'] {users['username']}, users['email'] { users['email']}, users['accounttype'] {users['accounttype']}")   
        self.user_creation.user_reg_to_application(users['username'], users['email'], users['accounttype'])
        expect(self.user_creation.get_message_locator()).to_have_text(users['expected']['ui'])
    
    @pytest.mark.parametrize("users",data_users_negative)
    def test_user_creation_error(self, users):
        """	user creation negative use cases """
        self.user_creation.goto_users_page()
        logger.info(f"users['username'] {users['username']}, users['email'] { users['email']}, users['accounttype'] {users['accounttype']}")   
        self.user_creation.user_reg_to_application(users['username'], users['email'], users['accounttype'])
        if users['expected']['message'] == "True":
            expect(self.user_creation.get_message_locator()).to_have_text(users['expected']['ui'])
        else:
            print(f" users => {users['expected']['message']}")
            expect(self.user_creation.get_toast_message(users['expected']['message'])).to_have_text(users['expected']['ui'])

    

    


 
    


 
