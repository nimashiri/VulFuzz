
# import tensorflow as tf
# from tensorflow.python.ops import array_ops
# from tensorflow.python.ops import array_grad
# from tensorflow.python.ops import gen_array_ops
from tensorflow.python.ops import io_ops, clip_ops

# from tensorflow.python.framework import sparse_tensor
# import tensorflow as tf
# tf.compat.v1.disable_eager_execution()

# input_tensor = array_ops.placeholder(tf.float32, shape=[4, 4])

# array_ops.quantize_and_dequantize_v2(input_tensor,
#                                                         input_min = 5.0,
#                                                         input_max= -10.0,
#                                                         range_given=True)
# x = tf.constant([1, 1, 2, 4, 4, 4, 7, 8, 8])
# gen_array_ops.unique(x)

# clip_ops.clip_by_value(x, clip_value_min=-1, clip_value_max=1)


import ast, os

skip_list_dir  = [
    'profiler',
    '__pycache__',
    'compat',
    'compiler',
    'data',
    'debug',
    'dis',
    'dlpack',
    'kernel_tests',
    'lib',
    'tools',
    'tpu'
]

for root, dirs, files in os.walk('/home/nimashiri/.local/lib/python3.8/site-packages/tensorflow/python/'):
    for module in dirs:
        current_module = os.path.join(root, module)
        current_module
        

with open("/home/nimashiri/.local/lib/python3.8/site-packages/tensorflow/python/ops/clip_ops.py", "r") as source:
    ast_tree = ast.parse(source.read())

f_names = [x.name for x in ast.walk(ast_tree) if isinstance(x, ast.FunctionDef) or isinstance(x, ast.ClassDef)]
print(f_names,'\n')

f_objects = [x for x in ast.walk(ast_tree) if isinstance(x, ast.FunctionDef) or isinstance(x, ast.ClassDef)]
for f in f_objects:
    print(ast.get_docstring(f))