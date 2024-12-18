import os
import requests
import glob
import mimetypes
import zipfile
from pathlib import Path


class UserService:

    def __init__(self, auth_service_host, user, password):
        self.host = auth_service_host
        self.user = user
        self.password = password
        self.token_type = None
        self.access_token = None
        self.refresh_token = None

    def retrieve_access_token(self, client_id, client_secret):
        if self.access_token and self.refresh_token:
            self.refresh_access_token(client_id, client_secret)
            return

        url = f'{self.host}/authorization-center/oauth2/token'
        headers = {
            'Content-Type': 'infra/x-www-form-urlencoded'
        }
        params = {
            "grant_type": "password",
            "client_id": client_id,
            "client_secret": client_secret,
            "username": self.user,
            "password": self.password,
            "scope": "openid apis"
        }
        response = requests.post(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            self.token_type = data['token_type']
            self.access_token = data['access_token']
            self.refresh_token = data['refresh_token']
        else:
            print(f'failed to retrieve token, status {response.status_code}, {response.text}', )

    def refresh_access_token(self, client_id, client_secret):
        url = f'{self.host}/authorization-center/oauth2/token'
        headers = {
            'Content-Type': 'infra/x-www-form-urlencoded'
        }
        params = {
            "grant_type": "refresh_token",
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": self.refresh_token,
        }
        response = requests.post(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            self.token_type = data['token_type']
            self.access_token = data['access_token']
            self.refresh_token = data['refresh_token']
        else:
            print(f'failed to refresh token, status {response.status_code}, {response.text}', )

    def token(self):
        if not self.access_token:
            return None
        return self.token_type + ' ' + self.access_token


class DataService:

    def __init__(self, data_service_host, token):
        self.host = data_service_host
        self.token = token

    def download(self, bucket, prefix, folder_path):
        url = f'{self.host}/data-management/documents/streams/zip?bucket={bucket}&prefix={prefix}'
        headers = {
            'Authorization': self.token,
        }

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file_path = os.path.join(folder_path, os.path.basename(prefix) + ".zip")
        with requests.get(url, headers=headers, stream=True) as response:
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)

        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(folder_path)

        os.remove(file_path)

    def read_folder(self, folder: Path):
        paths = []
        for path in folder.iterdir():
            if path.is_file():
                if ".gitkeep" not in path.name:
                    paths.append(path)
            else:
                self.read_folder(path)
        return paths

    def upload(self, bucket, prefix, files_path):
        file_paths = []
        # paths = self.read_folder(Path(files_path))
        # for file_path in paths:
        for local_file in glob.glob(files_path + "/**", recursive=True):
            if Path(local_file).is_dir():
                continue
            file_paths.append(local_file)

        if not file_paths:
            print('model files not found')
            return None

        url = f'{self.host}/data-management/documents?bucket={bucket}&prefix={prefix}'
        headers = {
            'Authorization': self.token,
            # 'Content-Type': 'multipart/form-data'
        }
        files = [
            ('files', (f.replace(files_path, ""), open(f, 'rb'), mimetypes.guess_type(f)[0]))
            for f in file_paths
        ]

        response = requests.post(url, headers=headers, files=files)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f'failed to upload data, status {response.status_code}, {response.text}')
            return None


class MetaService:

    def __init__(self, meta_service_host, token):
        self.host = meta_service_host
        self.token = token

    def create_artifact(self, task_id, bucket, path, description):
        url = f'{self.host}/meta-data-management/artifacts/files'
        headers = {
            'Authorization': self.token,
            'Content-Type': 'application/json'
        }
        body = {
            "task_id": task_id,
            "file": {
                "bucket": bucket,
                "path": path,
            },
            "description": description
        }
        response = requests.post(url, headers=headers, json=body)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f'failed to retrieve data, status {response.status_code}, {response.text}')

        return None
