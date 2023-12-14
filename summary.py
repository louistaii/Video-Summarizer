
import os               
import math
from urllib.parse import urlparse

#external python modules
import openai                   #API
from pytube import YouTube      #downloads audio off youtube
from pydub import AudioSegment  #for audio file manipulation

#loads API_KEY
API_KEY = open("API_KEY", "r").read()
openai.api_key = API_KEY


def progress_bar(current, total):                #shows progress 
    percent = 100 * (current/ float(total))
    bar ='█' * int(percent) + '-' * (100 - int(percent))
    print(f"\r|{bar}| {percent:.2f}%", end = "\r")



def summarize():
    lines = open("transcription.txt", "r", encoding="utf-8").read()   #encoding utf-8 used to prevent errors with openai
    print("\nSummarising...\n")
    
    response = openai.chat.completions.create(           #openai chat completion api
        model="gpt-3.5-turbo-1106",                      #use gpt-4 for long transcriptions
        messages= [
            {"role": "system", "content": "Act as a text summarizer to create a concise summary of the text provided. Express the key points and concepts written in the original text without adding your interpretations. Ignore advertisements"},
            {"role": "user", "content": lines}]
            )
    
    output = response.choices[0].message.content.strip() #stripping response from api into readible format
    print(output)

    with open("summary.txt", "w" , encoding="utf-8") as f: 
        f.write(output)



def converttotext(audiodir):
    audio_file = open(audiodir, "rb")                   #loads mp3 file
    transcript = openai.audio.translations.create(      #transcibe/translate with openai API
        model="whisper-1", 
        file=audio_file, 
        response_format="text"
    )
    with open("transcription.txt", "a" , encoding="utf-8") as f:     #encoding utf-8 used to prevent errors with openai
        f.write(transcript)


def splitaudio(audio, splits):                     #split audio file into files of 20mins each

    #erase previous transcription.txt
    if os.path.exists("transcription.txt"):
        os.remove("transcription.txt")


    #splits audio into 20min (1200s) audio files
    progress_bar(0, splits)
    for i in range(splits):
        start = i * 1200 * 1000
        end = (i + 1) * 1200 * 1000
        split_audio = audio[start:end]
        output_path = os.path.join(f"part{i+1}.mp3")
        split_audio.export(output_path, format="mp3")                             
        converttotext(output_path)                      #transcribing individual smaller audio file 
        progress_bar(i+1, splits)



def uri_validator(link):        #tests for valid url
    try:
        result = urlparse(link)
        return all([result.scheme, result.netloc])
    except:
        return False



def main():

    link = input('Insert video directory/link: ')
   
    #fetch audio file
    if os.path.exists(link):
        audiodir = link
    elif uri_validator(link) == True:
        yt =  YouTube(link)
        t=yt.streams.filter(only_audio=True)
        print("\nDownloading audio...")
        t[0].download(filename="audio.mp3")
        audiodir = "audio.mp3"
    else:
        print("\nInvalid file directory or YouTube link")
        quit()
        
    
    audio = AudioSegment.from_file(audiodir)
    audiolength = math.ceil(audio.duration_seconds)
    splits = math.ceil(audiolength / (1200))



    #processing lengthy audio files (>30mins)
    if (audiolength >1800):
        print(f"Splitting file (estimate: {splits} mins)...")
        splitaudio(audio,splits)
    else:
        print("Transcribing...")
        converttotext(audiodir)

    summarize()

    #remove splitted mp3 files to reduce clutter
    for i in range(splits):
        if os.path.exists(f"part{i+1}.mp3"):
            os.remove((f"part{i+1}.mp3"))
        else:
            quit





if __name__ == "__main__":
    main()