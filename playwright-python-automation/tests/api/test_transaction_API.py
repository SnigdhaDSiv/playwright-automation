
import pytest
from src.utils.ExecuteAPI import *
from resources.testdata import mock_api
from src.utils.ApiMock import ApiMock
from factories.UserFactory import UserFactory
from factories.TransactionFactory import TransactionFactory
from resources.mockdata import *
from src.utils.DataAccessCompare import DataAccessCompare
from src.utils.CustomAssert  import *
from src.utils.Logger import get_logger
from collections import defaultdict

logger = get_logger(__name__)


class TestUserApi:
   
    @classmethod
    def setup_class(cls):
        cls.dac = DataAccessCompare()
     

    @pytest.fixture(autouse=True, scope='function')
    def setup(self, urls, request):
        self.base_url = urls["WEB_BASE_URL"]
        self.api = ExecuteAPI(self.base_url)
        request.cls.api = self.api
        yield  
        self.api.close()
   

    def test_get_transaction_by_userid(self, datastore):
        """Test GET /trasaction/userid"""
        if datastore.get("mock_api"):
            print(f"datastore.get('mock_api') => {datastore.get('mock_api')} ")
            user = UserFactory.create_user()
            print(user)
            self.mock = ApiMock()
            response_token = self.mock.login(user["name"],"password")
            logger.info(response_token.json()['token'])

            response_create = self.mock.create("users", user,response_token.json()['token'])
            logger.info(response_create.json())
            id = response_create.json()['id']


            transaction = TransactionFactory.create_transaction(mock_userid1)
            response_create = self.mock.create("transaction", transaction,response_token.json()['token'])
            logger.info(response_create.status)
            logger.info(response_create.json()) 
            id = response_create.json()['id']
          

            response = self.mock.get("transaction", mock_userid1 ,response_token.json()['token'])
            logger.info(response.status)
            logger.info(response.json())           
        else:
            #response = self.execute_api(self.base_url, "createtranscations", token_json, payload, baseconfig.headers_api)
            # #data = json.loads(response.content)
            logger.info("mock_api =FALSE")
        
        assert response.status == 200
        mapping_json = self.dac.get_mapping_json("transaction_config")
        fail, message = self.dac.data_compare(response.json()[0], transaction, mapping_json)
        assert fail is False, message
         

    def test_create_transaction(self, datastore):
        """Test POST /posts a transaction"""
        if datastore.get("mock_api"):
            print(f"datastore.get('mock_api') => {datastore.get('mock_api')} ")
            user = UserFactory.create_user()
            print(user)
            self.mock = ApiMock()
            response_token = self.mock.login(user["name"],"password")
            logger.info(response_token.json()['token'])

            response_create = self.mock.create("users", user,response_token.json()['token'])
            logger.info(response_create.json())
            id = response_create.json()['id']


            transaction = TransactionFactory.create_transaction(mock_userid2)
            response = self.mock.create("transaction", transaction,response_token.json()['token'])
            logger.info(response.status)
            logger.info(response.json()) 
            id = response_create.json()['id']
                    
        else:
            #response = self.execute_api(self.base_url, "createtranscations", token_json, payload, baseconfig.headers_api)
            # #data = json.loads(response.content)
            logger.info("mock_api =FALSE")
        
        assert response.status == 201
        mapping_json = self.dac.get_mapping_json("transaction_config")
        fail, message = self.dac.data_compare(response.json(), transaction, mapping_json)
        assert fail is False, message
         

    def test_create_transaction_authentication_invalidtoken(self,datastore):
        """Test POST /posts invalid """
        if datastore.get("mock_api"):
            print(f"datastore.get('mock_api') => {datastore.get('mock_api')} ")
            user = UserFactory.create_user()
            print(user)
            self.mock = ApiMock()
            response_token = self.mock.login(user["name"],"password")
            logger.info(response_token.json()['token'])

            response_create = self.mock.create("users", user,response_token.json()['token'])
            logger.info(response_create.json())
            id = response_create.json()['id']


            transaction = TransactionFactory.create_transaction(mock_userid2)
            response = self.mock.create("transaction", transaction,"dummytoken")
            logger.info(response.status)
            logger.info(response.json()) 
            id = response_create.json()['id']          
        else:
            #response = self.execute_api(self.base_url, "createtranscations", token_json, payload, baseconfig.headers_api)
            # #data = json.loads(response.content)
            logger.info("mock_api =FALSE")
        
       
        CustomAssert.api_status(response.status,401)
        CustomAssert.contains(response.json()['error'],"Unauthorized")


    def test_get_transactions_not_exists(self, datastore):
        """Test GET /users transaction not found"""

        if datastore.get("mock_api"):
            print(f"datastore.get('mock_api') => {datastore.get('mock_api')} ")
            user = UserFactory.create_user()
            print(user)
            self.mock = ApiMock()
            response_token = self.mock.login(user["name"],"password")
            logger.info(response_token.json()['token'])

            response_create = self.mock.create("users", user,response_token.json()['token'])
            logger.info(response_create.json())
            id = response_create.json()['id']

            response = self.mock.get("transaction", "A001" ,response_token.json()['token'])
            logger.info(response.status)
            logger.info(response.json())           
        else:
            #response = self.execute_api(self.base_url, "createtranscations", token_json, payload, baseconfig.headers_api)
            # #data = json.loads(response.content)
            logger.info("mock_api =FALSE")
        

    
        CustomAssert.api_status(response.status,404)
        CustomAssert.contains(response.json()['error'],"transaction not found")

    
    '''def test_update_users(self):
        """Test PUT /users user not found"""
        print(mock_api)'''

    
    '''def test_delete_users(self):
         """Test DELETE /users valid user"""
         print(mock_api)'''

    
    def test_auth_transactions_insuffient_permission(self, datastore):
        """Test invalid token """
        if datastore.get("mock_api"):
            print(f"datastore.get('mock_api') => {datastore.get('mock_api')} ")
            user = UserFactory.create_user()
            print(user)
            self.mock = ApiMock()
            response_token = self.mock.login(user["name"],"password")
            logger.info(response_token.json()['token'])

            response_create = self.mock.create("users", user,response_token.json()['token'])
            logger.info(response_create.json())
            id = response_create.json()['id']

            response = self.mock.get("transaction", "A002" ,"generaltoken")
            logger.info(response.status)
            logger.info(response.json())           
        else:
            #response = self.execute_api(self.base_url, "createusers", token_json, payload, baseconfig.headers_api)
            # #data = json.loads(response.content)
            logger.info("mock_api =FALSE")
        
        CustomAssert.api_status(response.status,403)
        CustomAssert.contains(response.json()['error'],"Access denied")

        

    def test_user_detail_data_validation(self, datastore):
        """" add a user ,add a transaction, get api and check the user exists and validate the data"""
        if datastore.get("mock_api"):
            print(f"datastore.get('mock_api') => {datastore.get('mock_api')} ")
            user = UserFactory.create_user()
            print(user)
            self.mock = ApiMock()
            response_token = self.mock.login(user["name"],"password")
            logger.info(response_token.json()['token'])

            response_create = self.mock.create("users", user,response_token.json()['token'])
            logger.info(response_create.json())
            id = response_create.json()['id']


            transaction = TransactionFactory.create_transaction(mock_userid1)
            response_create = self.mock.create("transaction", transaction,response_token.json()['token'])
            logger.info(response_create.status)
            logger.info(response_create.json()) 
            id = response_create.json()['id']
          

            response = self.mock.get("transaction", mock_userid1 ,response_token.json()['token'])
            logger.info(response.status)
            logger.info(response.json())           
        else:
            
            #response = self.execute_api(self.base_url, "createtranscations", token_json, payload, baseconfig.headers_api)
            # #data = json.loads(response.content)
            logger.info("mock_api =FALSE")
        
        assert response.status == 200
        mapping_json = self.dac.get_mapping_json("transaction_config")
        fail, message = self.dac.data_compare(response.json()[0], transaction, mapping_json)
        assert fail is False, message
         

    def test_create_transaction_empty_userid(self, datastore):
        """Test POST /posts empty userid"""
        if datastore.get("mock_api"):
            print(f"datastore.get('mock_api') => {datastore.get('mock_api')} ")
            user = UserFactory.create_user()
            print(user)
            self.mock = ApiMock()
            response_token = self.mock.login(user["name"],"password")
            logger.info(response_token.json()['token'])

            response_create = self.mock.create("users", user,response_token.json()['token'])
            logger.info(response_create.json())
            id = response_create.json()['id']


            transaction = TransactionFactory.create_transaction(mock_userid1)
            transaction["user_id"] = ""
            response = self.mock.create("transaction", transaction,response_token.json()['token'])
            logger.info(response.status)
            logger.info(response.json()) 
       
        else:
            #response = self.execute_api(self.base_url, "createusers", token_json, payload, baseconfig.headers_api)
            # #data = json.loads(response.content)
            logger.info("mock_api =FALSE")
        
        CustomAssert.api_status(response.status,400)
        CustomAssert.contains(response.json()['error'],"Missing field")

    def test_create_transactionid_empty_receipient_id(self, datastore):
        """Test POST /posts invalid email"""
        if datastore.get("mock_api"):
            print(f"datastore.get('mock_api') => {datastore.get('mock_api')} ")
            user = UserFactory.create_user()
            print(user)
            self.mock = ApiMock()
            response_token = self.mock.login(user["name"],"password")
            logger.info(response_token.json()['token'])

            response_create = self.mock.create("users", user,response_token.json()['token'])
            logger.info(response_create.json())
            id = response_create.json()['id']


            transaction = TransactionFactory.create_transaction(mock_userid1)
            transaction["recipient_id"] = ""
            response = self.mock.create("transaction", transaction,response_token.json()['token'])
            logger.info(response.status)
            logger.info(response.json()) 
        else:
            #response = self.execute_api(self.base_url, "createusers", token_json, payload, baseconfig.headers_api)
            # #data = json.loads(response.content)
            logger.info("mock_api =FALSE")
        
        CustomAssert.api_status(response.status,400)
        CustomAssert.contains(response.json()['error'],"Missing field")
    
    def test_create_transaction_id_invalid_amount(self, datastore):
        """Test POST /posts invalid email"""
        if datastore.get("mock_api"):
            print(f"datastore.get('mock_api') => {datastore.get('mock_api')} ")
            user = UserFactory.create_user()
            print(user)
            self.mock = ApiMock()
            response_token = self.mock.login(user["name"],"password")
            logger.info(response_token.json()['token'])

            response_create = self.mock.create("users", user,response_token.json()['token'])
            logger.info(response_create.json())
            id = response_create.json()['id']


            transaction = TransactionFactory.create_transaction(mock_userid1)
            transaction["amount"] = -100
            response = self.mock.create("transaction", transaction,response_token.json()['token'])
            logger.info(response.status)
            logger.info(response.json()) 
        else:
            #response = self.execute_api(self.base_url, "createusers", token_json, payload, baseconfig.headers_api)
            # #data = json.loads(response.content)
            logger.info("mock_api =FALSE")
        
        CustomAssert.api_status(response.status,400)
        CustomAssert.contains(response.json()['error'],"Invalid amount")
    
    def test_get_transaction_cross_user_access_check_auth_neg(self, datastore):
        """ get transaction of user2 using the user1 token"""

        if datastore.get("mock_api"):
            print(f"datastore.get('mock_api') => {datastore.get('mock_api')} ")
            user1 = UserFactory.create_user()
            user2 = UserFactory.create_user()
            logger.info(f" user1 {user1} user2 {user2}")
            self.mock = ApiMock()
            response_token1 = self.mock.login(mock_userid1,"password")
            response_token2 = self.mock.login(mock_userid2,"password")
            logger.info(response_token2.json()['token'])

    

            transaction = TransactionFactory.create_transaction(mock_userid1)
            response_create = self.mock.create("transaction", transaction,response_token1.json()['token'])
            logger.info(response_create.status)
            logger.info(response_create.json()) 
            id = response_create.json()['id']

            response = self.mock.get("transaction", mock_userid1 ,response_token2.json()['token'])
            logger.info(response.status)
            logger.info(response.json())           
        else:
            #response = self.execute_api(self.base_url, "createtranscations", token_json, payload, baseconfig.headers_api)
            # #data = json.loads(response.content)
            logger.info("mock_api =FALSE")
        
        assert response.status == 401
        CustomAssert.contains(response.json()['error'],"Unauthorized")


        



   