## Dependencies
from multiprocessing import Process
import RPi.GPIO as GPIO
import time
from datetime import datetime
import os
import errno

## Import own-code
from audio_rec import record_audio
from face_tracking import detectAndTrackMultipleFaces
from transcribe_wav import transcribe

## Set Up Globals
RecLedPin = 18          # Recording Signal -- Blue
BusyLedPin = 23         # Busy Signal -- Red
OnLedPin = 24           # Alive Signal -- Green

ToggleBtnPin = 17       # Button to Toggle State
StopBtnPin = 22         # Button to power off


class CurrentState:
    def __init__(self, rec, busy, p_audio=None, p_video=None, dir_name=""):
        self.rec = rec
        self.busy = busy
        self.p_audio = p_audio
        self.p_video = p_video
        self.dir_name = dir_name
        self.itter_num = 0


    def start_recording(self):
        self.rec = True
        self.busy = False

        self.itter_num += 1
        self.p_audio = Process(target=record_audio, args=(self.dir_name,
                                                          self.itter_num))
        self.p_video = Process(target=detectAndTrackMultipleFaces,
                               args=(self.dir_name, self.itter_num))
        self.p_audio.start()
        self.p_video.start()

        GPIO.output(RecLedPin, self.rec)
        GPIO.output(BusyLedPin, self.busy)


    def stop_recording(self):
        self.busy = True
        self.rec = False

        self.p_audio.terminate()
        self.p_video.terminate()
        self.p_audio.join()
        self.p_video.join()
        
        self.busy = False
        GPIO.output(RecLedPin, self.rec)
        GPIO.output(BusyLedPin, self.busy)


    def trans_recording(self):
        print("* busy")
        self.busy = True
        self.rec = False
        GPIO.output(BusyLedPin, self.busy)

        files_to_trans = "recording_" + str(self.itter_num) + ".wav"
        transcribe(self.dir_name, files_to_trans, self.itter_num)
       
        self.busy = False
        GPIO.output(RecLedPin, self.rec)
        GPIO.output(BusyLedPin, self.busy)
        print("* not busy")



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

def setup():
    GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by physical location
    # GPIO.setwarnings(False)
    GPIO.setup(RecLedPin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(BusyLedPin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(OnLedPin, GPIO.OUT, initial=GPIO.HIGH)

    GPIO.setup(ToggleBtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(StopBtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) 


def promptProceses(state):
    if (not state.rec and not state.busy):
        state.start_recording()
    elif(state.rec):            # R: True, B: meh
        state.stop_recording()
        state.trans_recording()
    # else:                       # R: False, B: True
    #     pass
        # recording = False
        # busy = False

    # state.rec = recording
    # state.busy = busy
    
    


def loop():
    cur_state = CurrentState(False, False, dir_name=create_new_dir())

    updateStatus = lambda ev=None: promptProceses(cur_state)
    shutDown = lambda ev=None: destroy(cur_state)

    # wait for falling and set bouncetime to prevent the callback function from
    # being called multiple times when the button is pressed
    GPIO.add_event_detect(ToggleBtnPin, GPIO.FALLING, callback=updateStatus,
                          bouncetime=200)
    GPIO.add_event_detect(StopBtnPin, GPIO.FALLING, callback=shutDown,
                          bouncetime=200)
    while True:
        time.sleep(0.02)   # Don't do anything


def destroy(state):
    if not (state.rec or state.busy):
        GPIO.output(RecLedPin, GPIO.LOW)
        GPIO.output(BusyLedPin, GPIO.LOW)
        GPIO.output(OnLedPin, GPIO.LOW)
        GPIO.cleanup()                     # Release resource
        del state
        exit(0)


if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        GPIO.output(RecLedPin, GPIO.LOW)
        GPIO.output(BusyLedPin, GPIO.LOW)
        GPIO.output(OnLedPin, GPIO.LOW)
        GPIO.cleanup()
        exit(1)
