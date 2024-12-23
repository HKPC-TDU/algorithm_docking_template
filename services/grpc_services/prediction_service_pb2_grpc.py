# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import services.grpc_services.prediction_service_pb2 as prediction__service__pb2


class PredictionServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.deployPredictor = channel.unary_unary(
                '/prediction.PredictionService/deployPredictor',
                request_serializer=prediction__service__pb2.InferenceServiceRequest.SerializeToString,
                response_deserializer=prediction__service__pb2.InferenceServiceResponse.FromString,
                )
        self.Predict = channel.unary_unary(
                '/prediction.PredictionService/Predict',
                request_serializer=prediction__service__pb2.PredictRequest.SerializeToString,
                response_deserializer=prediction__service__pb2.PredictResponse.FromString,
                )
        self.registerContainer = channel.unary_unary(
                '/prediction.PredictionService/registerContainer',
                request_serializer=prediction__service__pb2.RegisterInferenceContainerRequest.SerializeToString,
                response_deserializer=prediction__service__pb2.InferenceServiceResponse.FromString,
                )


class PredictionServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def deployPredictor(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Predict(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def registerContainer(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PredictionServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'deployPredictor': grpc.unary_unary_rpc_method_handler(
                    servicer.deployPredictor,
                    request_deserializer=prediction__service__pb2.InferenceServiceRequest.FromString,
                    response_serializer=prediction__service__pb2.InferenceServiceResponse.SerializeToString,
            ),
            'Predict': grpc.unary_unary_rpc_method_handler(
                    servicer.Predict,
                    request_deserializer=prediction__service__pb2.PredictRequest.FromString,
                    response_serializer=prediction__service__pb2.PredictResponse.SerializeToString,
            ),
            'registerContainer': grpc.unary_unary_rpc_method_handler(
                    servicer.registerContainer,
                    request_deserializer=prediction__service__pb2.RegisterInferenceContainerRequest.FromString,
                    response_serializer=prediction__service__pb2.InferenceServiceResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'prediction.PredictionService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class PredictionService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def deployPredictor(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/prediction.PredictionService/deployPredictor',
            prediction__service__pb2.InferenceServiceRequest.SerializeToString,
            prediction__service__pb2.InferenceServiceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Predict(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/prediction.PredictionService/Predict',
            prediction__service__pb2.PredictRequest.SerializeToString,
            prediction__service__pb2.PredictResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def registerContainer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/prediction.PredictionService/registerContainer',
            prediction__service__pb2.RegisterInferenceContainerRequest.SerializeToString,
            prediction__service__pb2.InferenceServiceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class PredictorStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.PredictorPredict = channel.unary_unary(
                '/prediction.Predictor/PredictorPredict',
                request_serializer=prediction__service__pb2.PredictorPredictRequest.SerializeToString,
                response_deserializer=prediction__service__pb2.PredictorPredictResponse.FromString,
                )
        self.PredictStream = channel.stream_stream(
                '/prediction.Predictor/PredictStream',
                request_serializer=prediction__service__pb2.PredictStreamRequest.SerializeToString,
                response_deserializer=prediction__service__pb2.PredictStreamResponse.FromString,
                )


class PredictorServicer(object):
    """Missing associated documentation comment in .proto file."""

    def PredictorPredict(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PredictStream(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PredictorServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'PredictorPredict': grpc.unary_unary_rpc_method_handler(
                    servicer.PredictorPredict,
                    request_deserializer=prediction__service__pb2.PredictorPredictRequest.FromString,
                    response_serializer=prediction__service__pb2.PredictorPredictResponse.SerializeToString,
            ),
            'PredictStream': grpc.stream_stream_rpc_method_handler(
                    servicer.PredictStream,
                    request_deserializer=prediction__service__pb2.PredictStreamRequest.FromString,
                    response_serializer=prediction__service__pb2.PredictStreamResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'prediction.Predictor', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Predictor(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def PredictorPredict(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/prediction.Predictor/PredictorPredict',
            prediction__service__pb2.PredictorPredictRequest.SerializeToString,
            prediction__service__pb2.PredictorPredictResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def PredictStream(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/prediction.Predictor/PredictStream',
            prediction__service__pb2.PredictStreamRequest.SerializeToString,
            prediction__service__pb2.PredictStreamResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
