import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow.experimental import dtensor

def configure_virtual_cpus(ncpu):
  phy_devices = tf.config.list_physical_devices('CPU')
  tf.config.set_logical_device_configuration(
        phy_devices[0], 
        [tf.config.LogicalDeviceConfiguration()] * ncpu)

configure_virtual_cpus(8)
tf.config.list_logical_devices('CPU')

devices = [f'CPU:{i}' for i in range(8)]

tf.keras.backend.experimental.enable_tf_random_generator()
tf.keras.utils.set_random_seed(1337)

mesh = dtensor.create_mesh([("batch", 8)], devices=devices)

example_weight_layout = dtensor.Layout([dtensor.UNSHARDED, dtensor.UNSHARDED], mesh)  # or
example_weight_layout = dtensor.Layout.replicated(mesh, rank=2)

example_data_layout = dtensor.Layout(['batch', dtensor.UNSHARDED], mesh)  # or
example_data_layout = dtensor.Layout.batch_sharded(mesh, 'batch', rank=2)

unsharded_layout_2d = dtensor.Layout.replicated(mesh, 2)
unsharded_layout_1d = dtensor.Layout.replicated(mesh, 1)

model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28)),
  tf.keras.layers.Dense(128, 
                        activation='relu',
                        name='d1',
                        kernel_layout=unsharded_layout_2d, 
                        bias_layout=unsharded_layout_1d),
  tf.keras.layers.Dense(10,
                        name='d2',
                        kernel_layout=unsharded_layout_2d, 
                        bias_layout=unsharded_layout_1d)
])

for weight in model.weights:
  print(f'Weight name: {weight.name} with layout: {weight.layout}')
  break

def normalize_img(image, label):
  """Normalizes images: `uint8` -> `float32`."""
  return tf.cast(image, tf.float32) / 255., label

batch_size = 128

ds_train = ds_train.map(
    normalize_img, num_parallel_calls=tf.data.AUTOTUNE)
ds_train = ds_train.cache()
ds_train = ds_train.shuffle(ds_info.splits['train'].num_examples)
ds_train = ds_train.batch(batch_size)
ds_train = ds_train.prefetch(tf.data.AUTOTUNE)

ds_test = ds_test.map(
    normalize_img, num_parallel_calls=tf.data.AUTOTUNE)
ds_test = ds_test.batch(batch_size)
ds_test = ds_test.cache()
ds_test = ds_test.prefetch(tf.data.AUTOTUNE)

@tf.function
def train_step(model, x, y, optimizer, metrics):
  with tf.GradientTape() as tape:
    logits = model(x, training=True)
    # tf.reduce_sum sums the batch sharded per-example loss to a replicated
    # global loss (scalar).
    loss = tf.reduce_sum(tf.keras.losses.sparse_categorical_crossentropy(
        y, logits, from_logits=True))

  gradients = tape.gradient(loss, model.trainable_variables)
  optimizer.apply_gradients(zip(gradients, model.trainable_variables))

  for metric in metrics.values():
    metric.update_state(y_true=y, y_pred=logits)

  loss_per_sample = loss / len(x)
  results = {'loss': loss_per_sample}
  return results

@tf.function
def eval_step(model, x, y, metrics):
  logits = model(x, training=False)
  loss = tf.reduce_sum(tf.keras.losses.sparse_categorical_crossentropy(
        y, logits, from_logits=True))

  for metric in metrics.values():
    metric.update_state(y_true=y, y_pred=logits)

  loss_per_sample = loss / len(x)
  results = {'eval_loss': loss_per_sample}
  return results

def pack_dtensor_inputs(images, labels, image_layout, label_layout):
  num_local_devices = image_layout.mesh.num_local_devices()
  images = tf.split(images, num_local_devices)
  labels = tf.split(labels, num_local_devices)
  images = dtensor.pack(images, image_layout)
  labels = dtensor.pack(labels, label_layout)
  return  images, labels

