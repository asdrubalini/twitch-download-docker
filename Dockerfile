FROM python:3.7.7-stretch

RUN apt update -y
RUN apt upgrade -y
RUN apt install wget -y

RUN mkdir /ffmpeg
WORKDIR /ffmpeg
RUN wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
RUN tar xvf ffmpeg*.tar.xz && rm -f *.tar.xz
RUN mv ffmpeg* bin/
ENV PATH="/ffmpeg/bin/:${PATH}"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ADD TwitchDownloader/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

RUN useradd -m -d /home/dev dev
RUN chown -R dev /home/dev/
USER dev

COPY --chown=dev ./TwitchDownloader/ /home/dev/src/

WORKDIR /home/dev/src/
CMD ["python", "-u", "./__main__.py"]
# CMD ["sleep", "infinity"]
