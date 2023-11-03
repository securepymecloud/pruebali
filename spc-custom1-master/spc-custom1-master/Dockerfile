# Use the official Python base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config supervisor \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . .

# Set the environment variable for Flask
ENV FLASK_APP=app.py

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose the port on which the Flask app will run
EXPOSE 5000
EXPOSE 5001
EXPOSE 5002
EXPOSE 5003
EXPOSE 5004
EXPOSE 5005

# Run the Flask app when the container starts
# CMD ["flask", "run", "--host=0.0.0.0"]
CMD [ "/usr/bin/supervisord" ]