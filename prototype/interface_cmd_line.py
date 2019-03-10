"""Command Line Interface for Instrumented Classroom Project"""


from datetime import datetime
import os
# import fnmatch
import errno
from multiprocessing import Process

## Import own-code
from audio_rec import record_audio
from face_tracking import detectAndTrackMultipleFaces
from transcribe_wav import transcribe
# from test_mult_proc import f_rec, f_busy


def create_new_dir():
    """
    This function creates a new directory in the current one in which to store
    the generated output files.  The directory name used is the current time
    stamp.  If such a directory already exists we do nothing and use it.
    """
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
    """
    This function contains the body of logic that indefinitely records and
    then process that information per the user's input.
    """
    recording, busy = False, False
    p_rec, p_vid = None, None
    # p_trans = None
    itter_num = 0
    dir_name = create_new_dir()
    while True:
        if (not recording and not busy):                    # R = F and B = F
            # dir_name = create_new_dir()
            print("Press r to start recording and s to stop recording: ")
            rec = input()
            while rec != "r":
                print("Press r to start recording: ")
                rec = input()
            recording = True
            busy = False
            itter_num += 1
            p_rec = Process(target=record_audio, args=(dir_name, itter_num))
            p_vid = Process(target=detectAndTrackMultipleFaces,
                            args=(dir_name, itter_num))
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
            # p_trans = Process(target=transcribe, args=(dir_name, "recording_.wav"))
            # p_trans.start()

        else:                                              # R = F and B = T
            # files_to_trans = fnmatch.filter(os.listdir('.'), 'recording_*.wav')
            # for file in files_to_trans
            if p_rec.is_alive():
                pass
                 # print("this shouldn't happen")
            else:
                files_to_trans = "recording_" + str(itter_num) + ".wav"
                transcribe(dir_name, files_to_trans, itter_num)
                print("To record again, press r, otherwise press any other key: ")
                rec = input()
                if rec == 'r':
                    busy = False
                    recording = False
                else:
                    exit(0)



            # if p_trans.is_alive():
            #     pass
            # else:
            #     print("To record again, press r, otherwise press any other key: ")
            #     rec = input()
            #     if rec == 'r':
            #         print("Don't have this functionality yet.  We're working on it :)")
            #     exit(0)  # add post processing here


if __name__ == '__main__':
    try:
        loop()
    except KeyboardInterrupt:
        exit(0)
