from gtts import gTTS
import os
from pathlib import Path

def toSpeech(text: str):
    lang = 'en'

    myobj = gTTS(text=text, lang=lang, slow=False)
    audio_path = (Path(__file__).parent / "./audio.mp3").resolve()
    
    myobj.save(audio_path)
    os.system(audio_path)


if __name__ == '__main__':
    toSpeech('Test 1234')