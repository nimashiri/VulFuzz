import tensorflow as tf
from struct import Struct
# Data size on the solution u
N_u = 50
# Collocation points size, where we’ll check for f = 0
N_f = 10000
# DeepNN topology (2-sized input [x t], 8 hidden layer of 20-width, 1-sized output [u]
layers = [2, 20, 20, 20, 20, 20, 20, 20, 20, 1]
# Setting up the TF SGD-based optimizer (set tf_epochs=0 to cancel it)
tf_epochs = 100
tf_optimizer = tf.keras.optimizers.Adam(
  learning_rate=0.1,
  beta_1=0.99,
  epsilon=1e-1)
# Setting up the quasi-newton LBGFS optimizer (set nt_epochs=0 to cancel it)
nt_epochs = 2000
nt_config = Struct()
nt_config.learningRate = 0.8
nt_config.maxIter = nt_epochs
nt_config.nCorrection = 50
nt_config.tolFun = 1.0 * np.finfo(float).eps

# Getting the data
path = os.path.join(appDataPath, "burgers_shock.mat")
x, t, X, T, Exact_u, X_star, u_star, \
  X_u_train, u_train, X_f, ub, lb = prep_data(path, N_u, N_f, noise=0.0)

# Creating the model and training
logger = Logger(frequency=10)
pinn = PhysicsInformedNN(layers, tf_optimizer, logger, X_f, ub, lb, nu=0.01/np.pi)
def error():
  u_pred, _ = pinn.predict(X_star)
  return np.linalg.norm(u_star - u_pred, 2) / np.linalg.norm(u_star, 2)
logger.set_error_fn(error)
pinn.fit(X_u_train, u_train, tf_epochs, nt_config)

# Getting the model predictions, from the same (x,t) that the predictions were previously gotten from
u_pred, f_pred = pinn.predict(X_star)

plot_inf_cont_results(X_star, u_pred.numpy().flatten(), X_u_train, u_train,
  Exact_u, X, T, x, t)


# Setup
lb = np.array([-1.0])
ub = np.array([1.0])
idx_t_0 = 10
idx_t_1 = 90
nu = 0.01/np.pi

# Getting the data
path = os.path.join(appDataPath, "burgers_shock.mat")
x, t, dt, \
  Exact_u, x_0, u_0, x_1, x_star, u_star, \
  IRK_weights, IRK_times = prep_data(path, N_n=N_n, q=q, lb=lb, ub=ub, noise=0.0, idx_t_0=idx_t_0, idx_t_1=idx_t_1)

# Creating the model and training
logger = Logger(frequency=10)
pinn = PhysicsInformedNN(layers, tf_optimizer, logger, dt, x_1, lb, ub, nu, q, IRK_weights, IRK_times)
def error():
  u_pred = pinn.predict(x_star)
  return np.linalg.norm(u_pred - u_star, 2) / np.linalg.norm(u_star, 2)
logger.set_error_fn(error)
pinn.fit(x_0, u_0, tf_epochs, nt_config)

# Getting the model predictions, from the same (x,t) that the predictions were previously gotten from
u_1_pred = pinn.predict(x_star)


# Getting the model predictions, from the same (x,t) that the predictions were previously gotten from
u_1_pred = pinn.predict(x_star)


plot_inf_disc_results(x_star, idx_t_0, idx_t_1, x_0, u_0, ub, lb, u_1_pred, Exact_u, x, t)

# Getting the data
path = os.path.join(appDataPath, "burgers_shock.mat")
x, t, X, T, Exact_u, X_star, u_star, \
  X_u_train, u_train, ub, lb = prep_data(path, N_u, noise=0.0)
lambdas_star = (1.0, 0.01/np.pi)

# Creating the model and training
logger = Logger(frequency=10)
pinn = PhysicsInformedNN(layers, tf_optimizer, logger, ub, lb)
def error():
  l1, l2 = pinn.get_params(numpy=True)
  l1_star, l2_star = lambdas_star
  error_lambda_1 = np.abs(l1 - l1_star) / l1_star
  error_lambda_2 = np.abs(l2 - l2_star) / l2_star
  return (error_lambda_1 + error_lambda_2) / 2
