import os
# import argparse
import json
import tempfile
from scipy.io import wavfile as wf
import numpy as np
from math import ceil
# import pyaudio
import wave
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types


def write_output(trans_response, time_offset, output_file=""):
    # build object to save
    transcript = []

    for result in trans_response.results:
        sec_info = dict()
        sec_info["transcript"] = result.alternatives[0].transcript
        sec_info["confidence"] = result.alternatives[0].confidence
        sec_info["word_timings"] = list(map(lambda word: dict(word = word.word,
                                                              start_time = time_offset + word.start_time.seconds + word.start_time.nanos * 1e-9,
                                                              end_time = time_offset + word.end_time.seconds + word.end_time.nanos * 1e-9),
                                            result.alternatives[0].words))
        transcript.append(sec_info)

    return transcript
    # # print json file
    # with open(output_file, "w") as file_out:
    #     json.dump(transcript, file_out, indent = 2)


def read_chunks(input_file):
    chunks = []
    rate, data = wf.read(input_file)
    duration = len(data) / rate
    num_chunks = ceil(duration / 55)

    for chunk in np.array_split(data, num_chunks):
        temp = tempfile.TemporaryFile()
        wf.write(temp, rate, chunk)
        # print(len(chunk)/rate)
        chunks.append(temp.read())
        temp.close()

    return chunks, (len(data) / (num_chunks*rate))


def transcribe(dir_name, input_file, rec_num):
    # Instantiates a client
    client = speech.SpeechClient()

    input_file = os.path.join(dir_name, input_file)

    # configure and call recognition API
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code='en-US',
        enable_word_time_offsets=True,
        enable_automatic_punctuation=True)

    # read in audio file
    transcript = []

    chunks, time_offset = read_chunks(input_file)

    i = 0
    for chunk in chunks:

        audio = types.RecognitionAudio(content=chunk)

        response = client.recognize(config, audio)

        transcript.append(write_output(response, i*time_offset))
        i += 1

    output_file = os.path.join(dir_name,
                               "transcript_info_" + str(rec_num) + ".json")
    # write_output(response, output_file)
    with open(output_file, "w") as file_out:
        json.dump(transcript, file_out, indent = 2)
