#!/usr/bin/python
"""
Deep Learning for Cancer Therapy

Authors:
Kumud Ravisankaran | Valeria Brewer
Ninad Mehta | Suraj Jena

A custom TensorFlow Estimator for a DNNClassifier for mutation classification.

This code runs in correlation with ./dataProcessor.py, overseen by ./__main__.py
"""
# REVIEW Do Not Run
#=======================================================

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from typings.arguments import Arguments
from typings.state import State
from typings.run import Run
from typings.features import Features
from typings.settings import Settings
from typings.network import Network
import argparse
import tensorflow as tf
# from dataProcessor import DataProcessor


#/v1/: ALL
#/v1/arguments: learningRate, activation, regularization, regularizationRate, problemType
#/v1/state: numHiddenLayers, networkShape, noise, batchSize, percTrainData
#/v1/run: reset, play, nextButton, showTestData, discretize
#/v1/settings: dataset, weights
#/v1/features: features

"""
    This function checks whether there has been changes

    To determine whether a change has been made:
        compare value stored in ../v1/ to the value in ../v1/xxxx/

    When a value is changed in the playground, ../v1/xxxx/ is updated.
    However, ../v1/ is not changed at this time and so is the two tables
    do not match, then we know that there has been a change.
"""

class DNNClassifierModel:

    network = None

    def __init__(self):
        self.network = Network()

    #REVIEW Verify functions are correct

    def learningRateCallback(self, args):
        self.network.arguments.learningRate = args

        return self.network.arguments.learningRate

    def activationCallback(self, args):
        self.network.arguments.activation = args

        return self.network.arguments.activation

    def regularizationCallback(self, args):
        self.network.arguments.regularization = args

        return self.network.arguments.regularization

    def regularizationRateCallback(self, args):
        self.network.arguments.regularizationRate = args

        return self.network.arguments.regularizationRate

    def problemTypeCallback(self, args):
        self.network.arguments.problemType = args

        return self.network.arguments.problemType

    def batchSizeCallback(self, args):
        self.network.state.batchSize = args

        return self.network.state.batchSize

    def noiseCallback(self, args):
        self.network.state.noise = args

        return self.network.state.noisels

    def trainToTestRatioCallback(self, args):
        self.network.state.trainToTestRatio = args

        return self.network.state.trainToTestRatio

    def numHiddenLayersCallback(self, args):
        self.network.state.numHiddenLayers = args

        return self.network.state.numHiddenLayers

    def networkShapeCallback(self, args):
        self.network.state.networkShape = args

        return self.network.state.networkShape

    def resetCallback(self, args):
        self.network.run.reset = args

        return self.network.run.reset

    def playCallback(self, args):
        self.network.run.play = args

        return self.network.run.play

    def nextButtonCallback(self, args):
        self.network.run.nextButton = args

        return self.network.run.nextButton

    def showTestDataCallback(self, args):
        self.network.run.showTestData = args

        return self.network.run.showTestData

    def discretizeCallback(self, args):
        self.network.run.discretize = args

        return self.network.run.discretize

    def featuresCallback(self, args):
        self.network.features.features = args

        return self.network.features.features

    def datasetCallback(self, args):
        self.network.settings.dataset = args

        return self.network.settings.dataset

    def weightsCallback(self, args):
        self.network.settings.weights = args

        return self.network.settings.weights

    #REVIEW Verify if each and every line of routine lines up with our dataset requirements
    #TODO Adjust model for our particular inputs after redefining and designing neural net
    #XXX Priority 2
    def classifierModel(self, features, labels, mode, params):
        """
        NAME: classifierModel (dnnClassifier)
        INPUTS: (features: dictionary) - A mapping from key to tensors, the key being the type of feature e.g. '5a'
                    (labels: list) - A list containing all the labels
                    (mode: object) - Defines the model's operation - TRAIN, PREDICT, or EVALUATE
                    (params: dictionary) - dict for additional configuration; in this case contains
                                                    (feature_columns: list) - A list of tf.feature_column.numeric_columns
                                                    (hidden_units: list) - A list containing the number of neurons in each hidden_layer, indexed by layer index
                                                    (n_classes: Integer) - The model must choose between these many classes
                    RETURN: (tf.estimator.EstimatorSpec: object) - A different EstimatorSpec depending on the kind of ModeKeys
                    PURPOSE: This routine defines a Deep Neural Network [DNN] Classifier Model with 2 Hidden Layers
                        The purpose of this routine is to perform the appropriate function on the provided features:
                        If mode is TRAIN :- train the model on the provided input data in features, compute loss and training_op,
                                                    and return an EstimatorSpec(tf.estimator.ModeKeys.TRAIN, loss, train_op).
                        If mode is PREDICT :- compute the predictions on the provided data, which comes without labels,
                                                    store them in a dict() 'predictions' containing keys('class_ids', 'probabilities', 'logits'
                                                    and return an EstimatorSpec(tf.estimator.ModeKeys.PREDICT, predictions).
                                If mode is EVALUATE :- compute the evaluation metrics, the necessary ones chosen in the model_fn,
                                                    and return an EstimatorSpec(tf.estimator.ModeKeys.EVALUATE, loss, eval_metric_ops).
    """

        global stateObjStatus

        # returns a dense Tensor as the input layer based on provided feature_columns
        net = tf.feature_column.input_layer(features, params['feature_columns'])

        stateObjStatus = False

        for units in range(0, self.network.state.numHiddenLayers): #params['hidden_units']:
            # units is the number of output neurons in a layer
            net = tf.layers.dense(net, units=self.network.state.numHiddenLayers[units], activation=self.network.arguments.activation) # Using the ReLu activation function
            # net signifies input layer during first iteration - when new layer is created, previous layers -
            # output is in net

        # Compute logits (one per class)
        # No activation function defines this as the output layer
        logits = tf.layers.dense(net, params['n_classes'], activation=None)

        # predict() section of the model
        # Compute the predictions below
        predicted_classes = tf.argmax(logits, 1)
        # ModeKeys in tf.estimator defines the mode, which has PREDICT as one mode
        if mode == tf.estimator.ModeKeys.PREDICT:
            # Create a predictions dict to store class ids and probabilities, and also the logits
            predictions = {
                'class_ids' : predicted_classes[:, tf.newaxis],
                'probabilities' : tf.nn.softmax(logits),
                'logits' : logits,
            }
            # Return an EstimatorSpec with the mode as PREDICT and the predictions dict
            return tf.estimator.EstimatorSpec(mode, predictions=predictions)

        # Compute the loss
        #labels contains the ground truths, and logits are the logits calculated from earlier
        loss = tf.losses_sparse_softmax_cross_entropy(labels=labels, logits=logits)

        # Compute the evaluation metrics, if any - only accuracy added here
        # Need metrics to print additional material on TensorBoard
        accuracy = tf.metrics.accuracy(labels=labels,
                                                        predictions=predicted_classes,
                                                        name='acc_op')
        metrics = {'accuracy' : accuracy}
        # scalar will make accuracy available to TensorBoard in both TRAIN and EVAL modes
        tf.summary.scalar('accuracy', accuracy[1])

            # Entering evaluate() mode
        if mode == tf.estimator.ModeKeys.EVAL:
            # Evaluate mode simply returns an EstimatorSpec with the mode, loss and metrics
            return tf.estimator.EstimatorSpec(mode, loss=loss, eval_metric_ops=metrics)

        # Create training operation returned by the TRAIN mode call
        # ensure mode is TRAIN
        assert mode == tf.estimator.ModeKeys.TRAIN
        # Write a call to an optimizer function - using the Adagrad Gradient Descent Optimizer here
        optimizer = tf.train.AdagradOptimizer
        # The actual training operation, which makes use of the optimizer and gets a result
        # global_step keeps a record of the overall training steps taken (to know when to end)
        train_op = optimizer.minimize(loss, global_step=tf.train.get_global_step())

        # Only when in TRAIN mode, model returns an EstimatorSpec containing the mode, loss and
        # the training operation defined above
        return tf.estimator.EstimatorSpec(mode, loss=loss, train_op=train_op)

    def start():
        # TODO
        # Fetch the data from the dataset  - done by load_data() in ./dataProcessor.py
        #   (train_x, train_y), (test_x, test_y) = dataProcessor.load_data()

        feature_columns = []
        # for each key in the train_x dictionary
        #REVIEW after data loads successfully
        for key in train_x.keys():
            # append a numeric feature column to the list, with key same as the training set key
            feature_columns.append(tf.feature_column.numeric_column(key=key))

        # Build DNN with 2 hidden layers, and 10, 10 units respectively (for each layer) [units are the number of output neurons]
        # take hidden_units from DNNClassifierModel which checks for changes in networkShape
        # May need to *wait* for DNNClassifierModel.networkShape() to return with value
        classifier = tf.estimator.Estimator(
            model_fn=classifierModel,
            params={ #NOTE Unsure about hidden_units. Find a way to integrate networkShape here (hiddenLayers with the hiddenUnits)
                # Send the feature columns in params
                'feature_columns' : feature_columns,
                # Enter hidden layer units, 2 of X nodes each [used 10 as a placeholder]
                'hidden_units' : self.network.state.networkShape,
                # The model must choose between X classes
                'n_classes' : 2,
            }
        )

        # Train the model
        # Provide a lambda function to the train method for the actual input function with (features, labels, batch_size)
        # Take batch size from DNNClassifierModel which checks for changes in value
        # May need to *wait* for DNNClassifierModel.batchSize() to return with value
        classifier.train(
            input_fn=lambda:dataProcessor.train_input_fn(train_x, train_y, self.network.state.batchSize),
            steps=self.network.arguments.learningRate) #learningRate yet to be integrated with gradient descent

        # Evaluate the model
        # Provide a lambda function to the evaluate function of the classifier, which is dataProcessor's eval input print_function
        # Basically above 2 methods are wrappers for the original, our train/eval_input_fn from dataProcessor
        eval_result = classifier.evaluate(input_fn=lambda:dataProcessor.train_input_fn(train_k))

        print('\nTest set accuracy: {accuracy:0.3f}\n'.format(**eval_result))

        # Generate Predictions from the model
        # expected holds the expected classes to be classified into
        expected = ['Melanoma', 'Lung Adeno']
        # Predict x holds the test data to be used to display results after the model has been trained and evaluated
        predict_x = {
            'mutation' : [5, 3, 1],
            'fivea' : [3, 2, 4],
            'fivet' : [2, 1, 3],
            'threea' : [2, 4, 1],
            'threet' : [1, 4, 2]
        }

        # The same function as evaluate calls through it's lambda, eval_input_fn from dataProcessor.py is called here
        # But in predict mode - that function handles two modes, predict and evaluate
        # This takes predict_x as it's labels if no labels are provided, and
        predictions = classifier.predict(
            input_fn=lambda:iris_data.eval_input_fn(predict_x, labels = None, batch_size=self.network.state.batchSize))

        # Loop through the tuple list of (predictions, expected) which holds the predictions for each ith value in all 3 columns
        # of the predict_x dict, giving predictions for those sample values after the model has been trained and evaluated (i.e. "learned")
        for pred_dict, expec in zip(predictions, expected):
            # prints the predictions
            template = ('\nPrediction is "{}" ({:.1f}%), expected "{}"')
            # class_id of the prediction
            class_id = pred_dict['class_ids'][0]
            # Prediction probability of the class id selected above - the prediction
            probability = pred_dict['probabilities'][class_id]
            # print the correct answer's label, it's probability scaled into a percentage, and the expected class from the list
            print(template.format(dataProcessor.TUMOR[class_id],
                                  100 * probability, expec))
