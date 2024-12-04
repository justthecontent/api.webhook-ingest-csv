FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

# Create a volume mount point
VOLUME ["/data"]

# Run using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
