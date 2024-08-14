from services.training_handlers import LocalTrainingHandler, DistributedTrainingHandler
from core.settings import COMPUTATION_ENGINE_LOCAL


class TrainingInterceptor:
    def __init__(self, context):
        self.context = context
        if COMPUTATION_ENGINE_LOCAL.__eq__(context.config.COMPUTATION_ENGINE_TYPE):
            self.interceptor = LocalTrainingHandler(context.config.METADATA_STORE_SERVER, context.config.TASK_ID,
                                                    context.config.TRAINING_DATASET_ID,
                                                    context.config.TRAINING_DATASET_VERSION_HASH,
                                                    context.config.MODEL_VERSION,
                                                    context.config.MODEL_NAME)
        else:
            self.interceptor = DistributedTrainingHandler(auth_service_host=context.config.AI_PLAT_API_AUTH_SERVICE,
                                                          user=context.config.AI_PLAT_USER_NAME,
                                                          password=context.config.AI_PLAT_USER_PASSWORD,
                                                          client_id=context.config.AI_PLAT_CLIENT_ID,
                                                          client_secret=context.config.AI_PLAT_CLIENT_SECRET,
                                                          meta_service_host=context.config.AI_PLAT_API_META_SERVICE,
                                                          task_id=context.config.TASK_ID)

    def starting(self):
        self.interceptor.log_run_start()

    def failure(self):
        self.interceptor.log_run_end(False, 'fail to complete training job.')

    def success(self):
        self.interceptor.log_run_end(True, 'success to complete training job.')
        return self.interceptor.create_artifact(self.context.get_model_bucket(), self.context.get_model_path(),
                                                self.context.algorithm_name)
