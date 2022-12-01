
import csv
from .decorate_cls import decorate_class
from .decorate_func import decorate_function
import inspect

def hijack(obj, func_name_str, mode=""):
    func_name_list = func_name_str.split('.')
    func_name = func_name_list[-1]

    module_obj = obj
    if len(func_name_list) > 1:
        for module_name in func_name_list[:-1]:
            module_obj = getattr(module_obj, module_name)
    orig_func = getattr(module_obj, func_name)

    def is_class(x):
        return inspect.isclass(x)
    def is_callable(x):
        return callable(x)

    if mode == "function":
        wrapped_func = decorate_function(orig_func, func_name_str)
    elif mode == "class":
        wrapped_func = decorate_class(orig_func, func_name_str)
    else:
        if is_class(orig_func):
            wrapped_func = decorate_class(orig_func, func_name_str)
        elif is_callable(orig_func):
            wrapped_func = decorate_function(orig_func, func_name_str)
        else:
            wrapped_func = orig_func
    setattr(module_obj, func_name, wrapped_func)


with open(__file__.replace("__init__.py", "mxnet_apis.csv"), "r") as f1:
    csv_reader = csv.reader(f1, delimiter=',')
    skipped = ["enable_grad", "get_default_dtype", "load", "tensor", "no_grad", "jit"]
    for l in csv_reader:
        l = l.strip()
        if l not in skipped:
            if l[1] == 'function':
                hijack(nd, l[0], mode="function")
            else:
                hijack(nd, l[0])