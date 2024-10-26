FROM python:3.11.8
WORKDIR /ToStix
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY src/requirements.txt ./requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
COPY . .