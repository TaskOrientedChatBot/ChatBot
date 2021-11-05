from typing import Union

from tts.TransformerTTS.data.text.symbols import all_phonemes
from tts.TransformerTTS.data.text.tokenizer import Phonemizer, Tokenizer


class TextToTokens:
    def __init__(self, phonemizer: Phonemizer, tokenizer: Tokenizer):
        self.phonemizer = phonemizer
        self.tokenizer = tokenizer
    
    def __call__(self, input_text: Union[str, list]) -> list:
        phons = self.phonemizer(input_text)
        tokens = self.tokenizer(phons)
        return tokens
    
    @classmethod
    def default(cls, language: str, add_start_end: bool, with_stress: bool, model_breathing: bool, alphabet, njobs=1):
        phonemizer = Phonemizer(language=language, njobs=njobs, with_stress=with_stress)
        tokenizer = Tokenizer(add_start_end=add_start_end, model_breathing=model_breathing, alphabet=alphabet)
        return cls(phonemizer=phonemizer, tokenizer=tokenizer)

