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
import threading
import base64
from typing import Optional, Dict, Any

from dashscope.common.logging import logger
from dashscope.multimodal.dialog_state import DialogState
from dashscope.multimodal.multimodal_dialog import MultiModalDialog, MultiModalCallback
from dashscope.multimodal.multimodal_request_params import (
    Upstream, Downstream, ClientInfo, RequestParameters, 
    Device, RequestToRespondParameters,BizParams
)

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
VIDEO_FRAME_INTERVAL = 0.5  # 500ms


class ListeningStateMonitor:
    """监控Listening状态的工具类"""
    
    def __init__(self):
        self.listening_event = threading.Event()
        self.listening_count = 0
        self.lock = threading.Lock()
    
    def on_listening_state(self):
        """当进入Listening状态时调用"""
        with self.lock:
            self.listening_count += 1
            logger.info(f"Listening state detected (count: {self.listening_count})")
            self.listening_event.set()
    
    def wait_for_next_listening(self, timeout: float = 30.0) -> bool:
        """
        等待下一次Listening状态
        
        Args:
            timeout: 超时时间（秒）
            
        Returns:
            bool: 是否成功等到Listening状态
        """
        # 清除当前事件状态
        self.listening_event.clear()
        
        logger.info(f"Waiting for next Listening state (timeout: {timeout}s)...")
        
        # 等待事件被设置
        success = self.listening_event.wait(timeout)
        
        if success:
            logger.info("Next Listening state detected!")
        else:
            logger.warning(f"Timeout waiting for Listening state after {timeout}s")
        
        return success
    
    def get_listening_count(self) -> int:
        """获取Listening状态的计数"""
        with self.lock:
            return self.listening_count
    
    def reset(self):
        """重置监控器状态"""
        with self.lock:
            self.listening_count = 0
            self.listening_event.clear()


class ChatCallback(MultiModalCallback):
    """Callback handler for multi-modal conversation events"""
    
    def __init__(self, listening_monitor: ListeningStateMonitor, vqa_handler_func = None):
        self.first_listening = True
        self.listening_monitor = listening_monitor
        self.vqa_handler_func = vqa_handler_func
        
    
    def on_connected(self):
        logger.debug("Connected to server")

    def on_started(self, dialog_id: str):
        global g_dialog_id
        g_dialog_id = dialog_id
        logger.info(f"Dialog started: {dialog_id}")

    def on_stopped(self):
        logger.info("Dialog stopped")

    def on_state_changed(self, state: DialogState):
        global conver_instance
        
        state_messages = {
            DialogState.LISTENING: "Listening for input...",
            DialogState.THINKING: "Processing request...",
            DialogState.RESPONDING: "Generating response..."
        }
        if state in state_messages:
            logger.info(state_messages[state])
        
        # 监控Listening状态
        if state == DialogState.LISTENING:
            self.listening_monitor.on_listening_state()

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
            try:
                commands_str = payload["output"]["extra_info"]["commands"]
                if "visual_qa" in commands_str:
                    if self.vqa_handler_func:
                        self.vqa_handler_func()
                    logger.debug("handle visual_qa command>>>>")
            except:
                return
    def on_request_accepted(self):
        logger.debug("Request accepted")

    def on_close(self, close_status_code: int, close_msg: str):
        logger.info(f"Connection closed - Status: {close_status_code}, Message: {close_msg}")


