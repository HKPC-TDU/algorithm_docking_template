from utils.orca3_utils import ModelTrainingHandler


class TrainingInterceptor:
    def __init__(self, context):
        self.context = context
        self.interceptor = ModelTrainingHandler(context.config.METADATA_STORE_SERVER, context.config.JOB_ID,
                                                context.config.RANK,
                                                context.config.TRAINING_DATASET_ID,
                                                context.config.TRAINING_DATASET_VERSION_HASH,
                                                context.config.MODEL_VERSION,
                                                context.config.MODEL_NAME)

    def create_artifact(self):
        return self.interceptor.create_artifact(self.context.model_bucket, self.context.model_path,
                                                self.context.algorithm_name)
