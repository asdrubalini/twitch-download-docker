FROM python:3.7.7

RUN apt update -y
RUN apt upgrade -y

RUN apt install ffmpeg -y

COPY ./TwitchDownloader/ /src/

WORKDIR /src/

RUN pip install -r ./requirements.txt

CMD ["python", "-u", "./__main__.py"]
