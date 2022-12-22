import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import DeviceSpec
device_spec = DeviceSpec(job="ps", device_type="GPU", device_index=0)
with tf.device(device_spec.to_string()):
  my_var = tf.Variable([1, 2, 3, 4, 5, 6, 7, 8], name="my_variable")
  squared_var = tf.square(my_var)

