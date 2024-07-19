"""
pcm_recorder.py: A simple class for managing PCM audio recordings.

This module provides a `Recorder` class that can be used to manage audio recordings in PCM format.
It utilizes the `sounddevice` library for capturing audio from the system's default input device.

Attributes:
    sample_rate (int): The sample rate at which audio will be recorded, measured in Hz.
    channels (int): The number of audio channels being recorded (mono or stereo).
    dtype (str): The data type of the recorded samples ('int16', 'float32', etc.).
    format_pcm (str): The format of the audio data ('pcm').
    block_size (int): The number of frames per buffer; determines the recording interval.
"""

import sounddevice as sd  # For audio recording capabilities

# Recording configuration parameters
sample_rate = 16000  # Sample rate (Hz)
channels = 1  # Mono channel
dtype = 'int16'  # Data type for audio samples
format_pcm = 'pcm'  # Audio data format
block_size = 1280  # Frames per buffer, equivalent to approximately 80 ms at 16kHz


class Recorder:
    """
    A class for managing PCM audio recordings using the sounddevice library.

    Attributes:
        _is_working (bool): Indicates whether the recorder is currently active.
        stream (sd.InputStream): An instance of the InputStream class for recording audio.

    Methods:
        start(): Starts the recording process.
        stop(): Stops the recording process.
        is_working(): Returns the current status of the recorder.
        __del__(): Ensures proper cleanup by closing the audio stream upon object deletion.
    """

    def __init__(self, callback):
        """
        Initializes the Recorder with specified recording parameters and a callback function.

        Args:
            callback (function): A user-defined function to handle incoming audio data.
        """
        # Initialize the audio stream
        self._is_working = False
        self.stream = sd.InputStream(
            samplerate=sample_rate,
            channels=channels,
            dtype=dtype,
            blocksize=block_size,
            callback=callback
        )

    def start(self):
        """Starts the recording process."""
        self.stream.start()
        self._is_working = True

    def stop(self):
        """Stops the recording process."""
        self._is_working = False
        self.stream.stop()

    def is_working(self):
        """
        Checks if the recorder is currently active.

        Returns:
            bool: True if recording, False otherwise.
        """
        return self._is_working

    def __del__(self):
        """Ensures the audio stream is closed when the Recorder object is deleted."""
        self.stream.close()
