from concurrent import futures
import grpc
from grpc import ServicerContext
import os
import prediction_service_pb2
import prediction_service_pb2_grpc as prediction_service
from grpc_health.v1 import health_pb2_grpc, health

from context import PredictContext
from predict import ModelPredict
from store import Repository
from pathlib import Path
from utils.file_utils import remove_directory


class ModelLoadingError(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


class PredictorServicer(prediction_service.PredictorServicer):

    def __init__(self, context, repository, predict_service):
        self.context = context
        self.repository = repository
        self.predict_service = predict_service

    def PredictorPredict(self, request, context: ServicerContext):
        try:
            contact = "###"
            data_info = request.document.split(contact)
            bucket = data_info[0]
            path = data_info[1]
            # print(bucket+":"+path)
            remove_directory(Path(self.context.inputs_path))
            remove_directory(Path(self.context.outputs_path))
            self.repository.download_input_paths(bucket, path, self.context.inputs_path)
            self.predict_service.predict()

            minio_path = f'{path}/outputs'
            self.repository.upload_local_folder_to_minio(local_path=self.context.outputs_path, bucket_name=bucket,
                                                         minio_path=minio_path)
            return prediction_service_pb2.PredictorPredictResponse(
                response=f'{bucket}{contact}{minio_path}')
        except ModelLoadingError as ex:
            context.abort(ex.status_code, ex.message)


def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    context = PredictContext()
    repository = Repository(context.config.MINIO_SERVER, context.config.MINIO_SERVER_ACCESS_KEY,
                            context.config.MINIO_SERVER_SECRET_KEY)
    predict_model = ModelPredict(context.inputs_path, context.outputs_path)
    prediction_service.add_PredictorServicer_to_server(
        PredictorServicer(context, repository, predict_model), server)
    health_servicer = health.HealthServicer(
        experimental_non_blocking=True,
        experimental_thread_pool=futures.ThreadPoolExecutor(max_workers=10))
    health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)
    server.add_insecure_port('0.0.0.0:51001')
    server.start()
    print("server is running")
    server.wait_for_termination()


if __name__ == "__main__":
    main()
