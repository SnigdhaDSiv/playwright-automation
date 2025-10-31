import importlib
import os


def load_env_module(env: str = None):
   
    env = (env or os.getenv("ENV_NAME", "qa")).lower()

    module_names = [
        f"resources.testdata.testdata_{env}",
        f"resources.testdata.testdata_api_{env}"
    ]

    data = {}
    for module_name in module_names:
        try:
            module = importlib.import_module(module_name)
            for attr in dir(module):
                if not attr.startswith("_"):
                    data[attr] = getattr(module, attr)
        except ModuleNotFoundError as e:
            raise RuntimeError(f"Test data module not found: {e.name}")

    return data
