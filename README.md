# Video Summarizer
Transcribe and summarize local/ downloaded Youtube videos for faster consumption of information.  
Ceated to summarize Abdul Bari YouTube lectures because playing on 2x speed isn't for everyone

## Quick Start
Clone this repository and run ```pip install -r requirements.txt``` in the directory to install dependencies needed  
Launch "run.bat" or "main.py" file to start

## Features
- Downloading of Youtube video audio using Pydub
- Transcription of audio using OpenAI Whisper
- Summarization of transcription using Huggingface transformers
- Allows for longer text summary by splitting text into parts and summarizing each part individually
- Transcription and summary of local video/audio files can be done offline
