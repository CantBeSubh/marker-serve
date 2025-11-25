ARG CUDA_VERSION="11.8.0"
ARG CUDNN_VERSION="8"
ARG UBUNTU_VERSION="22.04"


FROM nvidia/cuda:$CUDA_VERSION-cudnn$CUDNN_VERSION-devel-ubuntu$UBUNTU_VERSION

ENV DISABLE_AUTH="True"
ENV MAX_WORKERS=3

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
  xvfb

RUN pip3 install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ADD . /app
WORKDIR /app
RUN uv sync --locked
RUN uv pip install uvicorn
RUN uv run python3 -c 'from marker.models import create_model_dict;create_model_dict()'

# CMD uv run uvicorn main:app --host 0.0.0.0 --port 80 --workers $MAX_WORKERS
CMD uv run hypercorn --access-log - --error-log - main:app --bind 0.0.0.0:80 --workers $MAX_WORKERS
