# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.11-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

ENV discord_bot_token="OTQwODU5MTQzOTQ0ODE4NzI4.GoUhF9.L8WcdyUp4pWC1diQ6y0s6e4ry-op8y7z94kBWM"

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "src/run.py"]