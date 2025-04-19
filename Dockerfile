FROM python:3.11-slim

# ARG GITHUB_REPO=https://github.com/unclecode/crawl4ai.git
# ARG GITHUB_BRANCH=main
# ARG INSTALL_TYPE=default
# ARG ENABLE_GPU=false
# ARG TARGETARCH

# ENV PYTHONFAULTHANDLER=1 \
#     PYTHONHASHSEED=random \
#     PYTHONUNBUFFERED=1 \
#     PYTHONDONTWRITEBYTECODE=1 \
#     PIP_NO_CACHE_DIR=1 \
#     PIP_DISABLE_PIP_VERSION_CHECK=1 \
#     PIP_DEFAULT_TIMEOUT=100 \
#     DEBIAN_FRONTEND=noninteractive \
#     REDIS_HOST=localhost \
#     REDIS_PORT=6379

# WORKDIR /app

# RUN apt-get update && apt-get install -y --no-install-recommends \
#         build-essential \
#         curl \
#         wget \
#         git \
#         cmake \
#         pkg-config \
#         python3-dev \
#         libjpeg-dev \
#         redis-server \
#         libglib2.0-0 \
#         libnss3 \
#         libnspr4 \
#         libatk1.0-0 \
#         libatk-bridge2.0-0 \
#         libcups2 \
#         libdrm2 \
#         libdbus-1-3 \
#         libxcb1 \
#         libx11-6 \
#         libxcomposite1 \
#         libxdamage1 \
#         libxext6 \
#         libxfixes3 \
#         libxrandr2 \
#         libgbm1 \
#         libpango-1.0-0 \
#         libcairo2 \
#         libasound2 \
#         libatspi2.0-0 \
#     && rm -rf /var/lib/apt/lists/*

# RUN if [ "$ENABLE_GPU" = "true" ] && [ "$TARGETARCH" = "amd64" ] ; then \
#         apt-get update && apt-get install -y --no-install-recommends nvidia-cuda-toolkit && \
#         rm -rf /var/lib/apt/lists/*; \
#     else \
#         echo "Skipping NVIDIA CUDA Toolkit (unsupported or disabled)"; \
#     fi && \
#     if [ "$TARGETARCH" = "arm64" ]; then \
#         apt-get update && apt-get install -y --no-install-recommends libopenblas-dev && \
#         rm -rf /var/lib/apt/lists/*; \
#     elif [ "$TARGETARCH" = "amd64" ]; then \
#         apt-get update && apt-get install -y --no-install-recommends libomp-dev && \
#         rm -rf /var/lib/apt/lists/*; \
#     else \
#         echo "Skipping platform‑specific optimizations"; \
#     fi

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# RUN git clone --depth 1 --branch ${GITHUB_BRANCH} ${GITHUB_REPO} /tmp/crawl4ai \
#     && pip install --no-cache-dir /tmp/crawl4ai${INSTALL_TYPE:+[${INSTALL_TYPE}]} \
#     && rm -rf /tmp/crawl4ai

# RUN if [ "${INSTALL_TYPE}" = "all" ]; then \
#         python -m nltk.downloader punkt stopwords ; \
#     fi

# RUN pip install --no-cache-dir playwright \
#     && playwright install --with-deps chromium

COPY . .
EXPOSE 10000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
