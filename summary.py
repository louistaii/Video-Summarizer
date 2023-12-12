import os
import openai
from pytube import YouTube


API_KEY = open("API_KEY", "r").read()
openai.api_key = API_KEY

def summarise():
    lines = open("transcription.txt", "r").read()
    print("\nSummarising...")
    
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages= [
            {"role": "system", "content": "You are a helpful assistant that summarises the given text into short yet detailed notes, prioritizing statistics, formulas and equations"},
            {"role": "user", "content": lines}]
            )
    
    output = response.choices[0].message.content.strip()
    print(output)


def converttotext():
    audio_file = open("vid.mp4", "rb")
    print("\nGathering data...")
    transcript = openai.audio.translations.create(
        model="whisper-1", 
        file=audio_file, 
        response_format="text"
    )
    with open("transcription.txt", "w") as f:
        f.write(transcript)



def main():

    link = input('Insert video link: ')
    yt =  YouTube(link)
    video = yt.streams.get_lowest_resolution()
    print("Downloading video...")
    video.download( filename="vid.mp4")
    if os.path.exists("vid.mp4"):
        converttotext()
        summarise()
    else:
        print("Download failed")
    

    if os.path.exists("vid.mp4"):
        os.remove("vid.mp4")





if __name__ == "__main__":
    main()