import os
import queue
import sys
import threading

import pyaudio
import wx
import wx.richtext as rt
from dashscope import Client


# Set your Dashscope API key
def get_api_key():
    """
        Set your DashScope API-key. More information:
        https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    """
    if 'DASHSCOPE_API_KEY' in os.environ:
        return os.environ['DASHSCOPE_API_KEY']
    return '<your-dashscope-api-key>'


# Lock for controlling access to the PyAudio stream
pyaudio_lock = threading.Lock()

# Initialize global variables for microphone and audio stream
mic = None
audio_stream = None
# Queue for results from ASR: (fixed_text, unfixed_text, is_new_sentence)
asr_result_q: queue.Queue = queue.Queue()
stop_asr = threading.Event()


# Handle the ASR task. This function will get audio from microphone in while loop and send it to ASR.
# The streaming output of ASR will be pushed back to asr_result_q.
# TODO: the V2 realtime API exposes sentence-level transcription, not the word-level
# fixed/unfixed partials that gummy-realtime-v1 provided, so the subtitle display is
# approximated with final + stash text.
def AsrTask():
    global mic
    global audio_stream

    api_key = get_api_key()

    with pyaudio_lock:
        print('ASR session open.')
        mic = pyaudio.PyAudio()
        audio_stream = mic.open(format=pyaudio.paInt16,
                                channels=1,
                                rate=16000,
                                input=True)

    client = Client(api_key=api_key)
    try:
        session = client.audio.realtime.connect(
            model='qwen3-asr-flash-realtime',
        )
        session.connect()
        session.update_session(
            output_modalities=["text"],
            enable_input_audio_transcription=True,
            transcription_params={
                "language": "zh",
                "sample_rate": 16000,
                "input_audio_format": "pcm",
            },
        )

        def receive_events():
            try:
                for event in session.events():
                    kind = event.get('type')
                    if kind == 'conversation.item.input_audio_transcription.text':
                        stash = event.get('stash') or event.get('text', '')
                        asr_result_q.put(('', stash, False))
                    elif kind == 'conversation.item.input_audio_transcription.completed':
                        asr_result_q.put((event.get('transcript', ''), '', True))
            except Exception as e:
                print('event consumer error: ', e)

        receiver = threading.Thread(target=receive_events)
        receiver.start()

        print('translator start')
        print('requestId: ' + (session.session_id or 'unknown'))

        # Open a file to save microphone audio data
        saved_mic_audio_file = open('mic_audio.pcm', 'wb')

        # Continuously read audio data from the microphone
        try:
            while not stop_asr.is_set() and audio_stream:
                try:
                    data = audio_stream.read(3200, exception_on_overflow=False)
                    session.append_audio(data)
                    saved_mic_audio_file.write(data)
                except Exception as e:
                    print(e)
        finally:
            saved_mic_audio_file.close()
            session.close()
            receiver.join(timeout=30)

        print('translator stop')
    finally:
        with pyaudio_lock:
            if audio_stream is not None:
                try:
                    audio_stream.stop_stream()
                    audio_stream.close()
                except Exception:
                    pass
                audio_stream = None
            if mic is not None:
                try:
                    mic.terminate()
                except Exception:
                    pass
                mic = None
        client.close()


class SubtitleFrame(wx.Frame):
    def __init__(self):
        # Title of the window
        super().__init__(parent=None, title='实时语音识别', size=(1000, 500))

        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.top_sizer = wx.BoxSizer(wx.VERTICAL)

        # Text box for displaying asr result
        self.asr_text_box = rt.RichTextCtrl(self.panel,
                                            style=wx.NO_BORDER | rt.RE_READONLY
                                            | rt.RE_MULTILINE)
        self.asr_text_box.EnableVerticalScrollbar(True)
        self.asr_text_box.SetFont(
            wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                    wx.FONTWEIGHT_NORMAL))
        self.top_sizer.Add(self.asr_text_box, 1, wx.EXPAND | wx.ALL, 5)

        self.panel.SetSizer(self.top_sizer)

        # Timer to update text periodically
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
        self.timer.Start(10)

        # Buffer for accumulating text, [fixed, unfixed]
        self.text_buffer = [['', '']]
        # Show the frame
        self.Show()

    def set_title_style(self, title: wx.StaticText):
        font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                       wx.FONTWEIGHT_BOLD)
        title.SetFont(font)
        title.SetForegroundColour(wx.Colour(0, 0, 255))

    # Timer event handler to update text boxes
    def on_timer(self, event):
        while not asr_result_q.empty():
            result = asr_result_q.get()
            self.update_text(result)

    # Method to update the text in the text boxes
    def update_text(self, asr_result):
        fixed_text, unfixed_text, is_new_sentence = asr_result

        print('Updating text: ', [fixed_text, unfixed_text])

        # Update buffers with new text
        self.text_buffer[-1][0] += fixed_text
        self.text_buffer[-1][1] = unfixed_text

        if is_new_sentence:
            self.text_buffer.append(['', ''])

        print('text buffer: ', self.text_buffer)

        # Clear and update text box
        self.asr_text_box.Clear()

        # Write all lines except the last one in black
        normal_font = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                              wx.FONTWEIGHT_NORMAL)
        self.asr_text_box.BeginFont(normal_font)
        self.asr_text_box.BeginTextColour(wx.BLACK)

        if len(self.text_buffer) > 1:
            self.asr_text_box.WriteText(
                '\n'.join([x[0] + x[1] for x in self.text_buffer[:-1]]) + '\n')

        self.asr_text_box.WriteText(self.text_buffer[-1][0])
        self.asr_text_box.EndTextColour()
        self.asr_text_box.EndFont()

        # Write the last line in blue with larger font
        large_font = wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                             wx.FONTWEIGHT_BOLD)
        self.asr_text_box.BeginFont(large_font)
        self.asr_text_box.BeginTextColour(wx.BLUE)
        self.asr_text_box.WriteText(self.text_buffer[-1][1])
        self.asr_text_box.EndTextColour()
        self.asr_text_box.EndFont()

        # Auto-scroll to the bottom of the text boxes
        self.asr_text_box.ShowPosition(self.asr_text_box.GetLastPosition())


if __name__ == '__main__':
    # Start threads for ASR and TTS tasks
    asr_thread = threading.Thread(target=AsrTask)
    asr_thread.start()
    # Create and start the application's main loop
    try:
        app = wx.App(False)
        frame = SubtitleFrame()
        app.MainLoop()
    finally:
        stop_asr.set()
        asr_thread.join(timeout=5)
