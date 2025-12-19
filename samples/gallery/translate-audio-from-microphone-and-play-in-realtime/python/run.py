import os
import queue
import sys
import threading
import time

import dashscope
import pyaudio
import wx
import wx.richtext as rt
from dashscope.audio.asr import *
from dashscope.audio.tts_v2 import *

sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 '../../../utils/python'))

from RealtimeMp3Player import RealtimeMp3Player


# Set your Dashscope API key
def init_dashscope_api_key():
    """
        Set your DashScope API-key. More information:
        https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    """

    if 'DASHSCOPE_API_KEY' in os.environ:
        dashscope.api_key = os.environ[
            'DASHSCOPE_API_KEY']  # load API-key from environment variable DASHSCOPE_API_KEY
    else:
        dashscope.api_key = '<your-dashscope-api-key>'  # set API-key manually


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


# Handle the ASR task. This function will get audio from microphone in while loop and send it to ASR.
# The streaming output of ASR will be pushed back to the wx_text_queue and  asr_fixed_words
def gummyAsrTask():
    class Callback(TranslationRecognizerCallback):
        def __init__(self):
            super().__init__()
            # Initialize pointers for tracking words
            self.sentence_ptr = 0
            self.zh_word_ptr = 0
            self.tg_word_ptr = 0

        def on_open(self) -> None:
            # When the recognizer opens, set up the microphone stream
            global mic
            global audio_stream
            with pyaudio_lock:
                print('TranslationRecognizerCallback open.')
                mic = pyaudio.PyAudio()
                audio_stream = mic.open(format=pyaudio.paInt16,
                                        channels=1,
                                        rate=16000,
                                        input=True)

        def on_close(self) -> None:
            # Clean up the audio stream and microphone
            global mic
            global audio_stream
            print('TranslationRecognizerCallback close.')
            if audio_stream is None:
                print('audio_stream is None')
                return
            if audio_stream is not None:
                audio_stream.stop_stream()
                audio_stream.close()
                mic.terminate()
                audio_stream = None
                mic = None

        def on_event(
            self,
            request_id,
            transcription_result: TranscriptionResult,
            translation_result: TranslationResult,
            usage,
        ) -> None:
            new_chinese_words = ''
            new_target_language_words = ''
            is_sentence_end = False

            # Process transcription results. Only new fixed words will be pushed back.
            if transcription_result != None:
                for i, word in enumerate(transcription_result.words):
                    if word.fixed:
                        if i >= self.zh_word_ptr:
                            print('new fixed ch word: ', word.text)
                            new_chinese_words += word.text
                            self.zh_word_ptr += 1

            # Process translation results. Only new fixed words will be pushed back.
            if translation_result != None:
                target_language_translation = translation_result.get_translation(
                    'en')
                if target_language_translation != None:
                    for i, word in enumerate(
                            target_language_translation.words):
                        if word.fixed:
                            if i >= self.tg_word_ptr:
                                print('new fixed {} word: '.format(
                                    target_language, word.text))
                                asr_fixed_words.put([word.text, False])
                                new_target_language_words += word.text
                                self.tg_word_ptr += 1
                    # Check if the current sentence has ended
                    if target_language_translation.is_sentence_end:
                        print('target_language sentence end')
                        self.sentence_ptr += 1
                        self.tg_word_ptr = 0
                        self.zh_word_ptr = 0
                        asr_fixed_words.put(['', True])
                        is_sentence_end = True
            wx_text_queue.put(
                [new_chinese_words, new_target_language_words, False])
            if is_sentence_end:
                wx_text_queue.put(['', '', True])

    callback = Callback()

    # Set up the ASR translator
    translator = TranslationRecognizerRealtime(
        model='gummy-realtime-v1',
        format='pcm',
        sample_rate=16000,
        transcription_enabled=True,
        translation_enabled=True,
        translation_target_languages=[target_language],
        callback=callback,
    )

    print('translator start')
    translator.start()
    print('translator request_id: {}'.format(translator.get_last_request_id()))

    # Open a file to save microphone audio data
    saved_mic_audio_file = open('mic_audio.pcm', 'wb')

    # Continuously read audio data from the microphone
    while True:
        if audio_stream:
            try:
                data = audio_stream.read(3200, exception_on_overflow=False)
                translator.send_audio_frame(data)
                saved_mic_audio_file.write(data)
            except Exception as e:
                print(e)
        else:
            break

    print('translator stop')
    translator.stop()


# Handle the TTS task. This function will get text in asr_fixed_words in while loop and send it to TTS.
# The streaming output of TTS will be played back by the player.
def cosyvoiceTtsTask():
    player = RealtimeMp3Player()
    with pyaudio_lock:
        player.start()

    class Callback(ResultCallback):
        def on_open(self):
            print('tts websocket is open.')

        def on_complete(self):
            print('speech synthesis task complete successfully.')

        def on_error(self, message: str):
            print(f'speech synthesis task failed, {message}')

        def on_close(self):
            print('tts websocket is closed.')

        def on_event(self, message):
            pass

        def on_data(self, data: bytes) -> None:
            nonlocal player
            player.write(data)

    synthesizer_callback = Callback()

    # Create a speech synthesizer instance
    synthesizer = SpeechSynthesizer(model='cosyvoice-v3-flash',
                                    voice='longanhuan',
                                    callback=synthesizer_callback)

    print('tts request_id: {}'.format(synthesizer.get_last_request_id()))

    # Continuously check for new words to synthesize
    while True:
        if not asr_fixed_words.empty():
            word, is_sentence_end = asr_fixed_words.get()
            if is_sentence_end:
                # when the sentence ends, wait for the previous sentence to finish synthesing and playing.
                synthesizer.streaming_complete()
                player.stop()
                player.reset()
                # reset the player and synthesizer
                player.start()
                synthesizer = SpeechSynthesizer(model='cosyvoice-v3-flash',
                                                voice='longanhuan',
                                                callback=synthesizer_callback)
            else:
                print('send word: ', word)
                synthesizer.streaming_call(word)
        else:
            # Sleep briefly if no words are available
            time.sleep(0.01)


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
    app = wx.App(False)
    frame = SubtitleFrame()
    app.MainLoop()
