from context import TrainingContext
from interceptors import TrainingInterceptor
from store import Repository
from train import Model
from pathlib import Path
from utils.file_utils import remove_directory


def main():
    context = TrainingContext()
    # dataset
    # context.set_inputs("tdu-platform-dm", "datasets/20/versions-snapshots/hashAABQ")
    # create_task
    # context.set_task_id("12")
    print(context.config)
    interceptor = TrainingInterceptor(context)
    repository = Repository(context.config.MINIO_SERVER, context.config.MINIO_SERVER_ACCESS_KEY,
                            context.config.MINIO_SERVER_SECRET_KEY)
    # remove inputs and outputs
    remove_directory(Path(context.model_inputs_path))
    remove_directory(Path(context.model_outputs_path))
    # download dataset
    repository.download_input_paths(context.config.TRAINING_DATA_BUCKET, context.config.TRAINING_DATA_PATH,
                                    context.model_inputs_path)
    model = Model(context.model_inputs_path, context.model_outputs_path)
    model.train()
    # store model
    repository.upload_local_folder_to_minio(context.model_outputs_path, context.config.MODEL_BUCKET,
                                            context.config.MODEL_OBJECT_NAME)
    artifact = interceptor.create_artifact()
    print("upload model files as artifact '{}'".format(artifact.name))
    print('\n ------ ------ ----- FINISHED ! ------ ------ -----\n ')


if __name__ == "__main__":
    main()
