import ffmpeg


def convert_to_pcm(input_file: str, output_file: str):
    """
    Converts an audio file to a PCM format with a sample rate of 16kHz,
    bit depth of 16 bits, and mono channel using the ffmpeg library.

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
        # Executing the conversion operation, allowing overwrite of existing output files
        (
            ffmpeg
            .input(input_file)
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
        print(f"The file has been successfully converted and saved as: {output_file}")

    except ffmpeg.Error as e:
        # Capturing ffmpeg.Error exceptions, printing error details
        print(f"An error occurred: {e.stderr.decode()}")
