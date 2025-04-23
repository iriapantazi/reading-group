ARG FROM_IMAGE_NAME=nvcr.io/nvidia/pytorch:23.10-py3
FROM ${FROM_IMAGE_NAME}

ENV PYTORCH_VERSION=2.1.0a0+32f93b1


RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/3bf863cc.pub

WORKDIR /workspace/reading-group

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY src src
COPY setup.py .
RUN python -m pip install -e .
