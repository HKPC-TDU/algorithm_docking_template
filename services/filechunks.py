import hashlib
import tarfile

import os


class FileChunkService:
    CHUNK_SIZE = 90 * 1024 * 1024  # 90MB
    MODEL_FILE = "model.tar.gz"
    CHUNK_FOLDER = "chunks"
    CHUNK_FILE = "chunks_sha256.json"

    def is_require_chunks(self, folder_path):
        """Calculate the total size of all files in the specified folder and its subfolders."""
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(file_path)
                    if total_size > self.CHUNK_SIZE:
                        return True
                except OSError as e:
                    print(f"Error accessing file {file_path}: {e}")
        return False

    def tar_folder(self, folder_path, output_zip):
        """Create a tar.gz archive of the specified folder."""
        with tarfile.open(output_zip, "w:gz") as tar:
            # tar.add(folder_path)
            # Change the working directory to the folder you want to compress
            current_dir = os.getcwd()
            os.chdir(folder_path)

            # Add all files and directories inside the folder to the archive
            for root, dirs, files in os.walk('.'):
                dirs.sort()
                files.sort()
                for file in files:
                    full_path = os.path.join(root, file)
                    tar.add(full_path, arcname=full_path[2:] if full_path.startswith('./') else full_path)

            # Restore the original working directory
            os.chdir(current_dir)
        print(f"Folder '{folder_path}' has been compressed to '{output_zip}'.")

    def untar_file(self, tar_gz_path, extract_to='.'):
        """Extract all contents from a tar.gz file to a specified directory."""
        with tarfile.open(tar_gz_path, 'r:gz') as tar_ref:
            tar_ref.extractall(path=extract_to)

    def calculate_sha256(self, file_path, zipfile):
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
                if zipfile:
                    zipfile.write(byte_block)
        return sha256_hash.hexdigest()

    def split_file(self, file_path, output_path, chunk_size=CHUNK_SIZE):
        base_name = os.path.splitext(file_path)[0]
        chunks = []
        part_num = 1
        with open(file_path, 'rb') as input_file:
            while True:
                chunk_data = input_file.read(chunk_size)
                if not chunk_data:
                    break

                sha256_hash = hashlib.sha256()
                file_name = os.path.basename(file_path)
                chunk_filename = f"{output_path}/{file_name}.part{part_num}"
                with open(chunk_filename, 'wb') as chunk_file:
                    chunk_file.write(chunk_data)
                    sha256_hash.update(chunk_data)
                part_num += 1
                chunks.append({
                    "file_name": os.path.basename(chunk_filename),
                    "hash_sum": sha256_hash.hexdigest()
                })
        return chunks
