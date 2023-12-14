FROM python:3.7-slim-stretch

ENV PORT 8080
RUN apt-get -y update && apt-get -y install build-essential gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . .
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app