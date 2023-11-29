class ModelPredict:

    def __init__(self, inputs_path, outputs_path):
        self.inputs_path = inputs_path
        self.outputs_path = outputs_path

    def predict(self):
        print('load input from {0}'.format(self.inputs_path))

        # codes of algorithm
        print('predict')
        # codes of algorithm

        print('save result in {0}'.format(self.outputs_path))
