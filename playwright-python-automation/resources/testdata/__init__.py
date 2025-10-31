import os
import importlib

def load_data():
    env = os.getenv("ENV_NAME", "qa").lower()

    print(env)
    module_name = f"resources.testdata.testdata_{env}"  
    module_name_api = f"resources.testdata.testdata_api_{env}"  

    try:
        print(f"module_name => {module_name}")
        _testdata = importlib.import_module(module_name)
        _testdata_api = importlib.import_module(module_name_api)
        print(f"module_name_api => {module_name_api}")
    except ModuleNotFoundError:
        raise RuntimeError(f" Test data not found {env}")

    import_attributes(_testdata, globals()) 
    import_attributes(_testdata_api, globals()) 

def import_attributes(module, namespace:dict):
    for attr in dir(module):
        if not attr.startswith("_"):
            namespace[attr] = getattr(module, attr)
    
    print(globals())

    
load_data()


