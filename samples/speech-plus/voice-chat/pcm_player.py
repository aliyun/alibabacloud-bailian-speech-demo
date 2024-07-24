import threading
import time
import pyaudio


class PlayerCallback:
    """
    Callback interface used to execute specific operations upon playback completion.

    Methods:
        on_play_end(): Method called when playback ends.
    """

    def on_play_end(self):
        """
        Called when playback has ended. Default implementation does nothing, can be overridden by subclasses to provide concrete behavior.
        """


class PcmPlayer:
    """
    PCM audio player class responsible for playing PCM formatted audio data in a separate thread.

    Attributes:
        callback (PlayerCallback): Callback object invoked after playback completes, defaults to None.
        player (PyAudio): PyAudio instance managing audio devices.
        stream (Stream): Audio stream instance for playing audio data.
        play_thread (Thread): Thread instance for asynchronous audio playback.
        frame_data_queue (list): Queue holding audio frames pending playback.
        _is_end (bool): Flag indicating whether to stop playback.

    Methods:
        __init__(callback=None): Constructor initializing the player and setting the callback object.
        start_play(): Initiates audio playback.
        _play_in_thread(): Internal method playing audio data in an independent thread.
        play(frame_data): Adds an audio frame to the playback queue.
        stop_play(): Halts audio playback and invokes the callback function post-playback.
        cancel_play(): Clears the playback queue and immediately stops playback.
        __del__(): Destructor ensuring resources are released properly.
    """

    def __init__(self, callback: PlayerCallback = None):
        """
        Initializes a PcmPlayer instance, creates PyAudio and audio stream instances, prepares the playback thread.

        Parameters:
            callback (PlayerCallback): Optional parameter specifying the callback object after playback ends.
        """
        self.callback = callback if callback is not None else PlayerCallback()
        self.player = pyaudio.PyAudio()
        self.stream = self.player.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=24000,
            output=True
        )
        self.play_thread = None
        self.frame_data_queue = []
        self._is_end = False

    def start_play(self):
        """
        Starts audio playback, launching the playback thread.
        """
        self._is_end = False
        self.stream.start_stream()
        self.play_thread = threading.Thread(target=self._play_in_thread)
        self.play_thread.start()

    def _play_in_thread(self):
        """
        Loops through playing audio data within an independent thread until the queue is empty or marked to stop.
        """
        while self.frame_data_queue or not self._is_end:
            if not self.frame_data_queue:
                time.sleep(0.1)
                continue
            frame_data = self.frame_data_queue.pop(0)
            self.stream.write(frame_data)

        if self._is_end:
            self.stream.stop_stream()
            self.callback.on_play_end()

    def play(self, frame_data):
        """
        Queues an audio frame for playback.

        Parameters:
            frame_data (bytes): Single frame of PCM audio data.
        """
        self.frame_data_queue.append(frame_data)

    def feed_finish(self):
        """
        Sets the end flag, causing the playback thread to exit its loop, thus stopping playback.
        """
        self._is_end = True

    def cancel_play(self):
        """
        Clears all audio data from the playback queue and immediately halts playback.
        """
        self.frame_data_queue.clear()
        self._is_end = True

    def __del__(self):
        """
        Destructor ensuring that the audio stream and PyAudio instance are closed properly before the player is destroyed.
        """
        self.stream.close()
        self.player.terminate()
