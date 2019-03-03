## Command Line Interface for Instrumented Classroom Project


from datetime import datetime
import os, signal

## Import own-code
from audio_rec import record_audio
from face_tracking import detectAndTrackMultipleFaces
from multiprocessing import Process
# import transcribe_wav
# from test_mult_proc import f_rec, f_busy

recording = False
busy = False

p_rec = None
p_vid = None

def create_new_dir():
    new_dir = os.path.join(os.getcwd(),
                         datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    try:
        os.makedirs(new_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            # This was not a "directory exist" error..
            raise  RuntimeError("not a dir exists error")
    return new_dir


def post_processing():
    pass

## Model button with user input

## while user_input True: record audio/video
## on exit save data in director generated


# Type "rec" to record and "stop" to stop the recording and start the
# post-processing

def loop():
    global recording, busy
    dir_name = create_new_dir()
    while True:
        print("4")
        if (not recording and not busy):
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
            print("3")
        elif recording:
            halt = input()
            while halt != "s":
                print("Press s to stop recording: ")
                halt = input()
            recording = False
            busy = True
            p_rec.terminate()
            p_vid.terminate()
            p_rec = Process(target=record_audio, args=(dir_name,))
            p_vid = Process(target=detectAndTrackMultipleFaces, args=(dir_name,))

        else:
            exit(0)  # add post processing here


if __name__ == '__main__':
    try:
        loop()
    except KeyboardInterrupt:
        exit(0)
