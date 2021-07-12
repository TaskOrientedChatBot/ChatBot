from tts.tts_models import TTS, GooglePkgTTS, GoogleCloudTTS, ROTacotron2WaveRNNTTS
import argparse
import requests
import re


def chat_bot_tts(audio_synthesis: TTS, config: dict):
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

            if config["model"] != "ROTacotron2WaveRNN":
                audio = audio_synthesis.synthesize_text(text=bot_message)
                audio_synthesis.play(audio)
            else:
                audio_synthesis.play(bot_message)


def main(config):
    if config["model"] == "gcloud":
        from google.cloud import texttospeech
        # start it with defaults
        _voice_config = {
            "name": "ro-RO-Wavenet-A",
            "ssml_gender": texttospeech.SsmlVoiceGender.FEMALE,
        }

        _audio_config = {}

        gtts = GoogleCloudTTS(_voice_config, _audio_config)
    elif config["model"] == "gtts":
        gtts = GooglePkgTTS()
    elif config["model"] == "ROTacotron2WaveRNN":
        gtts = ROTacotron2WaveRNNTTS()
    else:
        raise ValueError("There's no synthesiser with name: {}".format(config["model"]))

    chat_bot_tts(gtts, config)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="gcloud", help="Select model to be used for playing sound.")
    args = parser.parse_args()
    _config = {
        "model": args.model
    }
    main(_config)
