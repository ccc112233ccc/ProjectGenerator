import os
import json

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load configuration
config_path = os.path.join(script_dir, 'config.json')
with open(config_path, 'r') as f:
    config = json.load(f)

# Set backend
os.environ["DDE_BACKEND"] = config['BACKEND']['type']

import deepxde as dde
import numpy as np

# Load dataset
train_x_path = config['DATASET']['train_x']
train_y_path = config['DATASET']['train_y']
test_x_path = config['DATASET']['test_x']
test_y_path = config['DATASET']['test_y']

d1 = np.loadtxt(train_x_path, delimiter=',', dtype='float32')
d2 = np.loadtxt(train_y_path, delimiter=',', dtype='float32')
d3 = np.loadtxt(test_x_path, delimiter=',', dtype='float32')
d4 = np.loadtxt(test_y_path, delimiter=',', dtype='float32')

x1 = d1[:, 0:4].astype('float32')
x2 = d1[:, 4:5].astype('float32')
x3 = d3[:, 0:4].astype('float32')
x4 = d3[:, 4:5].astype('float32')
y = d2[:, 1:2].astype('float32')
y2 = d4[:, 1:2].astype('float32')

maxx1 = np.array(config['NORMALIZATION']['maxx1'], dtype='float32')
minx1 = np.array(config['NORMALIZATION']['minx1'], dtype='float32')
maxx2 = np.float32(config['NORMALIZATION']['maxx2'])
minx2 = np.float32(config['NORMALIZATION']['minx2'])

x1 = (x1 - minx1) / (maxx1 - minx1) * 2 - 1
x2 = (x2 - minx2) / (maxx2 - minx2) * 2 - 1
x3 = (x3 - minx1) / (maxx1 - minx1) * 2 - 1
x4 = (x4 - minx2) / (maxx2 - minx2) * 2 - 1
y = y * 2 - 1
y2 = y2 * 2 - 1

X_train = (x1, x2)
y_train = y
X_test = (x3, x4)
y_test = y2

### this part is from the demo of DeepXDE
data = dde.data.Triple(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test)
m = 4
dim_x = 1
net = dde.nn.DeepONet(
    [m, 300, 300, 300, 300],
    [dim_x, 300, 300, 300, 300],
    "relu",
    "Glorot normal",
)
# Define a Model
model = dde.Model(data, net)
# Compile and Train
model.compile("adam", lr=0.001, loss='MSE')
##############################################
model_path = config['MODEL']['path']
train = config['TRAINING']['train']
iterations = config['TRAINING']['iterations']
display_every = config['TRAINING']['display_every']
batch_size = config['TRAINING']['batch_size']

if train:
    losshistory, train_state = model.train(iterations=iterations, display_every=display_every, batch_size=batch_size)
    # Plot the loss trajectory
    dde.utils.plot_loss_history(losshistory)
    model.save(model_path, protocol="backend")
else:
    model.restore(model_path + '-30000.pt')

xx = model.predict(X_test)
l1 = np.linalg.norm(xx - y_test, ord=2) / np.linalg.norm(y_test, ord=2)
er = xx - y_test
i = np.argmax(er)
print('relative error:')
print(l1)