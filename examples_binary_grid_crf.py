import numpy as np
import matplotlib.pyplot as plt

from crf import BinaryGridCRF
#from structured_perceptron import StructuredPerceptron
from structured_svm import StructuredSVM
#from structured_svm import SubgradientStructuredSVM
from examples_latent_crf import make_dataset_easy_latent

from IPython.core.debugger import Tracer
tracer = Tracer()


def make_dataset_blocks():
    Y = np.ones((20, 10, 12))
    Y[:, :, :6] = -1
    X = Y + 1.5 * np.random.normal(size=Y.shape)
    X = np.c_['3,4,0', X, -X]
    Y = (Y > 0).astype(np.int32)
    return X, Y


def make_dataset_checker(n_samples=20):
    np.random.seed(0)
    Y = np.ones((n_samples, 11, 13))
    Y[:, ::2, ::2] = -1
    Y[:, 1::2, 1::2] = -1
    X = Y + 1.5 * np.random.normal(size=Y.shape)
    X = np.c_['3,4,0', X, -X]
    Y = (Y > 0).astype(np.int32)
    return X, Y


def make_dataset_big_checker(n_samples=20):
    np.random.seed(0)
    Y_small = np.ones((n_samples, 11, 13))
    Y_small[:, ::2, ::2] = -1
    Y_small[:, 1::2, 1::2] = -1
    Y = Y_small.repeat(3, axis=1).repeat(3, axis=2)
    X = Y + 0.5 * np.random.normal(size=Y.shape)
    Y = (Y > 0).astype(np.int32)
    X = np.c_['3,4,0', X, -X]
    return X, Y


def main():
    #X, Y = make_dataset_blocks()
    #X, Y = make_dataset_checker()
    X, Y = make_dataset_easy_latent(n_samples=10)
    #X, Y = make_dataset_big_checker()
    crf = BinaryGridCRF()
    #clf = StructuredPerceptron(problem=crf, max_iter=100)
    clf = StructuredSVM(problem=crf, max_iter=200, C=100, verbose=0,
            check_constraints=False)
    #clf = SubgradientStructuredSVM(problem=crf, max_iter=2000, C=100)
    clf.fit(X, Y)
    Y_pred = clf.predict(X)
    i = 0
    loss = 0
    for x, y, y_pred in zip(X, Y, Y_pred):
        loss += np.sum(y != y_pred)
        plt.subplot(221)
        plt.imshow(x[:, :, 0], interpolation='nearest')
        plt.subplot(222)
        plt.imshow(y, interpolation='nearest')
        plt.subplot(223)
        plt.imshow(x[:, :, 0] > 0, interpolation='nearest')
        plt.subplot(224)
        plt.imshow(y_pred, interpolation='nearest')
        plt.savefig("data_%03d.png" % i)
        plt.close()
        i += 1
    print("loss: %f" % loss)

if __name__ == "__main__":
    main()
