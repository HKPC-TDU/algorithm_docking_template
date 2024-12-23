from services.filechunks import FileChunkService
from pathlib import Path
from utils.file_utils import remove_directory, mkdir_directory

import time
import os
import json


class FileService:

    def __init__(self, data_service):
        self.data_service = data_service
        self.fileChunkService = FileChunkService()

    def upload(self, bucket, prefix, input_folder):
        stat_time = time.time()
        if not self.fileChunkService.is_require_chunks(input_folder):
            self.data_service.upload(bucket, prefix, input_folder)
            print('!!!!!!!!!!!!!!!!!!!upload model files cost {}'.format(str(time.time() - stat_time)))
            return

        backup = input_folder + "_backup"
        mkdir_directory(Path(backup))
        remove_directory(Path(backup))
        zipfile = os.path.join(backup, self.fileChunkService.MODEL_FILE)
        self.fileChunkService.tar_folder(input_folder, zipfile)

        chunks_path = os.path.join(backup, self.fileChunkService.CHUNK_FOLDER)
        mkdir_directory(Path(chunks_path))
        chunks = self.fileChunkService.split_file(zipfile, chunks_path)
        output_labels_file = os.path.join(chunks_path, self.fileChunkService.CHUNK_FILE)
        with open(output_labels_file, 'w') as output_file:
            json.dump(chunks, output_file, indent=4)
        self.data_service.upload(bucket, prefix, chunks_path)
        print('!!!!!!!!!!!!!!!!!!!model files zip and upload cost {}'.format(str(time.time() - stat_time)))

    def download(self, bucket, prefix, output_folder):
        stat_time = time.time()
        mkdir_directory(Path(output_folder))
        remove_directory(Path(output_folder))
        self.data_service.download(bucket, prefix, output_folder)

        chunk_sum_json = os.path.join(output_folder, self.fileChunkService.CHUNK_FILE)
        if os.path.isfile(chunk_sum_json):
            with open(chunk_sum_json, 'r') as data_file:
                data = json.load(data_file)

            zipfile_path = os.path.join(output_folder, self.fileChunkService.MODEL_FILE)
            with open(zipfile_path, 'wb') as zipfile:
                for chunk in data:
                    chunk_file = os.path.join(output_folder, chunk["file_name"])
                    check_sum = self.fileChunkService.calculate_sha256(chunk_file, zipfile)
                    if not check_sum.__eq__(chunk["hash_sum"]):
                        print("file hash check error: ", chunk_file)
            self.fileChunkService.untar_file(zipfile_path, output_folder)
            print('!!!!!!!!!!!!!!!!!!!download cost {}'.format(str(time.time() - stat_time)))
