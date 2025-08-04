# Use official Python image
FROM python:3.10-slim

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .

RUN apt-get update && apt-get install -y default-libmysqlclient-dev gcc

RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Copy startup script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose Django port
EXPOSE 8000

# Run the script
ENTRYPOINT ["/entrypoint.sh"]
