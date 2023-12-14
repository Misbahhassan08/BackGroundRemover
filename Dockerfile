FROM python:3.8

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED True
ENV PORT 8080

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . .


CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app