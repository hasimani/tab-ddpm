# Start from a minimal Python image
FROM python:3.9-slim-bullseye

# set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PROJECT_DIR=/workspace/tab-ddpm

# create working directory
WORKDIR $PROJECT_DIR

# system dependencies (if needed for packages like scipy, pandas, etc.)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        git \
        wget \
        ca-certificates \
        libglib2.0-0 \
        libsm6 \
        libxrender1 \
        libxext6 && \
    rm -rf /var/lib/apt/lists/*

# copy requirements and project code
COPY requirements.txt $PROJECT_DIR/
COPY . $PROJECT_DIR/

# install PyTorch and other Python requirements
RUN pip install --upgrade pip "setuptools<70.0.0" wheel && \
    pip install "torch==1.10.1+cu111" -f https://download.pytorch.org/whl/torch_stable.html && \
    pip install -r requirements.txt

# set PYTHONPATH to include repo directory
ENV PYTHONPATH="${PYTHONPATH}:${PROJECT_DIR}"

# default command
CMD ["bash"]
