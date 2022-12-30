import tensorflow as tf


x = tf.constant(3.0)
with tf.GradientTape() as g:
  g.watch(x)
  y = x * x
dy_dx = g.gradient(y, x)
print(dy_dx)
tf.Tensor(6.0, shape=(), dtype=float32)
x = tf.constant(5.0)
with tf.GradientTape() as g:
  g.watch(x)
  with tf.GradientTape() as gg:
    gg.watch(x)
    y = x * x
  dy_dx = gg.gradient(y, x)  # dy_dx = 2 * x
d2y_dx2 = g.gradient(dy_dx, x)  # d2y_dx2 = 2
print(dy_dx)
tf.Tensor(10.0, shape=(), dtype=float32)
print(d2y_dx2)
tf.Tensor(2.0, shape=(), dtype=float32)
x = tf.constant(3.0)

with tf.GradientTape(persistent=True) as g:
  g.watch(x)
  y = x * x
  z = y * y
dz_dx = g.gradient(z, x)  # (4*x^3 at x = 3)
print(dz_dx)
tf.Tensor(108.0, shape=(), dtype=float32)
dy_dx = g.gradient(y, x)
print(dy_dx)
tf.Tensor(6.0, shape=(), dtype=float32)
x = tf.Variable(2.0)
w = tf.Variable(5.0)
with tf.GradientTape(
    watch_accessed_variables=False, persistent=True) as tape:
  tape.watch(x)
  y = x ** 2  # Gradients will be available for `x`.
  z = w ** 3  # No gradients will be available as `w` isn't being watched.
dy_dx = tape.gradient(y, x)
print(dy_dx)
tf.Tensor(4.0, shape=(), dtype=float32)
# No gradients will be available as `w` isn't being watched.
dz_dw = tape.gradient(z, w)
print(dz_dw)
None
a = tf.keras.layers.Dense(32)
b = tf.keras.layers.Dense(32)


with tf.GradientTape() as g:
  x = tf.constant([[1., 2.], [3., 4.]], dtype=tf.float32)
  g.watch(x)
  y = x * x

batch_jacobian = g.batch_jacobian(y, x)
