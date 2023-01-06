from builtins import object
import numpy as np

from ..layers import *
from ..fast_layers import *
from ..layer_utils import *


class ThreeLayerConvNet(object):
    """
    A three-layer convolutional network with the following architecture:

    conv - relu - 2x2 max pool - affine - relu - affine - softmax

    The network operates on minibatches of data that have shape (N, C, H, W)
    consisting of N images, each with height H and width W and with C input
    channels.
    """

    def __init__(
        self,
        input_dim=(3, 32, 32),
        num_filters=32,
        filter_size=7,
        hidden_dim=100,
        num_classes=10,
        weight_scale=1e-3,
        reg=0.0,
        dtype=np.float32,
    ):
        """
        Initialize a new network.

        Inputs:
        - input_dim: Tuple (C, H, W) giving size of input data
        - num_filters: Number of filters to use in the convolutional layer
        - filter_size: Width/height of filters to use in the convolutional layer
        - hidden_dim: Number of units to use in the fully-connected hidden layer
        - num_classes: Number of scores to produce from the final affine layer.
        - weight_scale: Scalar giving standard deviation for random initialization
          of weights.
        - reg: Scalar giving L2 regularization strength
        - dtype: numpy datatype to use for computation.
        """
        self.params = {}
        self.reg = reg
        self.dtype = dtype

        ############################################################################
        # TODO: Initialize weights and biases for the three-layer convolutional    #
        # network. Weights should be initialized from a Gaussian centered at 0.0   #
        # with standard deviation equal to weight_scale; biases should be          #
        # initialized to zero. All weights and biases should be stored in the      #
        #  dictionary self.params. Store weights and biases for the convolutional  #
        # layer using the keys 'W1' and 'b1'; use keys 'W2' and 'b2' for the       #
        # weights and biases of the hidden affine layer, and keys 'W3' and 'b3'    #
        # for the weights and biases of the output affine layer.                   #
        #                                                                          #
        # IMPORTANT: For this assignment, you can assume that the padding          #
        # and stride of the first convolutional layer are chosen so that           #
        # **the width and height of the input are preserved**. Take a look at      #
        # the start of the loss() function to see how that happens.                #
        ############################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

        # Initialize Weights and Biases
        C, H, W = input_dim
        self.params['W1'] = weight_scale * np.random.randn(num_filters, C, filter_size, filter_size)
        self.params['b1'] = np.zeros(num_filters)
        # Assuming a shape identical to the input image for the conv layer output
        self.params['W2'] = weight_scale * np.random.randn(num_filters * H * W // 4, hidden_dim)
        self.params['b2'] = np.zeros(hidden_dim)
        self.params['W3'] = weight_scale * np.random.randn(hidden_dim, num_classes)
        self.params['b3'] = np.zeros(num_classes)

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        for k, v in self.params.items():
            self.params[k] = v.astype(dtype)

    def loss(self, X, y=None):
        """
        Evaluate loss and gradient for the three-layer convolutional network.

        Input / output: Same API as TwoLayerNet in fc_net.py.
        """
        W1, b1 = self.params["W1"], self.params["b1"]
        W2, b2 = self.params["W2"], self.params["b2"]
        W3, b3 = self.params["W3"], self.params["b3"]

        # pass conv_param to the forward pass for the convolutional layer
        # Padding and stride chosen to preserve the input spatial size
        filter_size = W1.shape[2]
        conv_param = {"stride": 1, "pad": (filter_size - 1) // 2}

        # pass pool_param to the forward pass for the max-pooling layer
        pool_param = {"pool_height": 2, "pool_width": 2, "stride": 2}

        scores = None
        ############################################################################
        # TODO: Implement the forward pass for the three-layer convolutional net,  #
        # computing the class scores for X and storing them in the scores          #
        # variable.                                                                #
        #                                                                          #
        # Remember you can use the functions defined in annp/fast_layers.py and  #
        # annp/layer_utils.py in your implementation (already imported).         #
        ############################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

        # Forward Pass: conv - relu - 2x2 max pool - affine - relu - affine - softmax
        out1, cache1 = conv_relu_pool_forward(X, W1, b1, conv_param, pool_param)
        out2, cache2 = affine_relu_forward(out1, W2, b2)
        out3, cache3 = affine_forward(out2, W3, b3)
        scores = out3

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        if y is None:
            return scores

        loss, grads = 0, {}
        ############################################################################
        # TODO: Implement the backward pass for the three-layer convolutional net, #
        # storing the loss and gradients in the loss and grads variables. Compute  #
        # data loss using softmax, and make sure that grads[k] holds the gradients #
        # for self.params[k]. Don't forget to add L2 regularization!               #
        #                                                                          #
        # NOTE: To ensure that your implementation matches ours and you pass the   #
        # automated tests, make sure that your L2 regularization includes a factor #
        # of 0.5 to simplify the expression for the gradient.                      #
        ############################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

        loss, dout = softmax_loss(out3, y)
        loss += self.reg * np.sum([np.sum(self.params['W%d' % i] ** 2) for i in [1, 2, 3]])
        dout, grads['W3'], grads['b3'] = affine_backward(dout, cache3)
        grads['W3'] += 2 * self.reg * W3
        dout, grads['W2'], grads['b2'] = affine_relu_backward(dout, cache2)
        grads['W2'] += 2 * self.reg * W2
        _, grads['W1'], grads['b1'] = conv_relu_pool_backward(dout, cache1)
        grads['W1'] += 2 * self.reg * W1

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        return loss, grads




class NewConvNet(object):
    """
    A three-layer convolutional network with the following architecture:

    new: conv - relu
    conv - relu - 2x2 max pool - affine - relu - affine - softmax

    The network operates on minibatches of data that have shape (N, C, H, W)
    consisting of N images, each with height H and width W and with C input
    channels.
    """

    def __init__(
        self,
        input_dim=(3, 32, 32),
        num_filters_1=32,
        num_filters_2=24,
        filter_size_1=7,
        filter_size_2=5,
        hidden_dim=100,
        num_classes=10,
        weight_scale=1e-3,
        reg=0.0,
        dtype=np.float32,
    ):
        """
        Initialize a new network.

        Inputs:
        - input_dim: Tuple (C, H, W) giving size of input data
        - num_filters_1: Number of filters to use in the 0th convolutional layer
        - num_filters_2: Number of filters to use in the 1st convolutional layer
        - filter_size_1: Width/height of filters to use in the 0th convolutional layer
        - filter_size_2: Width/height of filters to use in the 1st convolutional layer
        - hidden_dim: Number of units to use in the fully-connected hidden layer
        - num_classes: Number of scores to produce from the final affine layer.
        - weight_scale: Scalar giving standard deviation for random initialization
          of weights.
        - reg: Scalar giving L2 regularization strength
        - dtype: numpy datatype to use for computation.
        """
        self.params = {}
        self.reg = reg
        self.dtype = dtype

        # Initialize Weights and Biases
        C, H, W = input_dim

        self.params['W0'] = weight_scale * np.random.randn(num_filters_1, C, filter_size_1, filter_size_1)
        self.params['b0'] = np.zeros(num_filters_1)

        self.params['W1'] = weight_scale * np.random.randn(num_filters_2, num_filters_1, filter_size_2, filter_size_2)
        self.params['b1'] = np.zeros(num_filters_2)
        # Assuming a shape identical to the input image for the conv layer output
        self.params['W2'] = weight_scale * np.random.randn(num_filters_2  * H * W // 4, hidden_dim)
        # self.params['W2'] = weight_scale * np.random.randn(num_filters_2 * 256, hidden_dim)
        
        self.params['b2'] = np.zeros(hidden_dim) 
        self.params['W3'] = weight_scale * np.random.randn(hidden_dim, num_classes)
        self.params['b3'] = np.zeros(num_classes)

        for k, v in self.params.items():
            self.params[k] = v.astype(dtype)

    def loss(self, X, y=None):
        """
        Evaluate loss and gradient for the three-layer convolutional network.

        Input / output: Same API as TwoLayerNet in fc_net.py.
        """
        W0, b0 = self.params["W0"], self.params["b0"]
        W1, b1 = self.params["W1"], self.params["b1"]
        W2, b2 = self.params["W2"], self.params["b2"]
        W3, b3 = self.params["W3"], self.params["b3"]

        # pass conv_param to the forward pass for the convolutional layer
        # Padding and stride chosen to preserve the input spatial size
        

        filter_size_1 = W0.shape[2]
        conv_param_1 = {"stride": 1, "pad": (filter_size_1 - 1) // 2}

        filter_size_2 = W1.shape[2]
        conv_param_2 = {"stride": 1, "pad": (filter_size_2 - 1) // 2}

        # pass pool_param to the forward pass for the max-pooling layer
        pool_param_1 = {"pool_height": 1, "pool_width": 1, "stride": 1}
        pool_param_2 = {"pool_height": 2, "pool_width": 2, "stride": 2}

        scores = None

        # Forward Pass:#conv -relu -# conv - relu - 2x2 max pool - affine - relu - affine - softmax
        out0, cache0 = conv_relu_pool_forward(X, W0, b0, conv_param_1, pool_param_1)
        out1, cache1 = conv_relu_pool_forward(out0, W1, b1, conv_param_2, pool_param_2)
        out2, cache2 = affine_relu_forward(out1, W2, b2)
        out3, cache3 = affine_forward(out2, W3, b3)
        scores = out3

        if y is None:
            return scores

        loss, grads = 0, {}

        loss, dout = softmax_loss(out3, y)
        loss += self.reg * np.sum([np.sum(self.params['W%d' % i] ** 2) for i in [0, 1, 2, 3]])
        dout, grads['W3'], grads['b3'] = affine_backward(dout, cache3)
        grads['W3'] += 2 * self.reg * W3
        dout, grads['W2'], grads['b2'] = affine_relu_backward(dout, cache2)
        grads['W2'] += 2 * self.reg * W2
        dout, grads['W1'], grads['b1'] = conv_relu_pool_backward(dout, cache1)
        grads['W1'] += 2 * self.reg * W1
        _, grads['W0'], grads['b0'] = conv_relu_pool_backward(dout, cache0)
        grads['W0'] += 2 * self.reg * W0

        return loss, grads