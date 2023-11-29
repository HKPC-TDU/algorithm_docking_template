from core.settings import TrainingConfig, PredictConfig


class TrainingContext:
    def __init__(self):
        self.config = TrainingConfig()
        self.model_bucket = self.config.MODEL_BUCKET
        self.model_path = self.config.MODEL_OBJECT_NAME
        self.algorithm_name = self.config.ALGORITHM_NAME
        self.model_inputs_path = './train_inputs'
        self.model_outputs_path = './train_outputs'
        # self.model_data_path = './train_model_data'

    def set_inputs(self, bucket, path):
        self.config.TRAINING_DATA_BUCKET = bucket
        self.config.TRAINING_DATA_PATH = path

    def set_task_id(self, task_id):
        self.config.JOB_ID = task_id

    def is_prod(self):
        return self.config.ENV and "PROD".__eq__(self.config.ENV.upper())


class PredictContext:

    def __init__(self):
        self.config = PredictConfig()
        self.inputs_path = './requests'
        self.outputs_path = './responses'

    def is_prod(self):
        return self.config.ENV and "PROD".__eq__(self.config.ENV.upper())
