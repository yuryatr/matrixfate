FROM python:3.12-slim-bullseye

        
WORKDIR /var/www/app
        
# install pypi packages
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# COPY . .
# 

# Make port 8080 available to the world outside this container
EXPOSE 8080
