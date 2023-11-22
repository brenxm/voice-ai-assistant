from network import ConnectionBlock
from pynput import keyboard
from time import sleep
from queue import Queue
import pyaudio
import time
import json
import io
# Recording voice prompt
# Press 'f20'
# Establish connection with server
# While pressing, record voice data ~
# Per cut off 1. Timeout - silent, 2. button up, create object with this properties
# Metadata (obj) - size of payload (binary size)
# Payload - audio data converted to binary
# Send data


class Microphone():
    def __init__(self):
        self.recording = False
        self.connection_block = False
    
    def listen_key(self, key):
        # Initialize key
        init_key_event(key, self.recording)

        # Blocking, waiting for recording action event
        while not self.recording:
            sleep(0.1)

        # Create a connection to the server
        self.connection_block = ConnectionBlock()
        
        payload_queue = Queue()

        # Start streaming
        # TODO: implement function to stream data

        while self.recording:
            # Blocking
            payload = payload_queue.get()

            payload_size = len(payload)

            payload_obj = {
                'metadata': json.dumps({'payload_size': payload_size}),
                'payload': payload
            }

            self.connection_block.send_payload(payload_obj)
        

        print('End of recording')



        # metadata, payload to obj
        # obj to send_to_server method


def init_key_event(key, recording):
    def on_press(key_event):
        nonlocal recording
        if key_event == key:
            recording = True

    def on_release(key_event):
        nonlocal recording
        if key_event == key:
            recording = False

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    

def stream_audio():
    pya = pyaudio.PyAudio()
    streamer = pya.open(format=pyaudio.paInt16, channels=1, rate=44100, inpt=True, frames_per_buffer=1024)
    audio_buffer = []
    sound_detected = True
    silence_start_time = None
    detected = False
    detected_index = [0]
    silent_called = False


    def stream():
        chunk = streamer.read(1024)
        audio_buffer.append(chunk)

        values = [int.from_bytes(chunk[i:i+2], 'little', signed=True) for i in range(0, len(chunk), 2)]

        if max(values) > 700:
            sound_detected = True

        if max(values) < 300:
            if silence_start_time is None:
                silence_start_time = time.time()
            
        elif time.time() - silence_start_time > 1.5 and not detected and sound_detected:
            detected = True
            silent_called = True
            index = len(audio_buffer)
            detected_index.append(index)



# Test
mic = Microphone()
mic.listen_key(keyboard.Key.f20)