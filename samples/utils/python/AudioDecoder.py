# !/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import subprocess
import time


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
    A decoder class responsible for decoding audio from files into OPUS format.
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
            ffmpeg_process = subprocess.Popen(
                [
                    'ffmpeg', '-i', input_file, '-f', 'opus', '-ar', '16000',
                    '-ac', '1', '-acodec', 'libopus', 'pipe:1'
                ],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
            )  # initialize ffmpeg to decode input audio or video

            while True:
                # Read bytes from the ffmpeg process stdout
                in_bytes = ffmpeg_process.stdout.read(3200)
                time.sleep(0.01)
                if not in_bytes:
                    break

                # Pass the audio data to the callback function
                self._callback.on_audio_data(in_bytes)

            # Close the pipes and wait for the ffmpeg process to finish
            ffmpeg_process.stdin.close()
            ffmpeg_process.wait()
        except subprocess.CalledProcessError as e:
            # Capturing ffmpeg exceptions, printing error details
            print(f'An error occurred: {e}')

    def convert_to_opus_file(self, input_file_to_decode: str,
                             output_file: str):
        """
        Converts an audio/video file to a OPUS format file with a sample rate of 16kHz,
        bit_depth of 16 bits, and mono channel using the ffmpeg library.

        This method leverages the ffmpeg library to transform any audio format
        into a specified OPUS format, ensuring the output file meets predefined
        audio specification requirements.

        Parameters:
        - input_file (str): The full path of the audio file to be converted.
        - output_file (str): The destination storage path for the resulting .opus file.

        Error Handling:
        Any errors encountered during the conversion process will capture the
        ffmpeg.Error exception and print detailed error information.
        """
        try:
            # Using ffmpeg to read the audio stream from input_file
            # Setting the output format to opus
            # Setting the codec to libopus
            # Setting the number of channels to 1 (mono)
            # Setting the sample rate to 16kHz
            # Executing the conversion operation, allowing to overwrite of existing output files
            # (
            #     ffmpeg
            #     .input(filename=input_file_to_decode)
            #     .output(
            #         output_file,
            #         format='opus',
            #         acodec='libopus',
            #         ac=1,
            #         ar='16k'
            #     )
            #     .run(overwrite_output=True)
            # )
            cmd = [
                'ffmpeg',
                '-i',
                input_file_to_decode,
                '-c:a',
                'libopus',
                '-ac',
                '1',
                '-ar',
                '16000',
                '-y',  # Overwrite output file without asking
                output_file
            ]

            subprocess.run(cmd)

            # After successful conversion, print confirmation message
            print(
                f'The input file has been successfully converted and saved as: {output_file}'
            )

        except subprocess.CalledProcessError as e:
            # Capturing ffmpeg exceptions, printing error details
            print(f'An error occurred: {e}')
