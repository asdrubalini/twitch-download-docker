import streamlink
import os
import subprocess
import time
import pathlib
import sys

from datetime import datetime


twitch_username = os.getenv("TWITCH_USERNAME")
sleep_seconds = os.getenv("SLEEP_SECONDS")
download_dir = os.getenv("DOWNLOAD_DIR")

if twitch_username == "" or twitch_username is None:
    print("twitch_username env must be specified")
    exit(1)

if sleep_seconds == "" or sleep_seconds is None:
    print("sleep_seconds env must be specified")
    exit(1)

if download_dir == "" or download_dir is None:
    print("download_dir env must be specified")
    exit(1)

sleep_seconds = int(sleep_seconds)


def get_live_url():
    stream_url = streamlink.streams("https://www.twitch.tv/" + twitch_username)

    if not stream_url:
        return

    return stream_url["best"].url


def ffmpeg_download_live(stream_url: str):
    now = datetime.now()
    live_filename = download_dir + twitch_username + "_" + now.strftime("%m_%d_%Y-%H_%M_%S") + ".mp4"

    # Measure time
    start_time = time.time()
    subprocess.call(
        ["ffmpeg", "-i", stream_url, "-c", "copy", live_filename],
        stdout=open(os.devnull, "w")
    )

    return time.time() - start_time


if __name__ == "__main__":
    print("starting script")
    pathlib.Path(download_dir).mkdir(parents=True, exist_ok=True)

    while True:
        print("checking if user is streaming")
        stream_url = get_live_url()

        # If the user is currently streaming, start downloading until the stream is over
        if stream_url:
            print(twitch_username, "has just started a new live stream")
            duration = ffmpeg_download_live(stream_url)
            print(twitch_username, "live stream has just terminated. It lasted", duration / 60, "minutes")
            sys.exit()

        time.sleep(sleep_seconds)
