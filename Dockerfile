FROM python:3.12.6

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH /app

WORKDIR /app

COPY ./requirements/requirements.txt requirements.txt
COPY abc_back ./abc_back
COPY conf ./conf

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        tzdata \
        gcc \
        musl-dev \
        libc-dev \
        libcurl4-gnutls-dev \
        librtmp-dev \
        postgresql-client-common \
        postgresql-client \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create folder for gunicorn logs
RUN mkdir -p /var/log/gunicorn

# Install project dependencies
RUN pip install --no-deps -r requirements.txt

CMD ["bash"]
