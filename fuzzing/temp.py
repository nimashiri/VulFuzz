import tensorflow as tf
import numpy as np
from tensorflow.python.ops import array_ops
try:
  try:
    with tf.device('/CPU'):
      arg_0_tensor = np.nan
      arg_0 = tf.identity(arg_0_tensor)
      maxlen = 5
      out = array_ops.sequence_mask(arg_0,maxlen=maxlen,)
      print(out)
  except Exception as e:
    print("Error:"+str(e))
  try:
    with tf.device('/GPU:0'):
      arg_0 = tf.identity(arg_0_tensor)
      arg_0 = tf.cast(arg_0, tf.int64)
      out = array_ops.sequence_mask(arg_0,maxlen=maxlen,)
  except Exception as e:
    print("Error:"+str(e))
except Exception as e:
  print("Error:"+str(e))