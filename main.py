import os
import pathlib
from urllib.parse import urlparse

from pytube import YouTube
from transformers import pipeline

import tiktoken
import whisper


path = pathlib.Path(__file__).parent.resolve()

def summarize(text):
    summarizer = pipeline('summarization')
    output = summarizer(text, max_length=130, min_length =10, do_sample=False)
    summary = output[0]['summary_text'] 
    with open(f"{path}/textfiles/summary.txt","a" , encoding="utf-8") as f:
        f.write(summary)
    f.close()


def splittext(text, limit, encoding):
    tokens = encoding.encode(text)
    parts = []
    text_parts = []
    current_part = []
    current_count = 0

    for token in tokens:
        current_part.append(token)
        current_count += 1

        if current_count >= limit:
            parts.append(current_part)
            current_part = []
            current_count = 0

    if current_part:
        parts.append(current_part)

    for part in parts:
        text = [
            encoding.decode_single_token_bytes(token).decode("utf-8", errors="replace")
            for token in part
        ]
        text_parts.append("".join(text))

    return text_parts



def transcribe(audiodir):
    model = whisper.load_model("base")
    print("Transcribing...this may take some time...")
    result = model.transcribe(audiodir)

    with open(f"{path}/textfiles/transcription.txt" , "w" , encoding="utf-8") as f:
        f.write(result["text"])

    print("Done!")
    f.close()


def url_validator(link):        #tests for valid url
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
    elif url_validator(link) == True:
        yt =  YouTube(link)
        t=yt.streams.filter(only_audio=True)
        
        if os.path.exists(f"{path}/audio.mp3"):
            os.remove(f"{path}/audio.mp3")
        
        print("\nDownloading audio...")
        t[0].download(f'{path}', filename = "audio.mp3")
        audiodir = "audio.mp3"
    else:
        print("Invalid URL or Directory")


    transcribe(audiodir)
    
    if os.path.exists(f"{path}/textfiles/summary.txt"):
        os.remove(f"{path}/textfiles/summary.txt")
    
    transcription = open(f"{path}/textfiles/transcription.txt", "r", encoding="utf-8").read()
    
    encoding = tiktoken.get_encoding("cl100k_base")
    text = splittext(transcription, 1000, encoding)
    for part in text:
        summarize(part)

    print("\n\nSummary:")
    output = open(f"{path}/textfiles/summary.txt", "r", encoding="utf-8").read()
    print(output)



if __name__ == "__main__":
    main()