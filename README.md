# Video Summarizer
Transcribe and summarize local/ downloaded videos for faster consumption of information.
Ceated to summarize Abdul Bari YouTube lectures because playing on 2x speed isn't for everyone

## Notes
- Tested on Python 3.11  
- Overall estimated run time: 2mins for a 30min video
- Python modules needed: [Pytube](https://pytube.io/en/latest/), [Pydub](https://github.com/jiaaro/pydub), [Openai](https://github.com/openai/openai-python)
- Downloading of YouTube video audio using Pytube                                                                                                  
- Longer audio inputs are split and processed using Pydub
- Transcription and summarry done using OpenAI API (gpt-3.5-turbo-1106)                                                                                               
- Get your own [API KEY](https://openai.com/pricing) and paste into "API_KEY" file


## Updates
131223
- Loading of local videos
- Splitting of longer audio files using Pydub to enable transcription of longer videos
- Testing of transcription up to audio length: 1hr 20mins
- gpt-3.5-turbo-1106 unable to process videos with extensive transcription (use gpt 4 instead)
- Testing of summary with gpt-3.5-turbo-1106 up to audio length: 45mins

141223
- Saving of summary
- Added progress bar and indicators
- Fixed bugs removing audio files to reduce cluster
- Improved openai prompt
- Testing of invalid urls