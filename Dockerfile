# source - https://github.com/adithya-s-k/marker-api/blob/master/docker/Dockerfile.cpu.server
FROM nvidia/cuda:12.9.1-cudnn-devel-ubuntu20.04

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    curl \
    unzip \
    git \
    python3 \
    python3-pip \
    libgl1 \
    libglib2.0-0 \
    curl \
    gnupg2 \
    ca-certificates \
    apt-transport-https \
    software-properties-common \
    libreoffice \
    ffmpeg \
    git-lfs \
    xvfb \
    && ln -s /usr/bin/python3 /usr/bin/python \
    && apt-get update \
    && apt install python3-packaging \    
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip

RUN pip3 install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu129

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ADD . /app
WORKDIR /app
RUN uv sync --locked
RUN ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "6969", "--reload"]