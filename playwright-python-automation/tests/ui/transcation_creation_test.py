
import pytest
from playwright.sync_api import Page, expect
from src.page_objects.transaction_page import TransactionPage
from src.utils.Logger import get_logger
from resources.testdata import transactions_postive
from resources.testdata import transactions_negative
from src.utils.Converter import Converter


logger = get_logger(__name__)


@pytest.mark.ui
class TestTransactionCreation:
    @pytest.fixture(autouse=True, scope='function')
    def setup(self, page: Page, urls):
        self.transaction_creation = TransactionPage(page, urls)
        
    @pytest.mark.parametrize("trans",transactions_postive)
    def test_transaction_creation(self, trans):
        """	transaction creation postive use cases """
        self.transaction_creation.goto_transaction_page()
        logger.info(f"transaction => {trans}")   
        val = Converter.format_float_decimal(trans['amount'], 2)
        logger.info(f"value after rounding => {val}")  
        expected_string = trans['expected']['ui'].replace("${userId}", trans['userid']).replace("${recipientId}",trans['recipientId']).replace("${amount}", val)
        logger.info(f"from locater=> {self.transaction_creation.get_message_locator()}")
        logger.info(f"expected_string =>{expected_string}")
        self.transaction_creation.transaction_reg_to_application(trans['userid'], trans['recipientId'], trans['amount'],trans['type'])
        expect(self.transaction_creation.get_message_locator()).to_have_text(expected_string)
    
    @pytest.mark.parametrize("trans",transactions_negative)
    def test_transaction_creation_error(self, trans):
        """	transaction creation negative use cases """
        self.transaction_creation.goto_transaction_page()
        logger.info(f"transaction => {trans}")   
        self.transaction_creation.transaction_reg_to_application(trans['userid'], trans['recipientId'], trans['amount'],trans['type'])
        expect(self.transaction_creation.get_message_locator()).to_have_text(trans['expected']['ui'])
    
    

    


 
    


 
