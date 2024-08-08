# coding=utf-8
# !/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import sys
import time
import ffmpeg


class AudioDecodeCallback:
    """
    An interface for receiving decoded audio data callbacks.

    Attributes:
        None

    Methods:
        on_audio_data(audio_data): Called whenever new audio data is available.
    """

    def on_audio_data(self, audio_data):
        """
        Invoked when new audio data becomes available.

        Args:
            audio_data (bytes): Decoded audio data.
        """
        pass


class AudioDecoder:
    """
    A decoder class responsible for decoding audio streams from files into PCM format.

    Attributes:
        _callback (AudioDecodeCallback): An instance responsible for handling decoded audio data.

    Methods:
        decode_audio_by_file(input_file): Decodes audio based on the specified audio file path.
    """

    def __init__(self, callback: AudioDecodeCallback = None):
        """
        Initializes the audio decoder.

        Args:
            callback (AudioDecodeCallback): Callback object to receive audio data.
        """
        self._callback = callback

    def decode_audio_in_blocks(self, input_file):
        """
        Decodes audio from the given file.

        Args:
            input_file (str): Path to the input audio file.
        """
        try:
            # Start the ffmpeg process asynchronously to decode audio
            out = (
                ffmpeg
                .input(input_file)
                .output('pipe:1', format='s16le', acodec='pcm_s16le', ac=1, ar='16k')
                .run_async(pipe_stdout=True, pipe_stderr=True)
            )

            while True:
                # Read bytes from the ffmpeg process stdout
                in_bytes = out.stdout.read(3200)
                time.sleep(0.01)
                if not in_bytes:
                    break

                # Pass the audio data to the callback function
                self._callback.on_audio_data(in_bytes)

            # Close the pipes and wait for the ffmpeg process to finish
            out.stdout.close()
            out.stderr.close()
            out.wait()

        except ffmpeg.Error as e:
            # Print ffmpeg stderr output upon encountering an error
            print(e.stderr, file=sys.stderr)
            # Exit the program with an error status
            sys.exit(1)

    def convert_to_pcm_file(self, input_file_to_decode: str, output_file: str):
        """
        Converts an audio/video file to a PCM format file with a sample rate of 16kHz,
        bit_depth of 16 bits, and mono channel using the ffmpeg library.

        This method leverages the ffmpeg library to transform any audio format
        into a specified PCM format, ensuring the output file meets predefined
        audio specification requirements.

        Parameters:
        - input_file (str): The full path of the audio file to be converted.
        - output_file (str): The destination storage path for the resulting PCM file.

        Error Handling:
        Any errors encountered during the conversion process will capture the
        ffmpeg.Error exception and print detailed error information.
        """
        try:
            # Using ffmpeg to read the audio stream from input_file
            # Setting the output format to s16le (little-endian 16-bit integer)
            # Setting the codec to pcm_s16le to obtain PCM data
            # Setting the number of channels to 1 (mono)
            # Setting the sample rate to 16kHz
            # Executing the conversion operation, allowing to overwrite of existing output files
            (
                ffmpeg
                .input(filename=input_file_to_decode)
                .output(
                    output_file,
                    format='s16le',
                    acodec='pcm_s16le',
                    ac=1,
                    ar='16k'
                )
                .run(overwrite_output=True)
            )

            # After successful conversion, print confirmation message
            print(f"The input file has been successfully converted and saved as: {output_file}")

        except ffmpeg.Error as e:
            # Capturing ffmpeg.Error exceptions, printing error details
            print(f"An error occurred: {e.stderr.decode()}")
