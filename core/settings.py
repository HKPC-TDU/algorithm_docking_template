import os
import sys

COMPUTATION_ENGINE_LOCAL = 'LocalContainer'


class Config:
    def __init__(self):
        self.ENV = os.environ.get('ENV') or "dev"
        self.COMPUTATION_ENGINE_TYPE = os.environ.get("COMPUTATION_ENGINE_TYPE", "") or "Local"
        self.AI_PLAT_API_AUTH_SERVICE = os.environ.get("AI_PLAT_API_AUTH_SERVICE") or "http://127.0.0.1"
        self.AI_PLAT_CLIENT_ID = os.environ.get("AI_PLAT_CLIENT_ID", "") or "0c3dc2c1-c912-4273-bdcc-c4bcfaaf2ee0"
        self.AI_PLAT_CLIENT_SECRET = os.environ.get("AI_PLAT_CLIENT_SECRET",
                                                    "") or "UVhCd2JHbGpZWFJwYjI1N1kyeHBaVzUwU1dROUp6QmpNMlJqTW1NeExXTTVNVEl0TkRJM015MWlaR05qTFdNMFltTm1ZV0ZtTW1WbE1DY3NJRzVoYldVOUozUmxjM1JBYUd0d1l5NXZjbWNuTENCdmQyNWxjazVoYldVOUoyaHJjR01uTENCelpYSjJaWEp6UFZ0b2RIUndPaTh2TVRJM0xqQXVNQzR4T2pNd01EQmRmUT09LiQyYSQxMCRhN2Y4WnVQYXYuVjJ3bFBjbldWMWN1QTBwWDBkQVcuQVN1OFJxRm9QeXNtSldKOFZEekg3Qy4xNzE3Mzc1NTQ1MjY5"
        self.AI_PLAT_USER_NAME = os.environ.get("AI_PLAT_USER_NAME", "") or "test@hkpc.org"
        self.AI_PLAT_USER_PASSWORD = os.environ.get("AI_PLAT_USER_PASSWORD", "") or "HKPC@2024"
        self.AI_PLAT_API_DATA_SERVICE = os.environ.get("AI_PLAT_API_DATA_SERVICE", "") or "http://127.0.0.1"
        self.AI_PLAT_API_META_SERVICE = os.environ.get("AI_PLAT_API_META_SERVICE", "") or "http://127.0.0.1"


