import torch
import inspect
# x = torch.nn.MaxPool1d(1, stride=2)
# getattr(x)

   # Utilities.
def is_class(x):
    return inspect.isclass(x)
def is_callable(x):
    return callable(x)
def is_built_in_or_extension_type(x):
    if is_class(x) and hasattr(x, '__dict__') and not '__module__' in x.__dict__:
        return True
    else:
        return False
        
def build_param_dict(*args, **kwargs):
    param_dict = dict()
    for ind, arg in enumerate(args):
        param_dict['parameter:%d' % ind] = sighdl.get_var_signature(arg)
    for key, value in kwargs.items():
        if key == 'name': continue
        param_dict[key] = sighdl.get_var_signature(value)
    param_dict = dict(param_dict)
    return param_dict

def dump_signature_of_class(klass, class_name, output_dir):
    if not hasattr(klass, '__call__'):
        return klass
    old_init = klass.__init__
    old_call = klass.__call__
    init_params = dict()


    def new_init(self, *args, **kwargs):
        nonlocal init_params
        try:
            init_params = build_param_dict(*args, **kwargs)
        except Exception as e:
            print(e.message)
        old_init(self, *args, **kwargs)

    def new_call(self, *inputs, **kwargs):
        nonlocal init_params

        input_signature = get_signature_for_tensors(inputs)
        outputs = old_call(self, *inputs, **kwargs)
        output_signature = get_signature_for_tensors(outputs)
        write_fn(self.__class__.__module__ + '.' + self.__class__.__name__, init_params, input_signature,
                 output_signature)
        return outputs

    klass.__init__ = new_init
    klass.__call__ = new_call
    return klass

def hijach(obj, api_name):
    module_obj = getattr(obj, api_name.split('.')[-2])
    orig_func = getattr(module_obj, api_name.split('.')[-1])

    if is_built_in_or_extension_type(orig_func):
      return False
    if is_class(orig_func):
        if hasattr(orig_func, '__slots__'):
            return False
        wrapped_func = dump_signature_of_class(orig_func, api_name.split('.')[-1], output_dir=output_dir)
        setattr(module_obj, api_name.split('.')[-1], wrapped_func)
        pass
    else:
        if is_callable(orig_func):
            wrapped_func = dump_signature_of_function(orig_func, func_name_str, output_dir=output_dir)
            setattr(module_obj, func_name, wrapped_func)
            return True
        else:
            return False


if __name__ == '__main__':
    torch.nn.MaxPool1d(1, stride=2)
    api_name = 'torch.nn.MaxPool1d'
    hijach(torch, api_name)