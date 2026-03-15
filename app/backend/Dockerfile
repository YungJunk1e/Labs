FROM python:3.14-slim
RUN pip install --upgrade pip
WORKDIR /backend-app
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENTRYPOINT ["python3","main.py"]
