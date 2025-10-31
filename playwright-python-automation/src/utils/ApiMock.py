
import uuid
import json
from src.utils.Converter import Converter
from collections import defaultdict
from src.utils.Logger import get_logger
from resources.mockdata import *

logger = get_logger(__name__)

class ApiMock:
    """Generic in-memory mock API with optional auth simulation."""

    def __init__(self):
        self._store = {} 
        self._auth_tokens = {}
        self._transactiondata = defaultdict(list)

    def login(self, username, password):
        # Simple auth simulation
        if  password == "password":
            token = str(uuid.uuid4())
            self._auth_tokens[username] = token
            return MockResponse({"token": token}, status=200)
        return MockResponse({"error": "Invalid credentials"}, status=401)

    def logout(self, token):
        self._auth_tokens.discard(token)
        return MockResponse({"message": "Logged out"}, status=200)

    def _check_auth(self, token):
        if token not in self._auth_tokens.values():
            return False
        return True
    
    

    def create(self, entity_name, data, token=None):
        if not self._check_auth(token):
            return MockResponse({"error": "Unauthorized"}, status=401)
        
        if 'name' in data and data['name'] == "":
            return MockResponse({"error": "Missing field"}, status=400)
        
        if 'email' in data and Converter.is_valid_email(data['email']) == False:
            return MockResponse({"error": "Missing field"}, status=400)
        
        if 'user_id' in data and data['user_id'] == "":
            return MockResponse({"error": "Missing field"}, status=400)
        
        if 'recipient_id' in data and data['recipient_id'] == "":
            return MockResponse({"error": "Missing field"}, status=400)

        if 'amount' in data and (data['amount'] == "" or data['amount'] < 0):
            return MockResponse({"error": "Invalid amount"}, status=400)
        

        entity_id = str(uuid.uuid4())
        entity = dict(data)
        entity["id"] = entity_id

        if entity_name not in self._store:
            self._store[entity_name] = {}

        self._store[entity_name][entity_id] = entity

        if entity_name is "transaction":
            self._transactiondata[data['user_id']].append(entity_id)
            logger.info(f" self._transactiondata[data['user_id']]  {self._transactiondata[data['user_id']]}" )

        return MockResponse(entity, status=201)

    def get_all(self, entity_name, token=None):
        if not self._check_auth(token):
            return MockResponse({"error": "Unauthorized"}, status=401)
        entities = list(self._store.get(entity_name, {}).values())
        return MockResponse(entities, status=200)
    
   

    def get(self, entity_name, entity_id, token=None):
        if entity_name == "":
            return MockResponse({"error": "Internal server error"}, status=500)
        if token == "generaltoken":
            return MockResponse({"error": "Access denied"}, status=403)
        if not self._check_auth(token):
            return MockResponse({"error": "Unauthorized"}, status=401)
        logger.info(type(self._check_auth))
        logger.info(mock_userid1)

        if entity_id == mock_userid1 and token == self._auth_tokens.get(mock_userid2,"dummy"):
            return MockResponse({"error": "Unauthorized"}, status=401)

        #entity = self._store.get(entity_name, {}).get(entity_id)

        if entity_name == 'transaction':
            logger.info(f" self._transactiondata[entity_id] {entity_id} {self._transactiondata[entity_id]}")
            entity = []
            for key in self._transactiondata[entity_id]:
                entity.append(self._store.get(entity_name, {}).get(key))
            logger.info(f" entity  {entity}" )
        else:
             entity = self._store.get(entity_name, {}).get(entity_id)
            
        if entity:
            return MockResponse(entity, status=200)
        return MockResponse({"error": f"{entity_name} not found"}, status=404)

    def update(self, entity_name, entity_id, data, token=None):
        if not self._check_auth(token):
            return MockResponse({"error": "Unauthorized"}, status=401)
        if entity_name in self._store and entity_id in self._store[entity_name]:
            self._store[entity_name][entity_id].update(data)
            return MockResponse(self._store[entity_name][entity_id], status=200)
        return MockResponse({"error": f"{entity_name} not found"}, status=404)

    def delete(self, entity_name, entity_id, token=None):
        if not self._check_auth(token):
            return MockResponse({"error": "Unauthorized"}, status=401)
        if entity_name in self._store and entity_id in self._store[entity_name]:
            deleted = self._store[entity_name].pop(entity_id)
            return MockResponse(deleted, status=200)
        return MockResponse({"error": f"{entity_name} not found"}, status=404)


class MockResponse:
    def __init__(self, json_data, status=200):
        self._json = json_data
        self.status = status

    def json(self):
        return self._json
