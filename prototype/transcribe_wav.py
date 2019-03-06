import os
# import argparse
import json
# import pyaudio
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types


# set up I/O files and parse arguments

# parser = argparse.ArgumentParser(description="Takes in a wav file and outputs "\
#                                    "the transcript info in a json file.",
#                                  prog="transcribe_wav.py")

# parser.add_argument('input_file', help="input wav file to transcribe")
# args = parser.parse_args()


def write_output(trans_response, output_file):
    # build object to save
    print(output_file)
    transcript = []

    for result in trans_response.results:
        sec_info = dict()
        sec_info["transcript"] = result.alternatives[0].transcript
        sec_info["confidence"] = result.alternatives[0].confidence
        sec_info["word_timings"] = list(map(lambda word: dict(word = word.word,
                                                              start_time = word.start_time.seconds + word.start_time.nanos * 1e-9,
                                                              end_time =  word.end_time.seconds + word.end_time.nanos * 1e-9),
                                            result.alternatives[0].words))
        transcript.append(sec_info)
        print("confidence")

    # print json file
    with open(output_file, "w") as file_out:
        json.dump(transcript, file_out, indent = 2)



def transcribe(dir_name, input_file):
    # Instantiates a client
    client = speech.SpeechClient()

    input_file = os.path.join(dir_name, input_file)
    # read in audio file
    with open(input_file, "rb") as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    # configure and call recognition API
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code='en-US',
        enable_word_time_offsets=True,
        enable_automatic_punctuation=True)

    response = client.recognize(config, audio)

    output_file = os.path.join(dir_name, "transcript_info.json")
    write_output(response, output_file)
    exit(0)
