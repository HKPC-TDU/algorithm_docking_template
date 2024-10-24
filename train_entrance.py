from context import TrainingContext
from interceptors import TrainingInterceptor
from services.store import MinIORepository, DocumentService
from train import Model
from pathlib import Path
from utils.file_utils import remove_directory, mkdir_directory
from datetime import datetime
from core.settings import COMPUTATION_ENGINE_LOCAL


def main():
    # 1. build context and interceptor
    context = TrainingContext()
    interceptor = TrainingInterceptor(context)
    # dataset
    # context.set_inputs("tdu-platform-dm", "datasets/20/versions-snapshots/hashAABQ")
    # create_task
    # context.set_task_id("16")
    print('\n ------ ------ ----- context initial ------ ------ ----- \n')
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), context.config)
    mkdir_directory(Path(context.model_inputs_folder))
    mkdir_directory(Path(context.model_outputs_folder))
    mkdir_directory(Path(context.history_model_folder))
    if context.is_prod():
        print('\n ------ ------ ----- data preparation ------ ------ ----- \n')
        # 2. remove inputs and outputs
        remove_directory(Path(context.model_inputs_folder))
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), f'remove history inputs in {context.model_inputs_folder}')
        remove_directory(Path(context.model_outputs_folder))
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), f'remove history outputs in {context.model_outputs_folder}')
        remove_directory(Path(context.history_model_folder))
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), f'remove history model in {context.history_model_folder}')
        config = context.config
        if COMPUTATION_ENGINE_LOCAL.__eq__(config.COMPUTATION_ENGINE_TYPE):
            repository = MinIORepository(config.MINIO_SERVER, config.MINIO_SERVER_ACCESS_KEY,
                                         config.MINIO_SERVER_SECRET_KEY)
        else:
            repository = DocumentService(auth_service_host=config.AI_PLAT_API_AUTH_SERVICE,
                                         user=config.AI_PLAT_USER_NAME, password=config.AI_PLAT_USER_PASSWORD,
                                         client_id=config.AI_PLAT_CLIENT_ID, client_secret=config.AI_PLAT_CLIENT_SECRET,
                                         data_service_host=config.AI_PLAT_API_DATA_SERVICE)
        # 3 download data
        # 3.1 download dataset

        repository.download_inputs(config.TRAINING_DATA_BUCKET, config.TRAINING_DATA_PATH, context.model_inputs_folder)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
              f'download current inputs from {config.TRAINING_DATA_BUCKET}/{config.TRAINING_DATA_PATH}')
        repository.download_inputs(context.get_model_bucket(), context.get_history_model_path(),
                                   context.history_model_folder)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
              f'download history model from {context.get_model_bucket()}/{context.get_history_model_path()}')
        interceptor.starting()
    # 4. model training
    print('\n ------ ------ ----- training ------ ------ ----- \n')
    try:
        model = Model(context.model_inputs_folder, context.model_outputs_folder, context.history_model_folder)
        model.train()
    except Exception as err:
        if context.is_prod():
            interceptor.failure()
        raise err

    if context.is_prod():
        print('\n ------ ------ ----- result persistence ------ ------ ----- \n')
        # 5. store model
        repository.upload_outputs(context.model_outputs_folder, context.get_model_bucket(),
                                  context.get_model_path())
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
              f'upload current outputs to {context.get_model_bucket()}/{context.get_model_path()}')
        # 6. create artifact
        artifact_name = interceptor.success()
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "upload model files as artifact '{}'".format(artifact_name))

    print('\n ------ ------ ----- FINISHED ! ------ ------ -----\n ')


if __name__ == "__main__":
    main()
