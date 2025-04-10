# Use the official Python 3.12-slim image as the base image
FROM python:3.12-slim

# Install ffmpeg and other necessary system dependencies
RUN apt-get update && apt-get install -y ffmpeg

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /
COPY env.ini /env.ini

# Check the ini file and conditionally install openai-whisper if [Local] use_local_whisper=True
RUN if grep -q "^\[Local\]" /env.ini && grep -q "^use_local_whisper=True" /env.ini; then \
    pip install --no-cache-dir openai-whisper; \
fi

# Make port 9091 available to the world outside this container
EXPOSE 9091

# Run the application when the container launches
CMD ["python", "main.py"]
