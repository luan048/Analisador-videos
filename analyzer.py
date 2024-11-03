from pytubefix import YouTube
from dotenv import load_dotenv
import os
import openai

load_dotenv()

apiKey = os.getenv("API-KEY")

# API chatgpt
openai.api_key = apiKey

def downloadVideo(video_url) :
    # Download do audio do video
    video = YouTube(video_url)
    only_audio = video.streams.filter(only_audio=True, file_extension='mp4').first()

    # Nome do arquivo em audio
    audio_path = "auth.mp4"
    only_audio.download(filename=audio_path)

    return audio_path

#Converte audio em text
def transcribeAudio(audio_path) :
    with open(audio_path, "rb") as audio_file:
        transcription = openai.Audio.transcribe(
            model="whisper-1",
            file=audio_file
        )

    return transcription['text']

def summarizeText(text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Resuma  o seguinte text:\n\n{text}",
        max_tokens=150
    )
    return response['choices'][0]['text'].strip()

def analyze_video(video_url):
    print("Baixando e extraindo áudio...")
    audio_path = downloadVideo(video_url)

    print("Transcrevendo áudio...")
    transcription_text = transcribeAudio(audio_path)

    print("Resumindo transcrição...")
    summary = summarizeText(transcription_text)

    os.remove(audio_path)

    return summary

video_url = input('Digite a URL do video: ')
summary = analyze_video(video_url)
print("Resumo do Video:\n", summary)