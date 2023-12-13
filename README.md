# Video Summarizer

## Description  
- Created to summarize Abdul Bari YouTube lectures because playing on 2x speed isn't for everyone
- Download YouTube videos using Pytube or load local videos                                                                                                     
- Transcribes and summarizes video content using OpenAI API                                                                                                                       
- Get your own [API KEY](https://openai.com/pricing) and paste into "API_KEY" file
- Tested on Python 3.11


## Updates
131223
- Loading of local videos
- Splitting of longer audio files using Pydub to enable transcription of longer videos
- Tested up to audio length: 1hr 20mins
- Openai API unable to process and summarise large text (videos with extensive transcription)