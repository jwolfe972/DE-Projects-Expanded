FROM python:3.10

WORKDIR /app

COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY .. .


CMD ["python3", "kafka-example-producer.py"]
