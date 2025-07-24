#!/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

"""
Multi-modal Dialog Conversation Demo

This module demonstrates voice-based conversations with DashScope multi-modal dialog API.
"""

import random
import sys
import time
import os
import multiprocessing
import logging
from typing import Optional, Dict, Any

from dashscope.common.logging import logger
from dashscope.multimodal.dialog_state import DialogState
from dashscope.multimodal.multimodal_dialog import MultiModalDialog, MultiModalCallback
from dashscope.multimodal.multimodal_request_params import (
    Upstream, Downstream, ClientInfo, RequestParameters, 
    Device, RequestToRespondParameters
)
logger = logging.getLogger('dashscope')
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
# create formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to ch
console_handler.setFormatter(formatter)

# add ch to logger
logger.addHandler(console_handler)

# Global variables
g_dialog_id: Optional[str] = None
conver_instance: Optional['TMultiModalConversation'] = None
begin_time: int = 0

# Configuration constants
AUDIO_CHUNK_SIZE = 3200
AUDIO_SLEEP_INTERVAL = 0.1
MAX_CONVERSATION_ROUNDS = 2
CONVERSATION_TIMEOUT = 10
WEBSOCKET_URL = "wss://dashscope.aliyuncs.com/api-ws/v1/inference"
MODEL_NAME = "multimodal-dialog"
VOICE_NAME = "longxiaochun_v2"
SAMPLE_RATE = 48000


class ChatCallback(MultiModalCallback):
    """Callback handler for multi-modal conversation events"""
    
    def on_connected(self):
        logger.debug("Connected to server")

    def on_started(self, dialog_id: str):
        global g_dialog_id
        g_dialog_id = dialog_id
        logger.info(f"Dialog started: {dialog_id}")

    def on_stopped(self):
        logger.info("Dialog stopped")

    def on_state_changed(self, state: DialogState):
        state_messages = {
            DialogState.LISTENING: "Listening for input...",
            DialogState.THINKING: "Processing request...",
            DialogState.RESPONDING: "Generating response..."
        }
        if state in state_messages:
            logger.info(state_messages[state])

    def on_speech_audio_data(self, data: bytes):
        logger.debug(f"Received audio data: {len(data)} bytes")

    def on_error(self, error: Exception):
        logger.error(f"Error: {error}")
        sys.exit(1)

    def on_responding_started(self):
        global conver_instance
        logger.debug("Response started")
        if conver_instance:
            conver_instance.send_local_responding_started()

    def on_responding_ended(self, payload: Dict[str, Any]):
        logger.debug("Response ended")
        if conver_instance:
            conver_instance.send_local_responding_ended()

    def on_speech_content(self, payload: Dict[str, Any]):
        if payload:
            logger.debug(f"Speech content: {payload}")

    def on_responding_content(self, payload: Dict[str, Any]):
        if payload:
            logger.debug(f"Response content: {payload}")

    def on_request_accepted(self):
        logger.debug("Request accepted")

    def on_close(self, close_status_code: int, close_msg: str):
        logger.info(f"Connection closed - Status: {close_status_code}, Message: {close_msg}")