class TMultiModalConversation:
    """Multi-modal conversation manager"""
    
    def __init__(self, app_id: str, workspace_id: str, api_key: str, 
                 dialog_id: str = "", conversation_mode: str = "duplex"):
        """Initialize conversation with provided credentials"""
        logger.debug("Initializing conversation")
        
        # 初始化Listening状态监控器
        self.listening_monitor = ListeningStateMonitor()
        
        # Configure request parameters
        up_stream = Upstream(type="AudioAndVideo", mode="duplex", audio_format="pcm")
        client_info = ClientInfo(user_id="demo_user", device=Device(uuid="demo_device_12345"))
        biz_params = BizParams(user_prompt_params={"user_name":"大米"})
        request_params = RequestParameters(
            upstream=up_stream,
            downstream=Downstream(voice=VOICE_NAME, sample_rate=SAMPLE_RATE),
            client_info=client_info,
            biz_params=biz_params
        )

        self.callback = ChatCallback(self.listening_monitor, vqa_handler_func =self.send_image_vqa)
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
        
        # 视频相关状态
        self.video_mode_active = False
        self.video_thread_running = False

    def start_conversation(self):
        """Start conversation session"""
        self.conversation.start("")
        logger.info("Conversation started")

    def get_conversation_mode(self) -> str:
        """Get current conversation mode"""
        return self.conversation.get_conversation_mode()

    def wait_for_listening_state(self, timeout: float = 30.0) -> bool:
        """
        等待系统进入Listening状态
        
        Args:
            timeout: 超时时间（秒）
            
        Returns:
            bool: 是否成功等到Listening状态
        """
        return self.listening_monitor.wait_for_next_listening(timeout)

    def get_listening_count(self) -> int:
        """获取Listening状态的计数"""
        return self.listening_monitor.get_listening_count()

    def start_speech_interaction(self, worker_id: int):
        """Start speech interaction with audio streaming"""
        # Wait for listening state
        while self.conversation.get_dialog_state() != DialogState.LISTENING:
            time.sleep(0.1)
        
        logger.info(f"Worker [{worker_id}] starting speech")
        self.conversation.send_heart_beat()
        self.conversation.start_speech()

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
        # 停止视频帧发送
        self.video_thread_running = False
        
        self.conversation.stop()
        logger.info("Conversation stopped")

    def _get_sample_images(self) -> str:
        """获取示例图片的base64数据"""
        sample_images = ""
        
        try:
            # 查找示例图片文件
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_dir = os.path.join(current_dir, '../../../sample-data/images')
            filename = "jpeg-bridge.jpg"
            
            # 如果有图片目录，读取图片文件
            if os.path.exists(image_dir):
                if filename in os.listdir(image_dir):
                    image_path = os.path.join(image_dir, filename)
                    with open(image_path, 'rb') as f:
                        image_data = base64.b64encode(f.read()).decode('utf-8')
                        sample_images = image_data
                        logger.debug(f"Loaded image: {filename}")
            
            # 如果没有找到图片，创建一个简单的测试图片
                
        except Exception as e:
            logger.error(f"Error loading sample images: {e}")
        
        logger.info(f"Loaded {len(sample_images)} sample images")
        return sample_images

    def send_image_vqa(self):
        """Test visual Q&A with image"""
        logger.info("Testing image VQA")

        image = {"type": "base64", "value": self._get_sample_images()}
        images_params = RequestToRespondParameters(images=[image])
        self.conversation.request_to_respond("prompt", "", parameters=images_params)

    def _get_audio_file(self, file_name: str) -> str:
        """Get audio file path"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        audio_files = [os.path.join(current_dir, '../../../sample-data/'+file_name)]
        return random.choice(audio_files)

    def send_stream_audio(self,file_name: str ,worker_id: int):
        # Stream audio file
        file_path = self._get_audio_file(file_name)

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
            conversation_mode=config.get('conversation_mode', 'duplex')
        )
        round_num = 0 
        # Start conversation
        conver_instance.start_conversation()
        
        # 等待第一次Listening状态
        logger.info(f"Worker [{worker_id}] waiting for first Listening state...")
        if not conver_instance.wait_for_listening_state(timeout=30.0):
            logger.error(f"Worker [{worker_id}] timeout waiting for first Listening state")
            return
        
        logger.info(f"Worker [{worker_id}] round: {round_num + 1}")
            
        # Start speech interaction
        if conver_instance.get_conversation_mode() != "duplex":
            conver_instance.start_speech_interaction(worker_id)
            
        # 发送第一次音频：看看前面有什么东西
        logger.info(f"Worker [{worker_id}] sending audio (round {round_num + 1})")
        conver_instance.send_stream_audio(file_name="look_front.wav", worker_id=worker_id)
            
        # Stop speech for push2talk mode
        if conver_instance.get_conversation_mode() == "push2talk":
            conver_instance.stop_speech_interaction()
            
        
        # 等待第二次Listening状态， VQA请求会在
        logger.info(f"Worker [{worker_id}] waiting for first Listening state...")
        if not conver_instance.wait_for_listening_state(timeout=30.0):
            logger.error(f"Worker [{worker_id}] timeout waiting for first Listening state")
            return
        

           
        # 等待一段时间让对话完成
        time.sleep(CONVERSATION_TIMEOUT)
        
        
        # 显示统计信息
        listening_count = conver_instance.get_listening_count()
        logger.info(f"Worker [{worker_id}] completed. Total Listening states: {listening_count}")
        
        # Cleanup
        conver_instance.stop_conversation()
        time.sleep(1)  # Brief cleanup delay
        
        logger.info(f"Worker {worker_id} completed successfully")
        
    except Exception as e:
        logger.error(f"Worker {worker_id} error: {e}")
        raise


def main():
    """Main function with configuration setup"""
    logger.info("Starting Multi-modal Dialog Demo with Video Support and Listening State Monitor")
    
    # ==================== Configuration Section ====================
    # TODO: Replace with your actual credentials
    APP_ID = ""  # Your app ID
    WORKSPACE_ID = ""  # Your workspace ID  
    API_KEY = ""  # Your API key
    DIALOG_ID = ""  # Optional: dialog ID for session continuation
    CONVERSATION_MODE = "duplex"  # Options: push2talk, tap2talk, duplex
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
