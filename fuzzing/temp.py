import tensorflow as tf
from tensorflow.python.ops import nn_ops
try:
  arg_0_tensor = tf.random.uniform([1, 1, 10, 1], dtype=tf.float32, maxval=1879048192)
  arg_0 = tf.identity(arg_0_tensor)
  arg_1_0 = 1
  arg_1_1 = 1
  arg_1_2 = 3
  arg_1_3 = 1
  arg_1 = [arg_1_0,arg_1_1,arg_1_2,arg_1_3,]
  arg_2_0 = 1
  arg_2_1 = None
  arg_2_2 = None
  arg_2_3 = 1
  arg_2 = [arg_2_0,arg_2_1,arg_2_2,arg_2_3,]
  arg_3 = "SAME"
  data_format = None
  results["res"] = nn_ops.max_pool(arg_0,arg_1,arg_2,arg_3,data_format=data_format,)
except Exception as e:
  results["err"] = "Error:"+str(e)
