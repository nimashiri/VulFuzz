results = dict()
import tensorflow as tf
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
from tensorflow.python.ops import gen_nn_ops
try:
  y_backprop_tensor = tf.random.uniform([4, 10, 10, 2], dtype=tf.float32)
  y_backprop = tf.identity(y_backprop_tensor)
  x_tensor = tf.random.uniform([4, 10, 10, 2], dtype=tf.float32)
  x = tf.identity(x_tensor)
  scale_tensor = [] 
  scale = tf.identity(scale_tensor)
  reserve_space_1_tensor = tf.random.uniform([2], dtype=tf.float32)
  reserve_space_1 = tf.identity(reserve_space_1_tensor)
  reserve_space_2_tensor = tf.random.uniform([2], dtype=tf.float32)
  reserve_space_2 = tf.identity(reserve_space_2_tensor)
  epsilon = 0.001
  data_format = "NHWC"
  is_training = False
  reserve_space_3_tensor = tf.random.uniform([], dtype=tf.float32)
  reserve_space_3 = tf.identity(reserve_space_3_tensor)
  results["res"] = gen_nn_ops.fused_batch_norm_grad_v3(y_backprop=y_backprop,x=x,scale=scale,reserve_space_1=reserve_space_1,reserve_space_2=reserve_space_2,epsilon=epsilon,data_format=data_format,is_training=is_training,reserve_space_3=reserve_space_3,)
except Exception as e:
  results["err"] = "Error:"+str(e)

print(results)