"""
This file contains the functions required to record continuous audio and record
it to disk.
"""

import queue
import sys
from datetime import datetime
import os
import signal
import errno
import sounddevice as sd
import soundfile as sf
# import numpy



DEVICE = 2
CHANNELS = 1
WAVE_OUTPUT_FILE_HEADER = "recording_"


'''
Testing function to create new director, moved to interface file.
TODO:: Delete later.
'''
def create_new_dir():
    mydir = os.path.join(os.getcwd(),
                         datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    try:
        os.makedirs(mydir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            # This was not a "directory exist" error..
            raise  RuntimeError("not a dir exists error")
    return mydir


'''
Records live audio from microphone and save it to file recording_.wav in the
director passed.  If no directory is specified it is saved at the current path.
'''
def record_audio(dir_name=""):

    filename = WAVE_OUTPUT_FILE_HEADER + ".wav"
    filename = os.path.join(dir_name, filename)

    device_info = sd.query_devices(DEVICE, 'input')
    rate = int(device_info['default_samplerate'])

    q = queue.Queue()

    def callback(indata, frames, time, status):
        del frames, time
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        q.put(indata.copy())

    with sf.SoundFile(filename, mode='x', samplerate=rate,
                      channels=CHANNELS) as file:
        signal.signal(signal.SIGINT, lambda n, f: (file.close(),
                                                   print("* done recording"),
                                                   exit(0)))
        signal.signal(signal.SIGTERM, lambda n, f: (file.close(),
                                                    print("* done recording"),
                                                    exit(0)))

        with sd.InputStream(samplerate=rate, device=DEVICE, channels=CHANNELS,
                            callback=callback):
            print("* recording")
            while True:
                file.write(q.get())


# dir_name = create_new_dir()
# record_audio(dir_name)
