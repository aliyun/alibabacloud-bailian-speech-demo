# Recording Audio in Web and Performing Speech Recognition

English | [简体中文](./README.md)

This project sets up a local HTTP service and WebSocket speech recognition service, recording audio in the web page and displaying recognition results in real time. You can refer to this example project to add speech recognition functionality to your own web pages.

## Prerequisites

#### Install Python Dependencies

The Alibaba Cloud Bailian SDK requires Python 3.8 or higher. The environment for running this demo can be installed via [PyPI](https://pypi.org/).

You can use the `pip install -r requirements.txt` command to install the dependencies in this folder. Alternatively, manually install the following dependencies:

- Import Bailian SDK
```commandline
pip3 install dashscope // Install Alibaba Cloud Bailian SDK
pip3 install websockets // Install WebSocket service dependencies
```

#### Configure Alibaba Cloud Bailian API-KEY

Before running this example, you need to create an Alibaba Cloud account, obtain the Alibaba Cloud Bailian API-KEY, and complete necessary environment configurations. For detailed API-KEY configuration steps, please refer to: [PREREQUISITES.md](../../../../PREREQUISITES.md)

## Run Example
This directory demonstrates a front-end/back-end separated speech recognition example, connecting the front-end and back-end through WebSocket, and showing how to handle real-time recognition results.

When you click the `Start Recording` button, the web page will establish a connection with the Python WebSocket service, start recording audio from the microphone, and send the recording to the WebSocket service in real-time. The server will call the paraformer-realtime-v2 speech recognition model and return real-time speech recognition results to the web page for display. Each sentence's real-time recognition results will continuously update on the same line until the sentence ends and moves to the next line.

First, configure the Bailian API-KEY in the environment variables and run `demo_server.py`, which by default runs the WebSocket service on port 9090 locally.

```
export DASHSCOPE_API_KEY=xxxxxxx
python demo_server.py
```

Then, run an HTTP service in this directory to support browser access to files in this directory.

```
python -m http.server 9000
```

You can then open the test page in your browser by entering `http://localhost:9000`. Enter a question and click the `Start Recording` button to send the message, then speak into the microphone.

<img src="../../../../docs/image/html-asr.png" width="400"/>

## About Audio Recording

In `audio_recorder.js`, we developed a PCMAudioRecorder using Web Audio API to record PCM format audio. It asynchronously converts sample points from floating-point numbers to 16-bit Int16Array through AudioWorkletNode and returns them via callback. The buffer size defaults to 1600 sample points, which is 100ms.
