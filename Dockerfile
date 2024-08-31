# Stage 1: Build the base image with dependencies
FROM python:3.12-slim as base

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Stage 2: Build the final image
FROM python:3.12-slim

# Copy the dependencies from the base image
COPY --from=base /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=base /usr/local/bin /usr/local/bin
COPY --from=base /usr/bin/ffmpeg /usr/bin/ffmpeg

# Copy the current directory contents into the container at /app
COPY . /
COPY env.ini /env.ini

# Make port 9091 available to the world outside this container
EXPOSE 9091

# Run app.py when the container launches
CMD ["python", "main.py"]