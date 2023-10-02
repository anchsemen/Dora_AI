import os

import speech_recognition as sr
from pydub import AudioSegment


def transcribe(file):
    audio = AudioSegment.from_file(f"C:/Users/anchs/PycharmProjects/AI_friend/{file}")
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export("converted_audio.wav", format="wav")

    recognizer = sr.Recognizer()
    with sr.AudioFile("converted_audio.wav") as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language="ru-RU")
            print("Распознанный текст:", text)
        except sr.UnknownValueError:
            text = "Речь не распознана"
        except sr.RequestError as e:
            print("Ошибка при запросе к сервису Google; {0}".format(e))
            text = 'Извините, ошибка с сервером. Попробуйте позже'
    os.remove("1.wav")
    os.remove("converted_audio.wav")
    return text
