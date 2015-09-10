# example of Convolutional Auto-encoder with layer visualization

from libdnn import AutoEncoder
import libdnn.visualizer as V
import chainer
import chainer.functions as F
import chainer.optimizers as Opt
import numpy
from sklearn.datasets import fetch_mldata
import matplotlib.pyplot as plt
import matplotlib as mpl


model = chainer.FunctionSet(
    fh1=F.Linear(28 ** 2, 200),
    fh2=F.Linear(200, 28 ** 2),
)


def forward(self, x, train):
    if train:
        F.dropout(x, ratio=0.3)

    h = F.dropout(F.sigmoid(self.model.fh1(x)), train=train)
    h = F.dropout(self.model.fh2(h), train=train)

    return h

ae = AutoEncoder(model, gpu=0)
ae.set_forward(forward)
ae.load_param('./ae.param.npy')

W1 = ae.model['fh1'].W
for i in range(4):
    for n in range(50):
        ax = plt.subplot(8, 7, n + 1)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        plt.imshow(chainer.cuda.to_cpu(W1[i * 50 + n]).reshape(28, 28), interpolation='none', cmap=mpl.cm.gray)
    plt.show()

W2 = ae.model['fh2'].W.T
for i in range(4):
    for n in range(50):
        ax = plt.subplot(8, 7, n + 1)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        plt.imshow(chainer.cuda.to_cpu(W2[i * 50 + n]).reshape(28, 28), interpolation='none', cmap=mpl.cm.gray)
    plt.show()


mnist = fetch_mldata('MNIST original', data_home='.')
perm = numpy.random.permutation(len(mnist.data))
train_data = mnist.data[perm][:60000].astype(numpy.float32) / 255
test_data = mnist.data[perm][60000:].astype(numpy.float32) / 255
for i in range(20):
    y = ae.forward(train_data[i * 20: i * 20 + 25], train=False)
    y = chainer.cuda.to_cpu(y.data)
    for n in range(25):
        ax = plt.subplot(5, 5, n + 1)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        plt.imshow(y[n].reshape(28, 28), interpolation='none', cmap=mpl.cm.gray)
    plt.show()

