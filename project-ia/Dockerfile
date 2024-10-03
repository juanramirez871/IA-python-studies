FROM ubuntu:latest


RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv

WORKDIR /app

COPY . .

COPY ./requirements.txt .


RUN python3 -m venv /app/venv
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt


EXPOSE 4000


CMD ["/app/venv/bin/python", "-m", "uvicorn", "app.__main__:app", "--host", "0.0.0.0", "--port", "4000"]