class TrainingConfig(Config):
    @staticmethod
    def int_or_default(variable, default):
        if variable is None:
            return default
        else:
            return int(variable)

    def __str__(self) -> str:
        if not "PROD".__eq__(self.ENV.upper()):
            return "model training settings"

        results = [
            "'{}' training settings".format(self.MODEL_NAME),
            "\nbackend service settings:",
            "{}={}".format("JOB_ID", self.TASK_ID),
            "{}={}".format("ALGORITHM_NAME", self.ALGORITHM_NAME),
            "{}={}".format("TRAINING_DATA_BUCKET", self.TRAINING_DATA_BUCKET),
            "{}={}".format("TRAINING_DATA_PATH", self.TRAINING_DATA_PATH),
            "{}={}".format("TRAINING_DATASET_ID", self.TRAINING_DATASET_ID),
            "{}={}".format("TRAINING_DATASET_VERSION_HASH", self.TRAINING_DATASET_VERSION_HASH),
            "{}={}".format("METADATA_STORE_SERVER", self.METADATA_STORE_SERVER),
            "{}={}".format("MINIO_SERVER", self.MINIO_SERVER),
            "{}={}".format("MINIO_SERVER_ACCESS_KEY", self.MINIO_SERVER_ACCESS_KEY),
            "{}={}".format("MINIO_SERVER_SECRET_KEY", self.MINIO_SERVER_SECRET_KEY),
            "{}={}".format("MODEL_BUCKET", self.MODEL_BUCKET),
            "{}={}".format("EPOCHS", self.EPOCHS),
            "{}={}".format("SAVE_EVERY_EPOCH", self.SAVE_EVERY_EPOCH),
            "{}={}".format("BATCH_SIZE", self.BATCH_SIZE),
        ]
        return "\n".join(results)

    def __init__(self):
        super().__init__()
        ######################## define in the backend services ###########################
        self.TASK_ID = os.getenv('JOB_ID') or "100"
        self.ALGORITHM_NAME = os.getenv('ALGORITHM_NAME') or "algo_few-shot-image-detector"
        self.METADATA_STORE_SERVER = os.getenv('METADATA_STORE_SERVER') or "127.0.0.1:6002"
        self.DATA_MANAGEMENT_SERVER = os.getenv('DATA_MANAGEMENT_SERVER') or "127.0.0.1:6000"
        self.TRAINING_DATASET_ID = os.getenv('TRAINING_DATASET_ID') or "2"
        self.TRAINING_DATASET_VERSION_HASH = os.getenv('TRAINING_DATASET_VERSION_HASH') or "hashBA=="
        self.MODEL_BUCKET = os.getenv('MODEL_BUCKET') or "tdu-platform-ms"
        self.MODEL_NAME = os.getenv('MODEL_NAME') or "task_few-shot-image-detector"
        self.MODEL_VERSION = "1.0"
        # docker: minio:9000, local: 127.0.0.1:9000
        self.MINIO_SERVER = os.getenv('MINIO_SERVER') or "127.0.0.1:9000"
        self.MINIO_SERVER_ACCESS_KEY = os.getenv('MINIO_SERVER_ACCESS_KEY') or "foooo"
        self.MINIO_SERVER_SECRET_KEY = os.getenv('MINIO_SERVER_SECRET_KEY') or "barbarbar"
        self.TRAINING_DATA_BUCKET = os.getenv('TRAINING_DATA_BUCKET') or "tdu-platform-dm"
        self.TRAINING_DATA_PATH = os.getenv('TRAINING_DATA_PATH') or "datasets/2/versions-snapshots/hashBA=="
        # hyper parameters
        self.EPOCHS = os.getenv('EPOCHS') or "500"
        self.SAVE_EVERY_EPOCH = os.getenv('SAVE_EVERY_EPOCH') or "50"
        self.BATCH_SIZE = os.getenv('BATCH_SIZE') or "10"


class PredictConfig(Config):

    def __str__(self) -> str:
        if not "PROD".__eq__(self.ENV.upper()):
            return "predict service settings"

        results = [
            "predict service settings",
            "{}={}".format("ENV", self.ENV),
            "{}={}".format("MINIO_SERVER", self.MINIO_SERVER),
            "{}={}".format("MINIO_SERVER_ACCESS_KEY", self.MINIO_SERVER_ACCESS_KEY),
            "{}={}".format("MINIO_SERVER_SECRET_KEY", self.MINIO_SERVER_SECRET_KEY),
            "{}={}".format("MODEL_BUCKET", self.MODEL_BUCKET),
            "{}={}".format("MODEL_PATH", self.MODEL_PATH),
        ]

        return "\n".join(results)

    def __init__(self):
        super().__init__()

        # docker: minio:9000, local: 127.0.0.1:9000
        self.MINIO_SERVER = os.getenv('MINIO_SERVER') or "127.0.0.1:9000"
        self.MINIO_SERVER_ACCESS_KEY = os.getenv('MINIO_SERVER_ACCESS_KEY') or "foooo"
        self.MINIO_SERVER_SECRET_KEY = os.getenv('MINIO_SERVER_SECRET_KEY') or "barbarbar"
        self.MODEL_BUCKET = os.getenv('MODEL_BUCKET') or "tdu-platform-ms"
        self.MODEL_PATH = os.getenv('MODEL_PATH') or "artifacts/task_few-shot-image-detector"
