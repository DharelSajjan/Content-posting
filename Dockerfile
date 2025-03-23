# Use a lightweight Python base image
FROM python:3.9-slim

# Install system dependencies including Chromium and its driver
RUN apt-get update && apt-get install -y \
  wget \
  gnupg \
  unzip \
  chromium \
  chromium-driver \
  && rm -rf /var/lib/apt/lists/*

# Set environment variables so Selenium can find Chromium and its driver
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROME_DRIVER_PATH=/usr/bin/chromedriver

# Set the working directory inside the container
WORKDIR /app

# Copy only requirements first, to leverage Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# By default, run the scheduler (or whichever script is your main entry point)
CMD ["python", "linkedin_scheduler.py"]
