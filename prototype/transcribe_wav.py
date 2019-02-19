import argparse
import json
import pyaudio
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types


# set up I/O files and parse arguments
output_file = "transcript_info.json"

parser = argparse.ArgumentParser(description="Takes in a wav file and outputs "\
                                   "the transcript info in a json file.",
                                 prog="transcribe_wav.py")

parser.add_argument('input_file', help="input wav file to transcribe")
args = parser.parse_args()


# Instantiates a client
client = speech.SpeechClient()

# read in audio file
with open(args.input_file, "rb") as audio_file:
    content = audio_file.read()
    audio = types.RecognitionAudio(content=content)

# configure and call recognition API
config = types.RecognitionConfig(
    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
    language_code='en-US',
    enable_word_time_offsets=True,
    enable_automatic_punctuation=True)

response = client.recognize(config, audio)


# build object to save
transcript = []

for result in response.results:
    chunk_trans = dict()
    chunk_trans["transcript"] = result.alternatives[0].transcript
    chunk_trans["confidence"] = result.alternatives[0].confidence
    chunk_trans["word_timings"] = list(map(lambda word: dict(word = word.word,
                                                             start_time = word.start_time.seconds + word.start_time.nanos * 1e-9,
                                                             end_time =  word.end_time.seconds + word.end_time.nanos * 1e-9),
                                           result.alternatives[0].words))
    transcript.append(chunk_trans)

# print json file
with open(output_file, "w") as file_out:
    json.dump(transcript, file_out, indent = 2)