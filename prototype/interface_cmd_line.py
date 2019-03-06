"""Command Line Interface for Instrumented Classroom Project"""


from datetime import datetime
import os
# import signal
import errno
from multiprocessing import Process

## Import own-code
from audio_rec import record_audio
from face_tracking import detectAndTrackMultipleFaces
from transcribe_wav import transcribe
# from test_mult_proc import f_rec, f_busy

recording = False
busy = False

p_rec = None
p_vid = None
p_trans = None


""" This function creates a new director in the current path to store output
into.  This directory name is the current time stamp, as to avoid collisions.
If such a directory already exists we do nothing and use it.
"""
def create_new_dir():
    new_dir = os.path.join(os.getcwd(),
                           datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    try:
        os.makedirs(new_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            # This was not a "directory exist" error..
            # raise  RuntimeError("not a dir exists error")
            raise e
    return new_dir



## Model button with user input

## while user_input True: record audio/video
## on exit save data in director generated


# Type "rec" to record and "stop" to stop the recording and start the
# post-processing

def loop():
    global recording, busy
    dir_name = create_new_dir()
    while True:
        if (not recording and not busy):                    # R = F and B = F
            print("Press r to start recording and s to stop recording: ")
            rec = input()
            while rec != "r":
                print("Press r to start recording: ")
                rec = input()
            recording = True
            busy = False
            p_rec = Process(target=record_audio, args=(dir_name,))
            p_vid = Process(target=detectAndTrackMultipleFaces, args=(dir_name,))
            p_rec.start()
            p_vid.start()
        elif recording:                                     # R = T and B = _
            halt = input()
            while halt != "s":
                print("Press s to stop recording: ")
                halt = input()
            recording = False
            busy = True
            p_rec.terminate()
            p_vid.terminate()
            print("* busy")
            p_trans = Process(target=transcribe, args=(dir_name, "recording_.wav"))
            p_trans.start()

        else:                                              # R = F and B = T
            if p_trans.is_alive():
                pass
            else:
                print("To record again, press r, otherwise press any other key: ")
                rec = input()
                if rec == 'r':
                    print("Don't have this functionality yet.  We're working on it :)")
                exit(0)  # add post processing here
            exit(0)


if __name__ == '__main__':
    try:
        loop()
    except KeyboardInterrupt:
        exit(0)
