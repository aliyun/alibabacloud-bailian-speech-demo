# QWEN-OMNI Real-time Multimodal Large Model

English | [简体中文](./README.md)

## Overview

The Qwen-Omni series of models supports input in multiple modalities, including video, audio, images, and text, and outputs audio and text. The real-time API provides low-latency multimodal interaction capabilities, supporting streaming input of audio and video, and can stream output of text and audio.

## Features

- **Voice Conversation**: Multi-turn conversations with real-time voice and video as inputs.
- **Voice Interruption**: Supports voice interruption at any time during the interaction.
- **WebSocket Connection**: Low-latency real-time communication.

## Prerequisites

### 1. Obtain API Credentials
Please log in to the multimodal conversation console, activate the service, and create an application. You will then be able to obtain the following parameters:
- **API Key**: For authentication
- **Workspace ID**: Workspace identifier
- **App ID**: Application identifier

### 2. Environment Requirements

#### Java Environment
- Java 8 or higher
- Maven 3.6+

#### Python Environment
- Python 3.9 or higher
- pip package manager

### Others
For more API details, please refer to the [official documentation](https://help.aliyun.com/zh/model-studio/realtime).