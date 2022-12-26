results = dict()
import tensorflow as tf
import os
import numpy as np
from tensorflow.python.ops import gen_count_ops
try:
  arg_0_tensor = tf.constant(np.nan, shape=[3, 1], dtype=tf.float64,)
  arg_0 = tf.identity(arg_0_tensor)
  arg_1_tensor = tf.random.uniform([3], minval=-256, maxval=257, dtype=tf.int32)
  arg_1 = tf.identity(arg_1_tensor)
  arg_2_tensor = tf.random.uniform([1], minval=-256, maxval=257, dtype=tf.int64)
  arg_2 = tf.identity(arg_2_tensor)
  arg_3_tensor = tf.random.uniform([0], minval=-256, maxval=257, dtype=tf.int32)
  arg_3 = tf.identity(arg_3_tensor)
  minlength = -1
  maxlength = -1
  binary_output = False
  results["res"] = gen_count_ops.sparse_count_sparse_output(arg_0,arg_1,arg_2,arg_3,minlength=minlength,maxlength=maxlength,binary_output=binary_output,)
except Exception as e:
  results["err"] = "Error:"+str(e)