# Set platform argument at the start
ARG TARGETPLATFORM=linux/amd64

# Use the platform argument in FROM
FROM er-saas-registry.cn-beijing.cr.aliyuncs.com/triage_namespace/er_triage_0210:python-3.9-slim-bookworm-amd64

# Switch to Alibaba mirrors for apt
RUN rm -rf /etc/apt/sources.list.d/* && \
    echo "deb https://mirrors.aliyun.com/debian/ bookworm main contrib non-free non-free-firmware" > /etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian-security/ bookworm-security main contrib non-free non-free-firmware" >> /etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian/ bookworm-updates main contrib non-free non-free-firmware" >> /etc/apt/sources.list

# Install system dependencies
RUN apt-get clean && \
    apt-get update && \
    apt-get install -y \
    default-libmysqlclient-dev \
    pkg-config \
    build-essential \
    python3-dev \
    curl && \
    rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install dependencies using Alibaba PyPI mirror
COPY requirements.txt /app/
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ \
    --trusted-host mirrors.aliyun.com \
    --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Copy environment file
COPY .env.production /app/.env

# Set Django settings module
ENV DJANGO_SETTINGS_MODULE=config.settings.production

# Collect static files
RUN python manage.py collectstatic --noinput

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "config.wsgi:application"]