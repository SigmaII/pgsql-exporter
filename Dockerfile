FROM python:3.12-slim
WORKDIR /usr/local/app

COPY output.json ./
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
EXPOSE 8080

RUN useradd app
USER app


CMD ["python3", "src/main.py"]