from network import ConnectionBlock
from pynput import keyboard
from time import sleep
from queue import Queue
import threading
import pyaudio
import time
import json

# Test module
from transcript_test import transcript


class Microphone():
    def __init__(self):
        self.recording = False
        self.connection_block = False
        self.streamed_audio_buffer = []
        self.disabled_key = False

    def listen_key(self, key):
        # Initialize key event
        self._init_key_event(key)

        while True:
            sleep(5)

    def disable_key(self):
        self.disabled_key = True

    def _init_key_event(self, key):
        def on_press(key_event):
            if key_event == key and not self.disabled_key:
                self.disabled_key = True
                self.recording = True

                # Establish connection
                # self.connection_block = ConnectionBlock()

                # Start streaming audio on separate thread
                stream_thread = threading.Thread(target=(self._stream_audio))
                stream_thread.start()

        def on_release(key_event):
            if key_event == key:
                self.recording = False
                self.disabled_key = False

        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.start()

    def _stream_audio(self):
        pya = pyaudio.PyAudio()
        streamer = pya.open(format=pyaudio.paInt16, channels=1,
                            rate=44100, input=True,  frames_per_buffer=1024)

        timeout = 1.5  # Timeout of when to slice the buffer of audio
        silence_threshold = 300
        active_sound_threshold = 500

        audio_buffer = []

        silence_start_time = None
        sound_detected = False

        while self.recording:
            chunk = streamer.read(1024)
            audio_buffer.append(chunk)

            values = [int.from_bytes(chunk[i:i+2], 'little', signed=True)
                      for i in range(90, len(chunk), 2)]

            if max(values) > active_sound_threshold:
                sound_detected = True
                silence_start_time = None

            if max(values) < silence_threshold:  # Silence is detected
                if silence_start_time is None:
                    silence_start_time = time.time()

                elif time.time() - silence_start_time > timeout:  # Timed out
                    if sound_detected:
                        # Temp variable for audio buffer, since it's being cleared
                        temp_buffer = list(audio_buffer)
                        send_payload_thread = threading.Thread(
                            target=self._send_payload, args=(temp_buffer,))
                        send_payload_thread.start()
                        audio_buffer.clear()
                        sound_detected = False
                        silence_start_time = None

        if len(audio_buffer) > 0:
            send_payload_thread = threading.Thread(
                target=self._send_payload, args=(audio_buffer,))
            send_payload_thread.start()

    def _send_payload(self, audio_chunks):

        audio_chunks = self._clean_audio_chunks(audio_chunks)

        if not audio_chunks:
            return
        print(
            f'received audio_chunks for transcriptions with the size of {len(audio_chunks)}')
        transcript(audio_chunks)

        payload = {
            'metadata': {
                'size': len(audio_chunks)
            },
            'payload': audio_chunks
        }

        # self.connection_block.send_payload(json.dumps(payload))

    def _clean_audio_chunks(self, audio_chunks):
        # Accept list/array of audio chunks as argument,
        # Removes leading silenced chunks and trailing silenced chunks
        # If all chunk is silenced, it will return false
        silence_threshold = 300

        # remove leading silences in audio_chunks
        for index, chunk in enumerate(audio_chunks):
            values = [int.from_bytes(chunk[i:i+2], 'little', signed=True)
                      for i in range(90, len(chunk), 2)]

            if max(values) > silence_threshold:
                audio_chunks = audio_chunks[index:]
                break

            if index == len(audio_chunks) - 1:
                return False

        # remove trailing silences in audio_chunks
        for index, chunk in reversed(list(enumerate(audio_chunks))):
            values = [int.from_bytes(chunk[i:i+2], 'little', signed=True)
                      for i in range(90, len(chunk), 2)]

            if max(values) > silence_threshold:
                audio_chunks = audio_chunks[:index + 1]
                break

        return audio_chunks


# Test
mic = Microphone()
mic.listen_key(keyboard.Key.f20)
