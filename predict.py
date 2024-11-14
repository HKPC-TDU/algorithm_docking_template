import os
import json
import argparse


class InferenceArgsParser:
    def __init__(self):
        parser = argparse.ArgumentParser('Info-Args-Parser', add_help=False)
        # Basic Training and Inference Setting
        parser.add_argument('--debug', default=False, type=bool)
        parser.add_argument('--is_output_boundbox', default=True, type=bool)
        parser.add_argument('--is_output_labels', default=False, type=bool)
        self.args_parser = parser

    def extract_args(self, args_map):
        parser = argparse.ArgumentParser('Info-Args-Parser', parents=[self.args_parser])
        args = parser.parse_args()
        if not args_map:
            return args

        debug = "debug".upper()
        if debug in args_map:
            args.debug = args_map[debug].upper() == 'TRUE'

        key_is_output_boundbox = "is_output_boundbox".upper()
        if key_is_output_boundbox in args_map:
            args.is_output_boundbox = args_map[key_is_output_boundbox].upper() == 'TRUE'

        is_output_labels = "is_output_labels".upper()
        if is_output_labels in args_map:
            args.is_output_labels = args_map[is_output_labels].upper() == 'TRUE'

        return args


class ModelPredict:

    def __init__(self, inputs_folder, outputs_folder, model_folder):
        self.inputs_folder = inputs_folder
        self.outputs_folder = outputs_folder
        self.model_folder = model_folder
        self.inference_label_file_name = 'labels.json'
        self.args_parser = InferenceArgsParser()

    def predict(self, args_map):
        print('load input from {0}'.format(self.inputs_folder))
        args = self.args_parser.extract_args(args_map)
        print(args.debug)

        labels = self._inference(args)

        if args.is_output_labels:
            self._generate_output_json(labels)

        print('save result in {0}'.format(self.outputs_folder))

    def _inference(self, args):
        # codes of algorithm
        print('predict')
        # codes of algorithm
        return []

    def get_output_json_path(self):
        return os.path.join(self.outputs_folder, self.inference_label_file_name)

    def _generate_output_json(self, output_labels):
        output_labels_file = os.path.join(self.outputs_folder, self.inference_label_file_name)
        with open(output_labels_file, 'w') as output_file:
            json.dump(output_labels, output_file, indent=4)
