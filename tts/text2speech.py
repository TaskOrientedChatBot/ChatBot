import os
import re

import requests
import subprocess
from gtts import gTTS


def chatbot_tts():
    sender = "Me"
    bot_message = ""
    while bot_message != "Bye":
        message = input("Me: ")
        r = requests.post("http://localhost:5002/webhooks/rest/webhook", json={"sender": sender, "message": message})
        print("Bot says: ")
        for i in r.json():
            bot_message = i["text"]
            print(bot_message)
            links = re.findall(r'(https?://[^\s]+)', bot_message)
            for idx, link in enumerate(links):
                bot_message = bot_message.replace(link, '')
            audio = gTTS(text=bot_message, lang="ro", slow=False)
            save_and_play_mp3(audio)


def save_and_play_mp3(audio):
    audio.save("file.mp3")
    subprocess.call(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", "file.mp3", "-filter:a", "atempo=1.6", "-vn",
                     "file_output.mp3"])
    subprocess.call(["cmdmp3", "file_output.mp3"], stdout=subprocess.DEVNULL)
    os.remove("file.mp3")
    os.remove("file_output.mp3")


if __name__ == "__main__":
    chatbot_tts()
