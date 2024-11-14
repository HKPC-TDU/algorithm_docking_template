from concurrent import futures
import grpc
from grpc import ServicerContext
from services.grpc_services import prediction_service_pb2_grpc as prediction_service, prediction_service_pb2
from grpc_health.v1 import health_pb2_grpc, health

from context import PredictContext
from predict import ModelPredict
from services.store import MinIORepository, DocumentService
from pathlib import Path
from utils.file_utils import remove_directory, mkdir_directory
from datetime import datetime
from core.settings import COMPUTATION_ENGINE_LOCAL
import os
import time
import mimetypes


class ModelLoadingError(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


class PredictorServicer(prediction_service.PredictorServicer):

    def __init__(self, context, repository, predict_service):
        self.context = context
        self.repository = repository
        self.predict_service = predict_service

    def PredictStream(self, request_iterator, context):
        try:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'request to predict')

            for request in request_iterator:
                start_time = time.time()
                mkdir_directory(Path(self.context.inputs_folder))
                mkdir_directory(Path(self.context.outputs_folder))
                # 1. remove history request
                remove_directory(Path(self.context.inputs_folder))
                print(f'remove history request in {self.context.inputs_folder}')
                # if self.context.is_prod() or self.context.is_pretrain_model():
                remove_directory(Path(self.context.outputs_folder))
                print(f'remove history result in {self.context.outputs_folder}')
                if request.files:
                    args = {
                        "IS_OUTPUT_LABELS": 'true',
                        "IS_OUTPUT_BOUNDBOX": 'false'
                    }
                    for file in request.files:
                        # Process file info
                        print(f"Received file: {file.filename}")
                        input_file = os.path.join(self.context.inputs_folder, file.filename)
                        with open(input_file, 'wb') as file_in:
                            file_in.write(file.content)
                    self.predict_service.predict(args)
                    output_labels_file = self.predict_service.get_output_json_path()
                    with open(output_labels_file, 'rb') as file_out:
                        binary_data = file_out.read()

                    file_name = os.path.basename(output_labels_file)
                    mime_type, _ = mimetypes.guess_type(output_labels_file)
                    size = os.path.getsize(output_labels_file)
                    print('request cost {}'.format(str(time.time() - start_time)))
                    yield prediction_service_pb2.PredictStreamResponse(
                        file=prediction_service_pb2.StreamFile(
                            contentType=mime_type,
                            filename=file_name,
                            content=binary_data,
                            length=size
                        )
                    )

        except ModelLoadingError as ex:
            context.abort(ex.status_code, ex.message)

    def PredictorPredict(self, request, context: ServicerContext):
        try:
            now = datetime.now()
            print(now.strftime("%Y-%m-%d %H:%M:%S"), 'request to predict')
            print("request:", request)
            mkdir_directory(Path(self.context.inputs_folder))
            mkdir_directory(Path(self.context.outputs_folder))
            if self.context.is_prod() or self.context.is_pretrain_model():
                contact = "###"
                data_info = request.document.split(contact)
                bucket = data_info[0]
                path = data_info[1]
                # 1. remove history request
                remove_directory(Path(self.context.inputs_folder))
                print(f'remove history request in {self.context.inputs_folder}')
                remove_directory(Path(self.context.outputs_folder))
                print(f'remove history result in {self.context.outputs_folder}')
                # 2 download current request
                inputs_path, minio_folder = self.repository.download_inputs(bucket, path, self.context.inputs_folder)
                print(f'download request from {bucket}/{path}')
                # 3. predict by model
                self.predict_service.predict(request.args)
                # 4. upload result to minio
                minio_path = f'{minio_folder}/outputs/{now.strftime("%Y%m%d%H%M%S%f")}'
                self.repository.upload_outputs(local_path=self.context.outputs_folder, bucket_name=bucket,
                                               minio_path=minio_path)
                print(f'upload result to {bucket}/{minio_path}')
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'finish\n')
                return prediction_service_pb2.PredictorPredictResponse(
                    response=f'{bucket}{contact}{minio_path}')
            # develop environment
            self.predict_service.predict(request.args)
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'finish\n')
            return prediction_service_pb2.PredictorPredictResponse(
                response=f'success to store result in {self.context.outputs_folder}')
        except ModelLoadingError as ex:
            context.abort(ex.status_code, ex.message)


def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    context = PredictContext()
    print('\n ------ ------ ----- context initial ------ ------ ----- \n')
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), context.config)
    config = context.config
    if COMPUTATION_ENGINE_LOCAL.__eq__(config.COMPUTATION_ENGINE_TYPE):
        repository = MinIORepository(config.MINIO_SERVER, config.MINIO_SERVER_ACCESS_KEY,
                                     config.MINIO_SERVER_SECRET_KEY)
    else:
        repository = DocumentService(auth_service_host=config.AI_PLAT_API_AUTH_SERVICE,
                                     user=config.AI_PLAT_USER_NAME, password=config.AI_PLAT_USER_PASSWORD,
                                     client_id=config.AI_PLAT_CLIENT_ID, client_secret=config.AI_PLAT_CLIENT_SECRET,
                                     data_service_host=config.AI_PLAT_API_DATA_SERVICE)
    # download model
    print('\n ------ ------ ----- model loading ------ ------ ----- \n')
    mkdir_directory(Path(context.model_folder))
    if context.is_prod() and context.model_bucket and context.model_path:
        remove_directory(Path(context.model_folder))
        print(f'remove history result in {context.model_folder}')
        repository.download_inputs(context.model_bucket, context.model_path, context.model_folder)
        print(f'download model from {context.model_bucket}/{context.model_path}')
    print(f'load model in {context.model_folder}')
    print('\n ------ ------ ----- serving ------ ------ ----- \n')
    predict_model = ModelPredict(context.inputs_folder, context.outputs_folder, context.model_folder)
    prediction_service.add_PredictorServicer_to_server(
        PredictorServicer(context, repository, predict_model), server)
    health_servicer = health.HealthServicer(
        experimental_non_blocking=True,
        experimental_thread_pool=futures.ThreadPoolExecutor(max_workers=10))
    health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)
    server.add_insecure_port('0.0.0.0:51001')
    server.start()
    print("server is running\n\n")
    server.wait_for_termination()


if __name__ == "__main__":
    main()
