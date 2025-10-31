
import pytest
from src.utils.ExecuteAPI import *
from resources.testdata import mock_api
from src.utils.ApiMock import ApiMock
from factories.UserFactory import UserFactory
from resources.mockdata import headers,mock_user_list
from src.utils.DataAccessCompare import DataAccessCompare
from src.utils.CustomAssert  import *
from src.utils.Logger import get_logger

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
   

  

    def test_get_users_by_id(self, datastore):
        """Test GET /users"""
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
            response = self.mock.get("users", id,response_token.json()['token'])
            logger.info(response.status)
            logger.info(response.json())           
        else:
            #response = self.execute_api(self.base_url, "createusers", token_json, payload, baseconfig.headers_api)
            # #data = json.loads(response.content)
            logger.info("mock_api =FALSE")
        
        assert response.status == 200
        mapping_json = self.dac.get_mapping_json("users_config")
        fail, message = self.dac.data_compare(response.json(), user, mapping_json)
        assert fail is False, message
         

    def test_create_users(self, datastore):
        """Test POST /posts"""
        if datastore.get("mock_api"):
            print(f"datastore.get('mock_api') => {datastore.get('mock_api')} ")
            user = UserFactory.create_user()
            print(user)
            self.mock = ApiMock()
            response_token = self.mock.login(user["name"],"password")
            logger.info(response_token.json()['token'])
            response = self.mock.create("users", user,response_token.json()['token'])
            logger.info(response.json())
            id = response.json()['id']
            
           
        else:
            #response = self.execute_api(self.base_url, "createusers", token_json, payload, baseconfig.headers_api)
            # #data = json.loads(response.content)
            logger.info("mock_api =FALSE")
        
        assert response.status == 201
        mapping_json = self.dac.get_mapping_json("users_config")
        fail, message = self.dac.data_compare(response.json(), user, mapping_json)
        logger.info(message)
        assert fail is False, message

    def test_create_users_authentication_invalidtoken(self,datastore):
        """Test POST /posts invalid"""
        if datastore.get("mock_api"):
            print(f"datastore.get('mock_api') => {datastore.get('mock_api')} ")
            user = UserFactory.create_user()
            print(user)
            self.mock = ApiMock()
            response_token = self.mock.login(user["name"],"password")
            logger.info(response_token.json()['token'])
            response = self.mock.create("users", user,"dummytoken")
            logger.info(response.json())
           
        else:
            #response = self.execute_api(self.base_url, "createusers", token_json, payload, baseconfig.headers_api)
            # #data = json.loads(response.content)
            logger.info("mock_api =FALSE")
        
       
        CustomAssert.api_status(response.status,401)
        CustomAssert.contains(response.json()['error'],"Unauthorized")


    def test_get_users_not_exists(self, datastore):
        """Test GET /users user not found"""
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
            response = self.mock.get("users", "notexits",response_token.json()['token'])
            logger.info(response.status)
            logger.info(response.json())           
        else:
            #response = self.execute_api(self.base_url, "getusersdetails", token_json, payload, baseconfig.headers_api)
            # #data = json.loads(response.content)
            logger.info("mock_api =FALSE")
        
        CustomAssert.api_status(response.status,404)
        CustomAssert.contains(response.json()['error'],"users not found")

    
    '''def test_update_users(self):
        """Test PUT /users user not found"""
        print(mock_api)'''

    
    '''def test_delete_users(self):
         """Test DELETE /users valid user"""
         print(mock_api)'''

    
    def test_auth_users_insuffient_permission(self, datastore):
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
            response = self.mock.get("users",id,"generaltoken")
            logger.info(response.status)
            logger.info(response.json())           
        else:
            #response = self.execute_api(self.base_url, "createusers", token_json, payload, baseconfig.headers_api)
            # #data = json.loads(response.content)
            logger.info("mock_api =FALSE")
        
        CustomAssert.api_status(response.status,403)
        CustomAssert.contains(response.json()['error'],"Access denied")

        

    def test_user_detail_data_validation(self, datastore):
        """" add a user , get api and check the user exists and validate the data"""
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
            response = self.mock.get("users", id,response_token.json()['token'])
            logger.info(response.status)
            logger.info(response.json())           
        else:
            #response = self.execute_api(self.base_url, "createusers", token_json, payload, baseconfig.headers_api)
            # #data = json.loads(response.content)
            logger.info("mock_api =FALSE")
        
        assert response.status == 200
        # Data validation
        mapping_json = self.dac.get_mapping_json("users_config")
        fail, message = self.dac.data_compare(response.json(), user, mapping_json)
        assert fail is False, message

    def test_create_user_empty_name(self, datastore):
        """Test POST /posts empty username"""
        if datastore.get("mock_api"):
            print(f"datastore.get('mock_api') => {datastore.get('mock_api')} ")
            user = UserFactory.create_user()
            print(user)
            self.mock = ApiMock()
            response_token = self.mock.login(user["name"],"password")
            logger.info(response_token.json()['token'])
            user["name"] = ""
            response = self.mock.create("users", user,response_token.json()['token'])
            logger.info(response.json())
 
        else:
            #response = self.execute_api(self.base_url, "createusers", token_json, payload, baseconfig.headers_api)
            # #data = json.loads(response.content)
            logger.info("mock_api =FALSE")
        
        CustomAssert.api_status(response.status,400)
        CustomAssert.contains(response.json()['error'],"Missing field")

    def test_create_user_invalid_email(self, datastore):
        """Test POST /posts invalid email"""
        if datastore.get("mock_api"):
            print(f"datastore.get('mock_api') => {datastore.get('mock_api')} ")
            user = UserFactory.create_user()
            print(user)
            self.mock = ApiMock()
            response_token = self.mock.login(user["name"],"password")
            logger.info(response_token.json()['token'])
            user["name"] = ""
            response = self.mock.create("users", user,response_token.json()['token'])
            logger.info(response.json())
          
            
           
        else:
            #response = self.execute_api(self.base_url, "createusers", token_json, payload, baseconfig.headers_api)
            # #data = json.loads(response.content)
            logger.info("mock_api =FALSE")
        
        CustomAssert.api_status(response.status,400)
        CustomAssert.contains(response.json()['error'],"Missing field")
    
    def test_get_users_server_error(self, datastore):
        """Test GET /users user not found"""
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
            response = self.mock.get("", "notexits",response_token.json()['token'])
            logger.info(response.status)
            logger.info(response.json())           
        else:
            #response = self.execute_api(self.base_url, "getusersdetails", token_json, payload, baseconfig.headers_api)
            # #data = json.loads(response.content)
            logger.info("mock_api =FALSE")
        
        CustomAssert.api_status(response.status,500)
        CustomAssert.contains(response.json()['error'],"Internal server error")

        



   