import importlib.util
import os


def getobjfrmfile(file_path, function_name):
    "get an object from a python file"
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    spec = importlib.util.spec_from_file_location("module.name", file_path)
    if not spec:
        raise Exception(f"error loading module specs: {file_path!r}")
    module = importlib.util.module_from_spec(spec)
    if not spec.loader:
        raise Exception(f"error loading module spec.lader: {file_path!r}")
    spec.loader.exec_module(module)
    if hasattr(module, function_name):
        return getattr(module, function_name)
    else:
        raise AttributeError(
            f"The component {function_name} does not exist in the module."
        )
