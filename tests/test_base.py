import os
import shutil
import unittest
from logging import Logger

from uncertainpy.base import Base, ParameterBase
from uncertainpy import NestModel, SpikingFeatures, GeneralFeatures, Parameters

from testing_classes import TestingFeatures, model_function
from testing_classes import TestingModel1d


class TestBase(unittest.TestCase):
    def setUp(self):
        self.output_test_dir = ".tests/"
        self.filename = os.path.join(self.output_test_dir, "output")

        if os.path.isdir(self.output_test_dir):
            shutil.rmtree(self.output_test_dir)
        os.makedirs(self.output_test_dir)


    def tearDown(self):
        if os.path.isdir(self.output_test_dir):
            shutil.rmtree(self.output_test_dir)


    def test_init(self):
        base = Base(model=model_function,
                    base_model=NestModel,
                    features=model_function,
                    base_features=GeneralFeatures,
                    verbose_level="warning",
                    verbose_filename=self.filename)

        self.assertIsInstance(base.model, NestModel)
        self.assertEqual(base.model.run, model_function)

        self.assertIsInstance(base.features, GeneralFeatures)
        self.assertEqual(base.features.features_to_run, ["model_function"])

        self.assertIsInstance(base.logger, Logger)


    def test_feature(self):
        base = Base()

        base.features = TestingFeatures()
        self.assertIsInstance(base._features, TestingFeatures)
        self.assertIsInstance(base.features, TestingFeatures)

        base.features = None
        self.assertIsInstance(base._features, GeneralFeatures)
        self.assertIsInstance(base.features, GeneralFeatures)
        self.assertEqual(base.features.features_to_run, [])


    def test_set_model(self):
        base = Base()
        base.model = TestingModel1d()

        self.assertIsInstance(base.model, TestingModel1d)
        self.assertIsInstance(base._model, TestingModel1d)
        self.assertEqual(base.model.name, "TestingModel1d")

        base = Base(base_model=NestModel)
        base.model = model_function

        self.assertIsInstance(base.model, NestModel)
        self.assertIsInstance(base._model, NestModel)
        self.assertEqual(base.model.run, model_function)
        self.assertEqual(base.model.name, "model_function")

        with self.assertRaises(TypeError):
            base.model = ["list"]



class TestParameterBase(unittest.TestCase):
    def test_init(self):
        parameterlist = [["a", 1, None],
                         ["b", 2, None]]

        base = ParameterBase(parameters=parameterlist,
                             model=model_function,
                             base_model=NestModel,
                             features=model_function,
                             base_features=GeneralFeatures)

        self.assertIsInstance(base.model, NestModel)
        self.assertEqual(base.model.run, model_function)

        self.assertIsInstance(base.features, GeneralFeatures)
        self.assertEqual(base.features.features_to_run, ["model_function"])

        self.assertIsInstance(base.parameters, Parameters)
        self.assertEqual(base.parameters["a"].value, 1)
        self.assertEqual(base.parameters["b"].value, 2)


    def test_set_parameters(self):
        base = ParameterBase()

        parameterlist = [["a", 1, None],
                         ["b", 2, None]]

        base.parameters = parameterlist

        self.assertIsInstance(base.parameters, Parameters)
        self.assertEqual(base.parameters["a"].value, 1)
        self.assertEqual(base.parameters["b"].value, 2)

        parameterlist = [["a", 1, None],
                         ["b", 2, None]]


        base.parameters = Parameters(parameterlist)

        self.assertIsInstance(base.parameters, Parameters)
        self.assertEqual(base.parameters["a"].value, 1)
        self.assertEqual(base.parameters["b"].value, 2)