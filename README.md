# Video Summarizer
Transcribe and summarize local/ downloaded videos for faster consumption of information.  
Ceated to summarize Abdul Bari YouTube lectures because playing on 2x speed isn't for everyone

## Features
- Download audio off Youtube videos using [Pytube](https://pytube.io/en/latest/) or load local videos / audios
- Transcription and summary of audio files using [Openai](https://github.com/openai/openai-python) API (gpt-3.5-turbo-1106) 
- Allows for transcription of longer audio files by splitting and processing the audio files using [Pydub](https://github.com/jiaaro/pydub)

## Notes
- Tested on Python 3.11  
- Estimated run time: 4 mins for a 1 hr video                                                                                              
- Get your own [API KEY](https://openai.com/pricing) and paste into "API_KEY" file
- Run ```pip install -r requirements.txt``` in the directory of the repository and then launch "run.bat"
