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


# Lock for controlling access to the PyAudio stream
pyaudio_lock = threading.Lock()

# Initialize global variables for microphone and audio stream
mic = None
audio_stream = None
# Queue for results from ASR
asr_result_q: queue.Queue[TranscriptionResult] = queue.Queue()


# Handle the ASR task. This function will get audio from microphone in while loop and send it to ASR.
# The streaming output of ASR will be pushed back to asr_result_q
def AsrTask():
    class Callback(TranslationRecognizerCallback):
        def __init__(self):
            super().__init__()

        def on_open(self) -> None:
            # When the recognizer opens, set up the microphone stream
            global mic
            global audio_stream
            with pyaudio_lock:
                print('RecognitionCallback open.')
                mic = pyaudio.PyAudio()
                audio_stream = mic.open(format=pyaudio.paInt16,
                                        channels=1,
                                        rate=16000,
                                        input=True)

        def on_close(self) -> None:
            # Clean up the audio stream and microphone
            global mic
            global audio_stream
            print('RecognitionCallback close.')
            if audio_stream is None:
                print('audio_stream is None')
                return
            if audio_stream is not None:
                audio_stream.stop_stream()
                audio_stream.close()
                mic.terminate()
                audio_stream = None
                mic = None

        def on_complete(self) -> None:
            print('RecognitionCallback completed.')  # translation completed

        def on_event(
            self,
            request_id,
            transcription_result: TranscriptionResult,
            translation_result: TranslationResult,
            usage,
        ) -> None:
            if transcription_result is not None:
                asr_result_q.put(transcription_result)

    callback = Callback()

    # Call translation service by async mode, you can customize the translation parameters, like model, format,
    # sample_rate For more information, please refer to https://help.aliyun.com/document_detail/2712536.html
    translator = TranslationRecognizerRealtime(
        model='gummy-realtime-v1',
        format='pcm',
        sample_rate=16000,
        transcription_enabled=True,
        translation_enabled=False,
        callback=callback,
    )

    print('translator start')
    translator.start()

    print('requestId: ' + translator.last_request_id)

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
    def update_text(self, asr_result: TranscriptionResult):
        is_new_sentence = False
        fixed_text = ''
        unfixed_text = ''
        for word in asr_result.words:
            if word.fixed:
                fixed_text += word.text
            else:
                unfixed_text += word.text

        print('Updating text: ', [fixed_text, unfixed_text])

        # Update buffers with new text
        self.text_buffer[-1] = [fixed_text, unfixed_text]

        if asr_result.is_sentence_end:
            self.text_buffer.append(['', ''])

        fixed_text = ''
        unfixed_text = ''
        if asr_result.stash is not None:
            for word in asr_result.stash.words:
                if word['fixed']:
                    fixed_text += word.text
                else:
                    unfixed_text += word.text
            self.text_buffer[-1] = [fixed_text, unfixed_text]

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
    app = wx.App(False)
    frame = SubtitleFrame()
    app.MainLoop()
