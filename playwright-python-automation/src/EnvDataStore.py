from src.utils.load_env_module import load_env_module

class EnvDataStore:
    _instance = None
    def  __init__(self, env="qa"):
        self.data = {}
        self.data = load_env_module(env)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def all(self):
        return self.data

    def load_env_data(self, env):
        self.data = load_env_module(env)
    
    def reload(self, env=None):
        self.env = (env or self.env).lower()
        self.data = load_env_module(env)


