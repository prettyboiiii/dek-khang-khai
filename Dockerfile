FROM python:3.8

RUN apt-get update
RUN apt-get -y install libopus-dev ffmpeg

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt

COPY . .

CMD [ "python", "main.py" ]