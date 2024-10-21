import os
import argparse


class InferenceArgsParser:
    def __init__(self):
        parser = argparse.ArgumentParser('Info-Args-Parser', add_help=False)
        # Basic Training and Inference Setting
        parser.add_argument('--debug', default=False, type=bool)
        self.args_parser = parser

    def extract_args(self, args_map):
        parser = argparse.ArgumentParser('Info-Args-Parser', parents=[self.args_parser])
        args = parser.parse_args()
        if not args_map:
            return args

        debug = "debug".upper()
        if debug in args_map:
            args.debug = args_map[debug].upper() == 'TRUE'

        return args


class ModelPredict:

    def __init__(self, inputs_folder, outputs_folder, model_folder):
        self.inputs_folder = inputs_folder
        self.outputs_folder = outputs_folder
        self.model_folder = model_folder
        self.args_parser = InferenceArgsParser()

    def predict(self, args_map):
        print('load input from {0}'.format(self.inputs_folder))
        args = self.args_parser.extract_args(args_map)
        print(args.debug)
        # codes of algorithm
        print('predict')
        # codes of algorithm

        print('save result in {0}'.format(self.outputs_folder))
