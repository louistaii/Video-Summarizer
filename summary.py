
import os               
import math

#run pip install on openai, pytube and pydub
import openai
from pytube import YouTube      #downloads audio off youtube
from pydub import AudioSegment  #for audio file manipulation

#loads API_KEY
API_KEY = open("API_KEY", "r").read()
openai.api_key = API_KEY


def summarize():
    lines = open("transcription.txt", "r", encoding="utf-8").read()   #encoding utf-8 used to prevent errors with openai
    print("Summarising...\n")
    
    response = openai.chat.completions.create(           #openai chat completion api
        model="gpt-3.5-turbo-1106",
        messages= [
            {"role": "system", "content": "You are a research assistant that summarises the given text into short yet detailed notes. Prioritize including statistics, formulas and equations. Ignore advertisements"},
            {"role": "user", "content": lines}]
            )
    
    output = response.choices[0].message.content.strip() #stripping response from api into readible format
    print(output)



def converttotext(audiodir):
    audio_file = open(audiodir, "rb")                   #loads mp3 file
    print("Transcribing...")
    transcript = openai.audio.translations.create(      #transcibe/translate with openai API
        model="whisper-1", 
        file=audio_file, 
        response_format="text"
    )
    with open("transcription.txt", "a" , encoding="utf-8") as f:     #encoding utf-8 used to prevent errors with openai
        f.write(transcript)


def splitaudio(audio, audiolength):                     #split audio file into files of 20mins each
    splits = math.ceil(audiolength / (1200))
    for i in range(splits):
        print(f"Splitting ({i+1} / {splits})...")
        start = i * 1200 * 1000
        end = (i + 1) * 1200 * 1000
        split_audio = audio[start:end]
        output_path = os.path.join(f"part{i+1}.mp3")
        split_audio.export(output_path, format="mp3")
        print("Completed")                              
        converttotext(output_path)                      #transcribing individual smaller audio file 
        if os.path.exists(output_path):                 #delete smaller audio file to prevent clutter
            os.remove(output_path)



def main():
    
    link = input('Insert video directory/link: ')
    
    #fetch audio file
    if os.path.exists(link):
        audiodir = link
    else:
        yt =  YouTube(link)
        t=yt.streams.filter(only_audio=True)
        print("\nDownloading audio...")
        t[0].download(filename="audio.mp3")
        audiodir = "audio.mp3"
    
    #erase previous transcription.txt
    if os.path.exists("transcription.txt"):
        os.remove("transcription.txt")

    audio = AudioSegment.from_file(audiodir)
    audiolength = audio.duration_seconds

    #processing lengthy audio files
    if (audiolength >1800):
        print(f"Audio file needs splitting: {audiolength}s")
        splitaudio(audio,audiolength)
    else:
        converttotext(audiodir)
    
    summarize()




if __name__ == "__main__":
    main()