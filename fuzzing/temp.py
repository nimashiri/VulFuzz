import tensorflow as tf
try:
  arg_0_tensor = tf.constant(-1250999896764, shape=[50, 200, 1], dtype=tf.float32,)
  arg_0 = tf.identity(arg_0_tensor)
  perm_0 = 1
  perm_1 = 0
  perm_2 = 2
  perm = [perm_0,perm_1,perm_2,]
  results["res"] = tf.transpose(arg_0,perm=perm,)
except Exception as e:
  results["err"] = "Error:"+str(e)
