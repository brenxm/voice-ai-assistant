import openai
from pydub import AudioSegment
import tempfile
import os
import io

openai.api_key = "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"

def transcript(audio_chunks):
    audio_data = b''.join(audio_chunks)
    audio_segment = AudioSegment(
        data=audio_data,
        sample_width=2,  # Example: 2 bytes per sample
        frame_rate=44100,  # Example: 44.1 kHz
        channels=1  # Example: Mono
    )

    # Export to a bytes-like object
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
        audio_segment.export(temp_file.name, format="mp3")
        temp_file_path = temp_file.name

    # Create the transcription using the temporary file
    with open(temp_file_path, 'rb') as audio_file:
        response = openai.audio.transcriptions.create(
            model='whisper-1',
            file=audio_file
        )

    # Print the response text
    print(f'{response.text} audio_size: {len(audio_chunks)}')

    # Delete the temporary file
    os.remove(temp_file_path)


