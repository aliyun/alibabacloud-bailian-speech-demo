import os
import queue
import sys
import threading
import time

import pyaudio
import wx
import wx.richtext as rt
from dashscope import Client

sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 '../../../utils/python'))

from RealtimeMp3Player import RealtimeMp3Player


# Set your Dashscope API key
def get_api_key():
    """
        Set your DashScope API-key. More information:
        https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    """
    if 'DASHSCOPE_API_KEY' in os.environ:
        return os.environ['DASHSCOPE_API_KEY']
    return '<your-dashscope-api-key>'


# Set the target language for translation
target_language = 'en'

# Lock for controlling access to the PyAudio stream
pyaudio_lock = threading.Lock()

# Initialize global variables for microphone and audio stream
mic = None
audio_stream = None
# Queue for text updates in wx
wx_text_queue = queue.Queue()
# Queue for fixed words from ASR
asr_fixed_words = queue.Queue()
stop_asr = threading.Event()


# Handle the ASR task. This function will get audio from microphone in while loop and send it to ASR.
# The streaming output of ASR will be pushed back to the wx_text_queue and asr_fixed_words.
def gummyAsrTask():
    global mic
    global audio_stream

    api_key = get_api_key()

    with pyaudio_lock:
        print('TranslationRecognizerCallback open.')
        mic = pyaudio.PyAudio()
        audio_stream = mic.open(format=pyaudio.paInt16,
                                channels=1,
                                rate=16000,
                                input=True)

    with Client(api_key=api_key) as client:
        with client.audio.realtime.connect(
                model='qwen3.8-livetranslate-flash-realtime',
        ) as session:
            session.update_session(
                output_modalities=["text"],
                translation_params={"language": target_language},
            )

            def receive_events():
                try:
                    for event in session.events():
                        kind = event.get('type')
                        if kind == 'response.text.delta':
                            delta = event.get('delta', '')
                            wx_text_queue.put(['', delta, False])
                            asr_fixed_words.put([delta, False])
                        elif kind == 'response.text.done':
                            wx_text_queue.put(['', event.get('text', ''), False])
                        elif kind == 'conversation.item.input_audio_transcription.completed':
                            wx_text_queue.put([event.get('transcript', ''), '', False])
                        elif kind == 'response.done':
                            wx_text_queue.put(['', '', True])
                            asr_fixed_words.put(['', True])
                except Exception as e:
                    print('event consumer error: ', e)

            receiver = threading.Thread(target=receive_events)
            receiver.start()

            print('translator start')
            print('translator request_id: {}'.format(session.session_id or 'unknown'))

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
                receiver.join(timeout=30)

            print('translator stop')

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


# Handle the TTS task. This function will get text in asr_fixed_words in while loop and send it to TTS.
# The streaming output of TTS will be played back by the player.
def cosyvoiceTtsTask():
    player = RealtimeMp3Player()
    with pyaudio_lock:
        player.start()

    api_key = get_api_key()
    with Client(api_key=api_key) as client:
        with client.audio.tts.connect(
                model='cosyvoice-v3-flash',
                voice='longanhuan',
                format='mp3') as session:
            complete_event = threading.Event()

            def receive_audio():
                try:
                    for chunk in session.audio_chunks():
                        player.write(chunk)
                except Exception as e:
                    print('tts audio consumer error: ', e)
                finally:
                    complete_event.set()

            audio_thread = threading.Thread(target=receive_audio)
            audio_thread.start()

            print('tts request_id: {}'.format(session.session.request_id))

            # Continuously check for new words to synthesize
            while True:
                if not asr_fixed_words.empty():
                    word, is_sentence_end = asr_fixed_words.get()
                    if is_sentence_end:
                        # Commit the accumulated text so the server returns audio.
                        session.flush()
                    else:
                        print('send word: ', word)
                        session.send_text(word)
                else:
                    if stop_asr.is_set():
                        break
                    # Sleep briefly if no words are available
                    time.sleep(0.01)

            session.stop()
            complete_event.wait(timeout=30)
            audio_thread.join(timeout=30)

    player.stop()


