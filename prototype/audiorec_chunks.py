import pyaudio
import wave
import os
from datetime import datetime
import signal
# import multiprocess


CHUNK = 8192 #22050 #8192
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 30 #120
WAVE_OUTPUT_FILE_HEADER = "recording_"


def create_new_dir():
    mydir = os.path.join(os.getcwd(), datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    try:
        os.makedirs(mydir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise  RuntimeError("not a dir exists error") # This was not a "directory exist" error..
    return mydir


def write_chunk_to_wav(audio, filename, frames):
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def record_audio_chunk(filename):
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=2,
                    frames_per_buffer=CHUNK)

    print("* recording")

    signal.signal(signal.SIGINT, lambda n, f: (stream.stop_stream(), stream.close(),
                                               p.terminate(), 
                                               write_chunk_to_wav(p, filename,frames),
                                               exit(0)))
    signal.signal(signal.SIGTERM, lambda n, f: (stream.stop_stream(), stream.close(),
                                               p.terminate(), 
                                               write_chunk_to_wav(p, filename,frames),
                                               exit(0)))

    frames = []

    print(datetime.now().strftime('%H:%M:%S.%f'))

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print(datetime.now().strftime('%H:%M:%S.%f'))


    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()
    write_chunk_to_wav(p, filename, frames)


def record_audio_chunks_loop(dir_name):
    i = 1
    while True:
        filename = WAVE_OUTPUT_FILE_HEADER + str(i) + ".wav"
        filename = os.path.join(dir_name, filename)
        record_audio_chunk(filename)
        i += 1




dir_name = create_new_dir()
record_audio_chunks_loop(dir_name)
