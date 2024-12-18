FROM python:3.8.0

WORKDIR /app

# fix: opencv-python-headless, Error: libGL.so.1: cannot open shared object file: No such file or directory
RUN apt-get update
RUN apt-get install -y libglib2.0-0
RUN apt-get install -y libsm6 libxext6 libxrender-dev
RUN apt-get install libgl1-mesa-glx -y

# AIM platform dependecies
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple minio==7.2.3 protobuf==3.20.3 grpcio==1.60.0 grpcio-health-checking==1.48.2

COPY requirements.txt requirements.txt
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt


COPY . .

EXPOSE 51001

#CMD [ "sh", "run_script.sh"]
CMD [ "python3", "-u", "manage.py"]
