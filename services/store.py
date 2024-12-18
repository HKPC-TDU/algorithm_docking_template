import os
import glob
from pathlib import Path
from minio import Minio
from services.repository import Repository
from services.aim_plat import UserService, DataService


class DocumentService(Repository):

    def __init__(self, auth_service_host, user, password, client_id, client_secret, data_service_host):
        self.user_service = UserService(auth_service_host, user, password)
        self.client_id = client_id
        self.client_secret = client_secret
        self.data_service_host = data_service_host

    def download_inputs(self, bucket, path, inputs_path):
        self.user_service.retrieve_access_token(self.client_id, self.client_secret)
        data_service = DataService(self.data_service_host, self.user_service.token())
        data_service.download(bucket, path, folder_path=inputs_path)
        minio_folder = path
        if Path(path).is_file():
            minio_folder = os.path.dirname(path)
        return inputs_path, minio_folder

    def upload_outputs(self, local_path, bucket_name, minio_path):
        self.user_service.retrieve_access_token(self.client_id, self.client_secret)
        data_service = DataService(self.data_service_host, self.user_service.token())
        data_service.upload(bucket_name, minio_path, local_path)


class MinIORepository:
    def __init__(self, host, user, password):
        self.client = Minio(
            host,
            access_key=user,
            secret_key=password,
            secure=False
        )

    def download_inputs(self, bucket, path, inputs_path):
        # print('start download inputs')
        data_files = self.client.list_objects(bucket, path, recursive=True)
        is_self_path = True
        for item in data_files:
            relative_path = os.path.relpath(item.object_name, start=path)
            # 如果相对路径为 '.'，说明路径和前缀完全相同，返回最短路劲
            if relative_path == '.':
                relative_path = os.path.basename(item.object_name)
            else:
                is_self_path = False
            self.client.fget_object(bucket, item.object_name,
                                    "{0}/{1}".format(inputs_path, relative_path))
        # print('success to download inputs: {0}'.format(inputs_path))
        minio_folder = path
        if is_self_path:
            minio_folder = os.path.dirname(path)
        return inputs_path, minio_folder

    def upload_outputs(self, local_path, bucket_name, minio_path):
        if not os.path.isfile(local_path):
            # hidden files (files starting with .) will not be found when use glob.glob
            for local_file in glob.glob(local_path + '/**'):
                local_file = local_file.replace(os.sep, "/")
                dir_path = local_file if os.path.isdir(local_file) else os.path.dirname(local_file)
                relative_path = dir_path.replace(local_path, "")
                if relative_path == "":
                    self.upload_outputs(local_file, bucket_name, minio_path)
                else:
                    if relative_path.startswith("/"):
                        relative_path = relative_path.lstrip("/")
                    self.upload_outputs(
                        local_file, bucket_name, os.path.join(minio_path, relative_path))
        else:
            remote_path = os.path.join(minio_path, os.path.basename(local_path))
            print(f'upload {local_path} to {bucket_name}, {remote_path}')
            self.client.fput_object(bucket_name, remote_path, local_path)
