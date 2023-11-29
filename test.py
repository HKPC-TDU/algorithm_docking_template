import grpc
import prediction_service_pb2
import prediction_service_pb2_grpc

channel = grpc.insecure_channel("localhost:51001")
stub = prediction_service_pb2_grpc.PredictorStub(channel)
result = stub.PredictorPredict(
    prediction_service_pb2.PredictorPredictRequest(
        document='tdu-platform-dm###datasets/20/versions-snapshots/hashAABQ'
    )
)

print(result)
