"""Shared hyperparameters for demo apps.

Override via environment variables:
    export FUN_REALTIME_SPACE_ID=your-bailian-space-id
    export FUN_REALTIME_MODEL=qwen-audio-3.0-realtime-plus
    # Optional: override the full base URL directly
    export FUN_REALTIME_BASE_URL=wss://your-bailian-space-id.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime
"""

import os

DEFAULT_MODEL = os.environ.get("FUN_REALTIME_MODEL", "qwen-audio-3.0-realtime-plus")
DEFAULT_SPACE_ID = os.environ.get("FUN_REALTIME_SPACE_ID", "")

# Priority: FUN_REALTIME_BASE_URL > FUN_REALTIME_SPACE_ID > public DashScope endpoint
if os.environ.get("FUN_REALTIME_BASE_URL"):
    DEFAULT_BASE_URL = os.environ["FUN_REALTIME_BASE_URL"]
elif DEFAULT_SPACE_ID:
    DEFAULT_BASE_URL = (
        f"wss://{DEFAULT_SPACE_ID}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime"
    )
else:
    DEFAULT_BASE_URL = "wss://dashscope.aliyuncs.com/api-ws/v1/realtime"