class TMultiModalConversation:
    """Multi-modal conversation manager"""
    
    def __init__(self, app_id: str, workspace_id: str, api_key: str, 
                 dialog_id: str = "", conversation_mode: str = "push2talk"):
        """Initialize conversation with provided credentials"""
        logger.debug("Initializing conversation")
        
        # Configure request parameters
        up_stream = Upstream(type="AudioOnly", mode=conversation_mode, audio_format="pcm")
        client_info = ClientInfo(user_id="demo_user", device=Device(uuid="demo_device_12345"))
        request_params = RequestParameters(
            upstream=up_stream,
            downstream=Downstream(voice=VOICE_NAME, sample_rate=SAMPLE_RATE),
            client_info=client_info
        )

        self.callback = ChatCallback()
        self.conversation = MultiModalDialog(
            app_id=app_id,
            workspace_id=workspace_id,
            url=WEBSOCKET_URL,
            request_params=request_params,
            multimodal_callback=self.callback,
            api_key=api_key,
            dialog_id=dialog_id,
            model=MODEL_NAME
        )

    def start_conversation(self):
        """Start conversation session"""
        self.conversation.start("")
        logger.info("Conversation started")

    def get_conversation_mode(self) -> str:
        """Get current conversation mode"""
        return self.conversation.get_conversation_mode()

    def start_speech_interaction(self, worker_id: int):
        """Start speech interaction with audio streaming"""
        # Wait for listening state
        while self.conversation.get_dialog_state() != DialogState.LISTENING:
            time.sleep(0.1)
        
        logger.info(f"Worker [{worker_id}] starting speech")
        self.conversation.start_speech()

        # Stream audio file
        audio_file = self._get_audio_file()
        self._stream_audio(audio_file, worker_id)

    def stop_speech_interaction(self):
        """Stop speech interaction"""
        logger.info("Stopping speech")
        self.conversation.stop_speech()

    def send_local_responding_started(self):
        """Notify local response started"""
        self.conversation.local_responding_started()

    def send_local_responding_ended(self):
        """Notify local response ended"""
        self.conversation.local_responding_ended()

    def stop_conversation(self):
        """Stop conversation session"""
        self.conversation.stop()
        logger.info("Conversation stopped")

    def test_image_vqa(self, image_data: str, question: str, image_type: str = "base64"):
        """Test visual Q&A with image"""
        logger.info("Testing image VQA")
        image = {"type": image_type, "value": image_data}
        images_params = RequestToRespondParameters(images=[image])
        self.conversation.request_to_respond("prompt", question, parameters=images_params)

    def _get_audio_file(self) -> str:
        """Get audio file path"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        audio_files = [os.path.join(current_dir, '../../../sample-data/1_plus_1.wav')]
        return random.choice(audio_files)

    def _stream_audio(self, file_path: str, worker_id: int):
        """Stream audio file to conversation"""
        global begin_time
        
        if not os.path.exists(file_path):
            logger.error(f"Audio file not found: {file_path}")
            return
        
        logger.debug(f"Worker [{worker_id}] streaming: {file_path}")
        
        with open(file_path, "rb") as f:
            while True:
                data = f.read(AUDIO_CHUNK_SIZE)
                if not data:
                    break
                self.conversation.send_audio_data(data)
                time.sleep(AUDIO_SLEEP_INTERVAL)
            
            begin_time = int(time.time() * 1000)
            logger.debug(f"Worker [{worker_id}] streaming completed at: {begin_time}ms")
            
            # Send empty packets for non-push2talk modes
            if self.get_conversation_mode() != "push2talk":
                while self.conversation.get_dialog_state() == DialogState.LISTENING:
                    time.sleep(0.1)
                    self.conversation.send_audio_data(bytearray(AUDIO_CHUNK_SIZE))


def worker_process(config: Dict[str, Any]):
    """Worker process for conversation handling"""
    worker_id = config['worker_id']
    logger.info(f"Starting worker {worker_id}")
    
    global conver_instance
    
    try:
        # Initialize conversation with provided config
        conver_instance = TMultiModalConversation(
            app_id=config['app_id'],
            workspace_id=config['workspace_id'],
            api_key=config['api_key'],
            dialog_id=config.get('dialog_id', ''),
            conversation_mode=config.get('conversation_mode', 'push2talk')
        )
        
        # Start conversation
        conver_instance.start_conversation()
        
        # Run conversation rounds
        for round_num in range(MAX_CONVERSATION_ROUNDS):
            logger.debug(f"Worker [{worker_id}] round: {round_num + 1}")
            
            # Start speech interaction
            conver_instance.start_speech_interaction(worker_id)
            
            # Stop speech for push2talk mode
            if conver_instance.get_conversation_mode() == "push2talk":
                conver_instance.stop_speech_interaction()
            
            # Wait between rounds
            time.sleep(CONVERSATION_TIMEOUT)
        
        # Cleanup
        conver_instance.stop_conversation()
        time.sleep(1)  # Brief cleanup delay
        
        logger.info(f"Worker {worker_id} completed")
        
    except Exception as e:
        logger.error(f"Worker {worker_id} error: {e}")
        raise


def main():
    """Main function with configuration setup"""
    logger.info("Starting Multi-modal Dialog Demo")
    
    # ==================== Configuration Section ====================
    # TODO: Replace with your actual credentials
    APP_ID = ""  # Your app ID
    WORKSPACE_ID = ""  # Your workspace ID  
    API_KEY = ""  # Your API key
    DIALOG_ID = ""  # Optional: dialog ID for session continuation
    CONVERSATION_MODE = "push2talk"  # Options: push2talk, tap2talk, duplex
    NUM_PROCESSES = 1  # Number of concurrent conversations
    
    # Validate configuration
    if not all([APP_ID, WORKSPACE_ID, API_KEY]):
        logger.error("Please configure APP_ID, WORKSPACE_ID, and API_KEY")
        sys.exit(1)
    
    # ==================== Execution Section ====================
    try:
        # Prepare worker configurations
        worker_configs = []
        for i in range(1, NUM_PROCESSES + 1):
            config = {
                'worker_id': i,
                'app_id': APP_ID,
                'workspace_id': WORKSPACE_ID,
                'api_key': API_KEY,
                'dialog_id': DIALOG_ID,
                'conversation_mode': CONVERSATION_MODE
            }
            worker_configs.append(config)
        
        # Run worker processes
        with multiprocessing.Pool(processes=NUM_PROCESSES) as pool:
            pool.map(worker_process, worker_configs)
        
        logger.info("All processes completed successfully")
        
    except Exception as e:
        logger.error(f"Main process error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
