import tensorflow as tf
from tensorflow.python.ops import nn_ops
try:
  arg_0_0_0 = 5.478554e-06
  arg_0_0_1 = 5.478554e-06
  arg_0_0_2 = 5.478554e-06
  arg_0_0_3 = 5.478554e-06
  arg_0_0 = [arg_0_0_0,arg_0_0_1,arg_0_0_2,arg_0_0_3,]
  arg_0_1_0 = 5.478554e-06
  arg_0_1_1 = 5.478554e-06
  arg_0_1_2 = 5.478554e-06
  arg_0_1_3 = 5.478554e-06
  arg_0_1 = [arg_0_1_0,arg_0_1_1,arg_0_1_2,arg_0_1_3,]
  arg_0 = [arg_0_0,arg_0_1,]
  arg_1_0 = 1
  arg_1_1 = 3
  arg_1 = [arg_1_0,arg_1_1,]
  arg_2 = 2
  results["res"] = nn_ops.in_top_k(arg_0,arg_1,arg_2,)
except Exception as e:
  results["err"] = "Error:"+str(e)
