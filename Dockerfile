# Set basic image with Linux and python 3.12
FROM python:3.12-slim
# Set env variable
ENV APP_HOME=/app
# Set workdir
WORKDIR $APP_HOME
# Copy all files
COPY . .
# Set dependencies in container
EXPOSE 3000/tcp
# Set storage dir
VOLUME $APP_HOME/storage
# Run app
ENTRYPOINT [ "python", "main.py"]