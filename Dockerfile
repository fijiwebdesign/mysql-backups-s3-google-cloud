# Use the official Python image as the base image
FROM python:3.9-slim

# Install mysql-client
RUN apt-get update && apt-get install -y default-mysql-client

# Set the working directory in the container
WORKDIR /app

# Copy the Python script and the utils directory into the container
COPY mysql_backup.py .
COPY utils utils/
COPY backups backups/
RUN chmod a+rwx -R backups
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Set the command to run the Python script
CMD ["python", "mysql_backup.py"]