logger.set_error_fn(error)
pinn.fit(X_u_train, u_train, tf_epochs, nt_config)

# Getting the model predictions, from the same (x,t) that the predictions were previously gotten from
u_pred, f_pred = pinn.predict(X_star)
lambda_1_pred, lambda_2_pred = pinn.get_params(numpy=True)

# Noise case
x, t, X, T, Exact_u, X_star, u_star, \
  X_u_train, u_train, ub, lb = prep_data(path, N_u, noise=0.01)
pinn = PhysicsInformedNN(layers, tf_optimizer, logger, ub, lb)
pinn.fit(X_u_train, u_train, tf_epochs, nt_config)
lambda_1_pred_noise, lambda_2_pred_noise = pinn.get_params(numpy=True)

print("l1: ", lambda_1_pred)
print("l2: ", lambda_2_pred)
print("l1_noise: ", lambda_1_pred_noise)
print("l2_noise: ", lambda_2_pred_noise)

plot_ide_cont_results(X_star, u_pred, X_u_train, u_train,
  Exact_u, X, T, x, t, lambda_1_pred, lambda_1_pred_noise, lambda_2_pred, lambda_2_pred_noise)

# Setup
lb = np.array([-1.0])
ub = np.array([1.0])
idx_t_0 = 10
skip = 80
idx_t_1 = idx_t_0 + skip

# Getting the data
path = os.path.join(appDataPath, "burgers_shock.mat")
x_0, u_0, x_1, u_1, x_star, t_star, dt, q, \
  Exact_u, IRK_alpha, IRK_beta = prep_data(path, N_0=N_0, N_1=N_1,
  lb=lb, ub=ub, noise=0.0, idx_t_0=idx_t_0, idx_t_1=idx_t_1)
lambdas_star = (1.0, 0.01/np.pi)

# Setting the output layer dynamically
layers[-1] = q
 
# Creating the model and training
logger = Logger(frequency=10)
pinn = PhysicsInformedNN(layers, tf_optimizer, logger, dt, lb, ub, q, IRK_alpha, IRK_beta)
def error():
  l1, l2 = pinn.get_params(numpy=True)
  l1_star, l2_star = lambdas_star
  error_lambda_1 = np.abs(l1 - l1_star) / l1_star
  error_lambda_2 = np.abs(l2 - l2_star) / l2_star
  return (error_lambda_1 + error_lambda_2) / 2
logger.set_error_fn(error)
pinn.fit(x_0, u_0, x_1, u_1, tf_epochs)

# Getting the model predictions
U_0_pred, U_1_pred = pinn.predict(x_star)
lambda_1_pred, lambda_2_pred = pinn.get_params(numpy=True)

# Noisy case (same as before with a different noise)
x_0, u_0, x_1, u_1, x_star, t_star, dt, q, \
  Exact_u, IRK_alpha, IRK_beta = prep_data(path, N_0=N_0, N_1=N_1,
  lb=lb, ub=ub, noise=0.01, idx_t_0=idx_t_0, idx_t_1=idx_t_1)
layers[-1] = q
pinn = PhysicsInformedNN(layers, tf_optimizer, logger, dt, lb, ub, q, IRK_alpha, IRK_beta)
pinn.fit(x_0, u_0, x_1, u_1, tf_epochs)
U_0_pred, U_1_pred = pinn.predict(x_star)
lambda_1_pred_noisy, lambda_2_pred_noisy = pinn.get_params(numpy=True)

print("l1: ", lambda_1_pred)
print("l2: ", lambda_2_pred)
print("noisy l1: ", lambda_1_pred_noisy)
print("noisy l2: ", lambda_2_pred_noisy)

plot_ide_disc_results(x_star, t_star, idx_t_0, idx_t_1, x_0, u_0, x_1, u_1,
  ub, lb, U_1_pred, Exact_u, lambda_1_pred, lambda_1_pred_noisy, lambda_2_pred, lambda_2_pred_noisy, x_star, t_star)
