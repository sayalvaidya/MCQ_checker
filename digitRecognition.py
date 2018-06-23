from __future__ import division
import numpy
import scipy.special
from os.path import join, dirname, realpath

UPLOAD_FOLDER_TRAINED_DATA = join(dirname(realpath(__file__)), 'static/trainedData/')
UPLOAD_FOLDER_CHARACTER_CSV = join(dirname(realpath(__file__)), 'static/characterCsv/')


class NeuralNetwork:
    def __init__(self, input_nodes, hidden_nodes, output_nodes, learning_rate):
        # number of input nodes
        self.input_nodes = input_nodes
        # number of hidden nodes
        self.hidden_nodes = hidden_nodes
        # number of output nodes
        self.output_nodes = output_nodes
        # learning rate
        self.lr = learning_rate

        self.weight_input_hidden = numpy.genfromtxt(UPLOAD_FOLDER_TRAINED_DATA + 'input_to_hidden.csv', delimiter=',')

        self.weight_hidden_output = numpy.genfromtxt(UPLOAD_FOLDER_TRAINED_DATA + 'hidden_to_output.csv', delimiter=',')

        # sigmoid function
        self.activation_function = lambda x: scipy.special.expit(x)

    def predict(self, inputs_list):
        # convert input list to 2d array
        inputs = numpy.array(inputs_list, ndmin=2).T

        # inputs to hidden layer
        hidden_inputs = numpy.dot(self.weight_input_hidden, inputs)

        # outputs from the hidden layer
        hidden_outputs = self.activation_function(hidden_inputs)

        # inputs to output layer
        final_inputs = numpy.dot(self.weight_hidden_output, hidden_outputs)

        # outputs from the output layer
        final_outputs = self.activation_function(final_inputs)

        return final_outputs


def recognize_single_character(rec_csv):
    input_nodes = 1024
    hidden_nodes = 300
    output_nodes = 15
    learning_rate = 0.08

    neural = NeuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)

    print("Single data")
    test_data = open(UPLOAD_FOLDER_CHARACTER_CSV + rec_csv, 'r')
    test_list = test_data.readlines()
    test_data.close()

    for record in test_list:
        all_values = record.split(',')
        inputs = (numpy.asfarray(all_values[0:]) / 255 * 0.99) + 0.01
        outputs = neural.predict(inputs)
        label = numpy.argmax(outputs)
        print(label)
        if label == 0:
            return '0'
        if label == 1:
            return '1'
        if label == 2:
            return '2'
        if label == 3:
            return '3'
        if label == 4:
            return '4'
        if label == 5:
            return '5'
        if label == 6:
            return '6'
        if label == 7:
            return '7'
        if label == 8:
            return '8'
        if label == 9:
            return '9'
        if label == 10:
            return 'A'
        if label == 11:
            return 'B'
        if label == 12:
            return 'C'
        if label == 13:
            return 'D'
        if label == 14:
            return 'E'
        else:
            return label