optimizer = tf.keras.dtensor.experimental.optimizers.Adam(0.01, mesh=mesh)
metrics = {'accuracy': tf.keras.metrics.SparseCategoricalAccuracy(mesh=mesh)}
eval_metrics = {'eval_accuracy': tf.keras.metrics.SparseCategoricalAccuracy(mesh=mesh)}

num_epochs = 3

image_layout = dtensor.Layout.batch_sharded(mesh, 'batch', rank=4)
label_layout = dtensor.Layout.batch_sharded(mesh, 'batch', rank=1)

for epoch in range(num_epochs):
  print("============================") 
  print("Epoch: ", epoch)
  for metric in metrics.values():
    metric.reset_state()
  step = 0
  results = {}
  pbar = tf.keras.utils.Progbar(target=None, stateful_metrics=[])
  for input in ds_train:
    images, labels = input[0], input[1]
    images, labels = pack_dtensor_inputs(
        images, labels, image_layout, label_layout)

    results.update(train_step(model, images, labels, optimizer, metrics))
    for metric_name, metric in metrics.items():
      results[metric_name] = metric.result()

    pbar.update(step, values=results.items(), finalize=False)
    step += 1
  pbar.update(step, values=results.items(), finalize=True)

  for metric in eval_metrics.values():
    metric.reset_state()
  for input in ds_test:
    images, labels = input[0], input[1]
    images, labels = pack_dtensor_inputs(
        images, labels, image_layout, label_layout)
    results.update(eval_step(model, images, labels, eval_metrics))

  for metric_name, metric in eval_metrics.items():
    results[metric_name] = metric.result()

  for metric_name, metric in results.items():
    print(f"{metric_name}: {metric.numpy()}")

class SubclassedModel(tf.keras.Model):

  def __init__(self, name=None):
    super().__init__(name=name)
    self.feature = tf.keras.layers.Dense(16)
    self.feature_2 = tf.keras.layers.Dense(24)
    self.dropout = tf.keras.layers.Dropout(0.1)

  def call(self, inputs, training=None):
    x = self.feature(inputs)
    x = self.dropout(x, training=training)
    return self.feature_2(x)

layout_map = tf.keras.dtensor.experimental.LayoutMap(mesh=mesh)

layout_map['feature.*kernel'] = dtensor.Layout.batch_sharded(mesh, 'batch', rank=2)
layout_map['feature.*bias'] = dtensor.Layout.batch_sharded(mesh, 'batch', rank=1)

with tf.keras.dtensor.experimental.layout_map_scope(layout_map):
  subclassed_model = SubclassedModel()
dtensor_input = dtensor.copy_to_mesh(tf.zeros((16, 16)), layout=unsharded_layout_2d)
# Trigger the weights creation for subclass model
subclassed_model(dtensor_input)

print(subclassed_model.feature.kernel.layout)

layout_map = tf.keras.dtensor.experimental.LayoutMap(mesh=mesh)

layout_map['feature.*kernel'] = dtensor.Layout.batch_sharded(mesh, 'batch', rank=2)
layout_map['feature.*bias'] = dtensor.Layout.batch_sharded(mesh, 'batch', rank=1)

with tf.keras.dtensor.experimental.layout_map_scope(layout_map):
  inputs = tf.keras.Input((16,), batch_size=16)
  x = tf.keras.layers.Dense(16, name='feature')(inputs)
  x = tf.keras.layers.Dropout(0.1)(x)
  output = tf.keras.layers.Dense(32, name='feature_2')(x)
  model = tf.keras.Model(inputs, output)

print(model.layers[1].kernel.layout)

with tf.keras.dtensor.experimental.layout_map_scope(layout_map):
  model = tf.keras.Sequential([
      tf.keras.layers.Dense(16, name='feature', input_shape=(16,)),
      tf.keras.layers.Dropout(0.1),
      tf.keras.layers.Dense(32, name='feature_2')
  ])

print(model.layers[2].kernel.layout)

