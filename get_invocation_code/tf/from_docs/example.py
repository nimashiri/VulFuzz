import tensorflow as tf
from tensorflow import lu_matrix_inverse
inv_X = tf.lu_matrix_inverse(*tf.linalg.lu(X))
tf.assert_near(tf.matrix_inverse(X), inv_X)

