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
        transcription = openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        ).text

    return transcription['text']

def summarizeText(transcription):
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
             "content": """
                Você é um assistente que resume videos, responda tudo com formatação Markdown.
            """},

            {"role": "user",
             "content": f"Descreva o seguinte video: {transcription}"}
        ])
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