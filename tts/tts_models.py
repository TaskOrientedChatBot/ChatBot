from google.cloud import texttospeech
from utils.paths import get_project_root
from typing import Dict
from gtts import gTTS
import subprocess
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(get_project_root(),
                                                            "artificialintelligence-253111-7c9f9a54cb61.json")


class TTS:

    def __init__(self):
        self._tmp_file = "tmp_file.mp3"

    def synthesize_text(self, text):
        raise NotImplementedError

    def play(self, audio):
        raise NotImplementedError


class GooglePkgTTS(TTS):

    def __init__(self, lang="ro", audio_tempo: float = 1.0):
        super().__init__()
        self.audio_tempo = audio_tempo
        self.lang = lang

    def synthesize_text(self, text):
        audio = gTTS(text=text, lang=self.lang, slow=False)
        return audio

    def play(self, audio):
        audio.save(self._tmp_file)

        if self.audio_tempo != 1.:
            subprocess.call(
                ["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", self._tmp_file, "-filter:a",
                 "atempo={}".format(self.audio_tempo), "-vn", self._tmp_file])

        subprocess.call(["cmdmp3", self._tmp_file], stdout=subprocess.DEVNULL)
        os.remove(self._tmp_file)


class GoogleCloudTTS(TTS):
    default_voice_config = {
        "language_code": "ro-RO",
        "name": "ro-RO-Wavenet-A",
        "ssml_gender": texttospeech.SsmlVoiceGender.FEMALE,
    }

    default_audio_config = {
        "audio_encoding": texttospeech.AudioEncoding.MP3,
    }

    def __init__(self, voice_selection_config: Dict = None, audio_config: Dict = None):
        super().__init__()
        self.client = texttospeech.TextToSpeechClient()
        self.voice_selection_config: Dict = voice_selection_config
        self.audio_config: Dict = audio_config

        self.__sanity_check()
        self.voice = texttospeech.VoiceSelectionParams(voice_selection_config)
        self.audio = texttospeech.AudioConfig(self.audio_config)

    def __sanity_check(self):
        def update_config(check_config, default_config):
            for key, value in default_config.items():
                if key not in check_config:
                    check_config[key] = value

        if self.voice_selection_config is None:
            self.voice_selection_config = self.default_voice_config
        else:
            update_config(self.voice_selection_config, GoogleCloudTTS.default_voice_config)

        if self.audio_config is None:
            self.audio_config = self.default_audio_config
        else:
            update_config(self.audio_config, GoogleCloudTTS.default_audio_config)

    def synthesize_text(self, text):
        input_text = texttospeech.SynthesisInput(text=text)
        response = self.client.synthesize_speech(
            input=input_text, voice=self.voice, audio_config=self.audio
        )

        return response.audio_content

    def play(self, audio):
        with open(self._tmp_file, "wb") as out:
            out.write(audio)

        subprocess.call(["cmdmp3", self._tmp_file], stdout=subprocess.DEVNULL)
        os.remove(self._tmp_file)

class ROTacotron2WaveRNNTTS(TTS):
    def __init__(self):
        super().__init__()

    def synthesize_text(self, text):
        pass

    def play(self, text):
        subprocess.call(["python",
                        "extern_tts_fork\inference.py",
                        "--text",
                        text], shell=True)
        subprocess.call(["cmdmp3",
                        "reply.wav"],
                        stdout=subprocess.DEVNULL)

        os.remove("reply.wav")

class ROTransformerTTS(TTS):
    def __init__(self):
        super().__init__()

    def synthesize_text(self, text):
        pass

    def play(self, text):
        subprocess.call(["python",
                        "tts\transformer_tts_predict.py",
                        "-t",
                        text,
                        "-p",
                        "TaskOrientedChatBotBlobs\TransformerTTS\Adr",
                        "-o",
                        "."], shell=True)

        subprocess.call(["cmdmp3",
                        ".\outputs\reply.wav"],
                        stdout=subprocess.DEVNULL)

if __name__ == "__main__":
    _text = "Ana are mere și pere."

    _voice_config = {
        "name": "ro-RO-Wavenet-A",
        "ssml_gender": texttospeech.SsmlVoiceGender.FEMALE,
    }

    _audio_config = {}
    gtts = GoogleCloudTTS(_voice_config, _audio_config)
    _audio = gtts.synthesize_text(_text)
    gtts.play(_audio)

    gtts2 = GooglePkgTTS()
    _audio = gtts2.synthesize_text(_text)
    gtts2.play(_audio)
