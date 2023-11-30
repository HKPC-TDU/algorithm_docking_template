from context import TrainingContext
from interceptors import TrainingInterceptor
from store import Repository
from train import Model
from pathlib import Path
from utils.file_utils import remove_directory
from datetime import datetime


def main():
    # 1. build context
    context = TrainingContext()
    # dataset
    # context.set_inputs("tdu-platform-dm", "datasets/20/versions-snapshots/hashAABQ")
    # create_task
    # context.set_task_id("12")
    print('\n ------ ------ ----- context initial ------ ------ ----- \n')
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), context.config)
    if context.is_prod():
        print('\n ------ ------ ----- data preparation ------ ------ ----- \n')
        # 2. remove inputs and outputs
        remove_directory(Path(context.model_inputs_path))
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), f'remove history inputs in {context.model_inputs_path}')
        remove_directory(Path(context.model_outputs_path))
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), f'remove history outputs in {context.model_outputs_path}')

        repository = Repository(context.config.MINIO_SERVER, context.config.MINIO_SERVER_ACCESS_KEY,
                                context.config.MINIO_SERVER_SECRET_KEY)
        # 3. download dataset
        repository.download_input_paths(context.config.TRAINING_DATA_BUCKET, context.config.TRAINING_DATA_PATH,
                                        context.model_inputs_path)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
              f'download current inputs from {context.config.TRAINING_DATA_BUCKET}/{context.config.TRAINING_DATA_PATH}')
    # 4. model training
    print('\n ------ ------ ----- training ------ ------ ----- \n')
    model = Model(context.model_inputs_path, context.model_outputs_path)
    model.train()
    if context.is_prod():
        print('\n ------ ------ ----- result persistence ------ ------ ----- \n')
        # 5. store model
        repository.upload_local_folder_to_minio(context.model_outputs_path, context.config.MODEL_BUCKET,
                                                context.config.MODEL_OBJECT_NAME)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
              f'upload current outputs to {context.config.MODEL_BUCKET}/{context.config.MODEL_OBJECT_NAME}')
        interceptor = TrainingInterceptor(context)
        # 6. create artifact
        artifact = interceptor.create_artifact()
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "upload model files as artifact '{}'".format(artifact.name))
    print('\n ------ ------ ----- FINISHED ! ------ ------ -----\n ')


if __name__ == "__main__":
    main()
