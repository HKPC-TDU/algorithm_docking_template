class Model:

    def __init__(self, inputs_path, outputs_path):
        self.inputs_path = inputs_path
        self.outputs_path = outputs_path

    def train(self):
        print('load dataset from {0}'.format(self.inputs_path))

        # codes of algorithm
        print('training')
        # codes of algorithm

        print('save model in {0}'.format(self.outputs_path))