class SubtitleFrame(wx.Frame):
    def __init__(self):
        # Title of the window
        super().__init__(parent=None, title='实时翻译器', size=(1000, 500))

        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.top_sizer = wx.BoxSizer(wx.VERTICAL)

        self.chinese_title = wx.StaticText(self.panel, label='中文')
        self.set_title_style(self.chinese_title)

        self.top_sizer.Add(self.chinese_title, 0,
                           wx.ALIGN_CENTER | wx.VERTICAL | wx.TOP, 5)

        # Text box for displaying Chinese translation
        self.chinese_text_box = rt.RichTextCtrl(
            self.panel, style=wx.NO_BORDER | rt.RE_READONLY | rt.RE_MULTILINE)
        self.chinese_text_box.EnableVerticalScrollbar(True)
        self.chinese_text_box.SetFont(
            wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                    wx.FONTWEIGHT_NORMAL))
        self.top_sizer.Add(self.chinese_text_box, 1, wx.EXPAND | wx.ALL, 5)

        self.target_language_title = wx.StaticText(self.panel,
                                                   label=target_language)
        self.set_title_style(self.target_language_title)

        self.top_sizer.Add(self.target_language_title, 0,
                           wx.ALIGN_CENTER | wx.VERTICAL | wx.TOP, 5)

        # Text box for displaying translated text
        self.target_language_text_box = rt.RichTextCtrl(
            self.panel, style=wx.NO_BORDER | rt.RE_READONLY | rt.RE_MULTILINE)
        self.target_language_text_box.EnableVerticalScrollbar(True)
        self.target_language_text_box.SetFont(
            wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                    wx.FONTWEIGHT_NORMAL))
        self.top_sizer.Add(self.target_language_text_box, 1,
                           wx.EXPAND | wx.ALL, 5)

        self.panel.SetSizer(self.top_sizer)

        # Timer to update text periodically
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
        self.timer.Start(100)

        # Buffer for accumulating text
        self.chinese_buffer = ''
        self.target_language_buffer = ''
        # Show the frame
        self.Show()

    def set_title_style(self, title: wx.StaticText):
        font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                       wx.FONTWEIGHT_BOLD)
        title.SetFont(font)
        title.SetForegroundColour(wx.Colour(0, 0, 255))

    # Timer event handler to update text boxes
    def on_timer(self, event):
        while not wx_text_queue.empty():
            content = wx_text_queue.get()
            self.update_text(content)

    # Method to update the text in the text boxes
    def update_text(self, content):
        chinese_text = content[0]
        target_language_text = content[1]
        # Check if this is a new sentence
        is_new_sentence = content[2]
        print('Updating Chinese text: ', chinese_text)
        print('Updating target_language text: ', target_language_text)

        # If it's a new sentence, add a line break
        if is_new_sentence == True:
            chinese_text = '\n' + chinese_text
            target_language_text = '\n' + target_language_text

        # Update buffers with new text
        self.chinese_buffer += chinese_text
        self.target_language_buffer += target_language_text

        # Clear and update text box
        self.chinese_text_box.Clear()
        self.chinese_text_box.BeginTextColour(wx.BLACK)
        self.chinese_text_box.WriteText(self.chinese_buffer)
        self.chinese_text_box.EndTextColour()

        self.target_language_text_box.Clear()
        self.target_language_text_box.BeginTextColour(wx.BLUE)
        self.target_language_text_box.WriteText(self.target_language_buffer)
        self.target_language_text_box.EndTextColour()
        print('target_language buffer: ', self.target_language_buffer)

        # Auto-scroll to the bottom of the text boxes
        self.chinese_text_box.ShowPosition(
            self.chinese_text_box.GetLastPosition())
        self.target_language_text_box.ShowPosition(
            self.target_language_text_box.GetLastPosition())


if __name__ == '__main__':
    # Start threads for ASR and TTS tasks
    asr_thread = threading.Thread(target=gummyAsrTask)
    asr_thread.start()
    tts_thread = threading.Thread(target=cosyvoiceTtsTask)
    tts_thread.start()
    # Create and start the application's main loop
    try:
        app = wx.App(False)
        frame = SubtitleFrame()
        app.MainLoop()
    finally:
        stop_asr.set()
        asr_thread.join(timeout=5)
