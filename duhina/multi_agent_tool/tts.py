from gtts import gTTS
from pathlib import Path
from playaudio import playaudio

def toSpeech(text: str):
    lang = 'en'

    myobj = gTTS(text=text, lang=lang, slow=False)
    audio_path = (Path(__file__).parent / "./audio.mp3").resolve()
    
    myobj.save(audio_path)
    playaudio(audio_path)


if __name__ == '__main__':
    toSpeech('Test 1234')